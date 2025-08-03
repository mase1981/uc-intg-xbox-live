import asyncio
import logging
import httpx
import ssl
import certifi
from pathlib import Path
from ucapi import IntegrationAPI, DeviceStates, Events
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.scripts import CLIENT_ID, CLIENT_SECRET

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

# --- Giant Bomb Artwork Fetcher ---
async def get_artwork_from_giant_bomb(session: httpx.AsyncClient, game_title: str, api_key: str) -> str | None:
    if not game_title or not api_key:
        return ""
    if game_title in ARTWORK_CACHE:
        return ARTWORK_CACHE[game_title]
    _LOG.info(f"Searching Giant Bomb for artwork for '{game_title}'...")
    search_url = "https://www.giantbomb.com/api/search/"
    params = {"api_key": api_key, "format": "json", "query": game_title, "resources": "game", "limit": 1}
    headers = {"User-Agent": "UC-Xbox-Integration"}
    try:
        resp = await session.get(search_url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("results"):
            image_url = data["results"][0].get("image", {}).get("original_url")
            if image_url:
                _LOG.info(f"✅ Found artwork: {image_url}")
                ARTWORK_CACHE[game_title] = image_url
                return image_url
        _LOG.warning(f"No artwork found on Giant Bomb for '{game_title}'.")
    except Exception:
        _LOG.exception("❌ Error fetching data from Giant Bomb API.")
    ARTWORK_CACHE[game_title] = ""
    return ""

# --- Core Logic ---
async def on_setup_complete():
    _LOG.info("✅ Setup complete, proceeding to connect.")
    await connect_and_start_client()

async def connect_and_start_client():
    global CLIENT, HTTP_SESSION, ENTITY
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

        # Mirroring PSN: Create entity and add to AVAILABLE list only
        if not ENTITY:
            profile = await CLIENT.profile.get_profile_by_xuid(CLIENT.xuid)
            gamertag = "Xbox User"
            for setting in profile.profile_users[0].settings:
                if setting.id == "ModernGamertag":
                    gamertag = setting.value
                    break
            _LOG.info(f"Gamertag found: {gamertag}")
            ENTITY = XboxPresenceMediaPlayer(API, CONFIG.liveid, f"Gamertag: {gamertag}")
            API.available_entities.add(ENTITY)

        await API.set_device_state(DeviceStates.CONNECTED)
    except Exception as e:
        _LOG.exception("❌ Failed to authenticate or create entity", exc_info=e)
        if HTTP_SESSION and not HTTP_SESSION.is_closed:
            await HTTP_SESSION.aclose()
        await API.set_device_state(DeviceStates.ERROR)

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
                resp = await CLIENT.people.get_friends_own_batch(
                    [CLIENT.xuid]
                )
                presence = resp.people[0]
                game_info = {
                    "image": ""
                }
                game_title = None
                if presence.presence_state == "Offline":
                    game_info["state"] = "OFF"
                    game_info["title"] = "Offline"
                elif presence.presence_text:
                    game_title = presence.presence_text
                    _LOG.info(f"✅ Found active game: {game_title}")
                    game_info["title"] = game_title
                    if game_title == "Home":
                        game_info["state"] = "ON"
                    else:
                        game_info["state"] = "PLAYING"
                        game_info["image"] = await get_artwork_from_giant_bomb(HTTP_SESSION, game_title, CONFIG.giantbomb_api_key)
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
    if CONFIG.tokens and CONFIG.liveid and CONFIG.giantbomb_api_key:
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