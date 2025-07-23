import asyncio
import logging
import os
import httpx
import ssl
import certifi
from pathlib import Path
from ucapi import IntegrationAPI, DeviceStates, Events
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.scripts import CLIENT_ID, CLIENT_SECRET

from .config import XboxLiveConfig
from .setup import XboxLiveSetup
from .media_player_entity import XboxPresenceMediaPlayer

_LOG = logging.getLogger(__name__)
UPDATE_INTERVAL_SECONDS = 60

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

# Logic Functions
async def on_setup_complete():
    _LOG.info("✅ Setup complete, proceeding to connect.")
    await connect_and_create_entity()

async def connect_and_create_entity():
    global ENTITY, CLIENT, HTTP_SESSION
    if not CONFIG.tokens or not CONFIG.liveid:
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

        _LOG.info("Fetching user profile to get gamertag...")
        profile = await CLIENT.profile.get_profile_by_xuid(CLIENT.xuid)

        # --- THIS IS THE FIX ---
        # The 'settings' attribute is a list, so we loop through it
        gamertag = "Xbox User"  # A default fallback name
        for setting in profile.profile_users[0].settings:
            if setting.id == "ModernGamertag":
                gamertag = setting.value
                break
        _LOG.info(f"Gamertag found: {gamertag}")

        await API.set_device_state(DeviceStates.CONNECTED)

        if not ENTITY:
            ENTITY = XboxPresenceMediaPlayer(API, CONFIG.liveid, gamertag)
            API.configured_entities.add(ENTITY)
            API.available_entities.add(ENTITY)

        start_presence_updates()

    except Exception as e:
        _LOG.exception("❌ Failed to authenticate or create entity", exc_info=e)
        if HTTP_SESSION and not HTTP_SESSION.is_closed:
            await HTTP_SESSION.aclose()
        await API.set_device_state(DeviceStates.ERROR)

def start_presence_updates():
    global UPDATE_TASK
    if UPDATE_TASK:
        UPDATE_TASK.cancel()
    UPDATE_TASK = loop.create_task(presence_update_loop())

async def presence_update_loop():
    _LOG.info(f"Starting presence update loop (will refresh every {UPDATE_INTERVAL_SECONDS}s).")
    while True:
        try:
            if CLIENT:
                _LOG.info("Fetching Xbox presence...")
                presence = await CLIENT.presence.get_presence(CLIENT.xuid)

                game_info = {"state": presence.state}
                if presence.state.lower() == "online" and presence.title_records:
                    active_title = presence.title_records[0]
                    game_info["title"] = active_title.name
                    for item in active_title.display_image:
                        if item.type == "Icon":
                            game_info["image"] = item.url
                            break
                else:
                    game_info["title"] = "Home" if presence.state.lower() == "online" else "Offline"
                    game_info["image"] = None

                if ENTITY:
                    await ENTITY.update_presence(game_info)
            else:
                _LOG.warning("Update loop running but client is not authenticated.")
        except Exception as e:
            _LOG.exception("❌ Error during presence update loop", exc_info=e)

        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)

@API.listens_to(Events.CONNECT)
async def on_connect() -> None:
    await API.set_device_state(DeviceStates.CONNECTED)

# Main Execution
SETUP_HANDLER = XboxLiveSetup(API, CONFIG, on_setup_complete)

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    driver_path = str(Path(__file__).resolve().parent.parent / "driver.json")
    await API.init(driver_path, SETUP_HANDLER.handle_command)
    await CONFIG.load(API)
    _LOG.info("🚀 Xbox Live Driver is up and discoverable.")
    await connect_and_create_entity()

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