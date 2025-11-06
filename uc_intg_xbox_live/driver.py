import asyncio
import logging
import httpx
import ssl
import certifi
from pathlib import Path
from ucapi import IntegrationAPI, DeviceStates, Events
from pythonxbox.api.client import XboxLiveClient
from pythonxbox.authentication.manager import AuthenticationManager
from pythonxbox.authentication.models import OAuth2TokenResponse
from pythonxbox.scripts import CLIENT_ID, CLIENT_SECRET

from config import XboxLiveConfig
from setup import XboxLiveSetup
from media_player_entity import XboxPresenceMediaPlayer

_LOG = logging.getLogger(__name__)
UPDATE_INTERVAL_SECONDS = 60
ARTWORK_CACHE = {}

# Global Objects
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

API = IntegrationAPI(loop)
CONFIG = XboxLiveConfig()
ENTITY: XboxPresenceMediaPlayer | None = None
UPDATE_TASK: asyncio.Task | None = None
CLIENT: XboxLiveClient | None = None
HTTP_SESSION: httpx.AsyncClient | None = None

def get_active_game_detail(presence_details):
    """Return the primary active game detail from presence details."""
    if not presence_details:
        return None
    return next(
        (d for d in presence_details
         if d.state == "Active" and d.title_id and d.is_game and d.is_primary),
        None
    )

async def on_setup_complete():
    _LOG.info("✅ Setup complete, proceeding to connect.")
    await connect_and_start_client()

async def connect_and_start_client():
    global CLIENT, HTTP_SESSION, ENTITY
    if not CONFIG.tokens or not CONFIG.liveid:
        _LOG.error("Missing tokens or liveid, cannot connect")
        await API.set_device_state(DeviceStates.ERROR)
        return

    _LOG.info("Attempting to authenticate with stored tokens...")
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        HTTP_SESSION = httpx.AsyncClient(verify=ssl_context)
        auth_mgr = AuthenticationManager(HTTP_SESSION, CLIENT_ID, CLIENT_SECRET, "")
        auth_mgr.oauth = OAuth2TokenResponse.model_validate(CONFIG.tokens)
        await auth_mgr.refresh_tokens()
        CONFIG.tokens = auth_mgr.oauth.model_dump()
        await CONFIG.save(API)
        CLIENT = XboxLiveClient(auth_mgr)
        _LOG.info("✅ Successfully authenticated with Xbox Live.")

        if not ENTITY:
            try:
                batch = await CLIENT.people.get_friends_by_xuid(CLIENT.xuid)
                people = getattr(batch, "people", None) or []
                gamertag = "Xbox User"
                if people:
                    profile = people[0]
                    gamertag = getattr(profile, "modern_gamertag", None) or gamertag
                else:
                    _LOG.warning("No people returned for current XUID; using default gamertag")
                _LOG.info(f"Gamertag found: {gamertag}")
                ENTITY = XboxPresenceMediaPlayer(API, CONFIG.liveid, f"Gamertag: {gamertag}")
                API.available_entities.add(ENTITY)
                _LOG.info("✅ Entity created and added to available entities.")
            except Exception as e:
                _LOG.exception("❌ Failed to create entity", exc_info=e)

        await asyncio.sleep(0.5)
        await API.set_device_state(DeviceStates.CONNECTED)
        _LOG.info("✅ Device state set to CONNECTED")
        await presence_update_loop()

    except Exception as e:
        _LOG.exception("❌ Failed to authenticate", exc_info=e)
        if HTTP_SESSION and not HTTP_SESSION.is_closed:
            await HTTP_SESSION.aclose()
        await API.set_device_state(DeviceStates.ERROR)

@API.listens_to(Events.CONNECT)
async def on_connect() -> None:
    """Called when remote connects via WebSocket."""
    _LOG.info("Remote connected via WebSocket - confirming device state")
    if CLIENT and ENTITY:
        await API.set_device_state(DeviceStates.CONNECTED)
        _LOG.info("✅ Device state confirmed as CONNECTED after remote connection")

@API.listens_to(Events.SUBSCRIBE_ENTITIES)
async def on_subscribe_entities(entity_ids: list[str]) -> None:
    """Listen for when the remote UI subscribes to our entity."""
    _LOG.debug(f"Received entity subscription for IDs: {entity_ids}")
    if ENTITY and ENTITY.id in entity_ids:
        _LOG.info("UI subscribed to our entity. Moving to configured list and starting updates.")
        API.configured_entities.add(ENTITY)
        start_presence_updates()

def start_presence_updates():
    global UPDATE_TASK
    if UPDATE_TASK and not UPDATE_TASK.done():
        _LOG.info("Update loop already running.")
        return
    _LOG.info("Starting presence update loop...")
    UPDATE_TASK = loop.create_task(presence_update_loop())

async def presence_update_loop():
    while True:
        try:
            if CLIENT and HTTP_SESSION and ENTITY:
                _LOG.info("Fetching Xbox presence data...")
                batch = await CLIENT.people.get_friends_by_xuid(CLIENT.xuid)
                people = getattr(batch, "people", None) or []
                if not people:
                    _LOG.warning("No people returned for current XUID; skipping presence update this cycle.")
                else:
                    profile = people[0]
                    game_info = {}
                    if profile.presence_state == "Offline":
                        game_info["state"] = "OFF"
                        game_info["title"] = "Offline"
                        game_info["image"] = ""
                    elif profile.presence_state == "Online":
                        game_info["state"] = "ON"
                        game_info["title"] = profile.presence_text or "Online"
                        game_info["image"] = ""

                        # Check for active game
                        presence_detail = None
                        if profile.presence_details:
                            presence_detail = next(
                                    (d for d in profile.presence_details
                                    if d.state == "Active" and d.title_id and d.is_game and d.is_primary),
                                    None
                                )

                        if presence_detail:
                            title = await CLIENT.titlehub.get_title_info(
                                presence_detail.title_id
                            )
                            titles = getattr(title, "titles", None) or []
                            if titles:
                                title_data = titles[0]
                                game_info["state"] = "PLAYING"
                                game_info["title"] = title_data.name
                                game_info["image"] = title_data.display_image
                await ENTITY.update_presence(game_info)
            else:
                _LOG.warning("Update loop running but client/entity not ready.")
        except Exception as e:
            _LOG.exception("❌ Error during presence update loop", exc_info=e)
        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)

# Main Execution
SETUP_HANDLER = XboxLiveSetup(API, CONFIG, on_setup_complete)

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    driver_path = str(Path(__file__).resolve().parent.parent / "driver.json")
    await API.init(driver_path, SETUP_HANDLER.handle_command)
    await CONFIG.load(API)
    _LOG.info("🚀 Xbox Live Driver is up and discoverable.")

    # Check if we have a complete configuration
    if CONFIG.tokens and CONFIG.liveid:
        _LOG.info("Complete configuration found, attempting auto-reconnection...")
        await connect_and_start_client()
    else:
        _LOG.info("Incomplete configuration, requiring setup.")
        await API.set_device_state(DeviceStates.ERROR)

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        _LOG.info("Driver stopped by user.")
    finally:
        if HTTP_SESSION and not HTTP_SESSION.is_closed:
            loop.run_until_complete(HTTP_SESSION.aclose())
        loop.close()
