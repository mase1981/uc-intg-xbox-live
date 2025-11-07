"""
Xbox Live driver module for Unfolded Circle integration.

:copyright: (c) 2025 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
import httpx
from pathlib import Path
from ucapi import IntegrationAPI, DeviceStates, Events
from pythonxbox.api.client import XboxLiveClient
from pythonxbox.authentication.manager import AuthenticationManager
from pythonxbox.authentication.models import OAuth2TokenResponse
from pythonxbox.scripts import CLIENT_ID, CLIENT_SECRET

from uc_intg_xbox_live.config import XboxLiveConfig
from uc_intg_xbox_live.setup import XboxLiveSetup
from uc_intg_xbox_live.media_player_entity import XboxPresenceMediaPlayer

_LOG = logging.getLogger(__name__)
UPDATE_INTERVAL_SECONDS = 60

API: IntegrationAPI | None = None
CONFIG = XboxLiveConfig()
ENTITY: XboxPresenceMediaPlayer | None = None
UPDATE_TASK: asyncio.Task | None = None
CLIENT: XboxLiveClient | None = None
HTTP_SESSION: httpx.AsyncClient | None = None

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
        if HTTP_SESSION and not HTTP_SESSION.is_closed:
            _LOG.debug("Closing existing HTTP session before creating new one")
            await HTTP_SESSION.aclose()

        timeout = httpx.Timeout(connect=5.0, read=15.0, write=10.0, pool=5.0)
        HTTP_SESSION = httpx.AsyncClient(verify=True, timeout=timeout)
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
                profile = next((p for p in people if getattr(p, "xuid", None) == CLIENT.xuid), None)
                gamertag = "Xbox User"
                if profile:
                    gamertag = getattr(profile, "modern_gamertag", None) or gamertag
                    _LOG.info(f"Gamertag found: {gamertag}")
                else:
                    _LOG.warning("No profile returned for current XUID; using default gamertag")
                
                ENTITY = XboxPresenceMediaPlayer(API, CONFIG.liveid, f"Gamertag: {gamertag}")
                API.available_entities.add(ENTITY)
                _LOG.info("✅ Entity created and added to available entities.")
            except Exception as e:
                _LOG.exception("❌ Failed to create entity", exc_info=e)

        await asyncio.sleep(0.5)
        await API.set_device_state(DeviceStates.CONNECTED)
        _LOG.info("✅ Device state set to CONNECTED")

    except Exception as e:
        _LOG.exception("❌ Failed to authenticate", exc_info=e)
        if HTTP_SESSION and not HTTP_SESSION.is_closed:
            await HTTP_SESSION.aclose()
        await API.set_device_state(DeviceStates.ERROR)

async def on_connect() -> None:
    _LOG.info("Remote connected via WebSocket - confirming device state")
    if CLIENT and ENTITY:
        await API.set_device_state(DeviceStates.CONNECTED)
        _LOG.info("✅ Device state confirmed as CONNECTED after remote connection")

async def on_subscribe_entities(entity_ids: list[str]) -> None:
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
    UPDATE_TASK = asyncio.create_task(presence_update_loop())

async def presence_update_loop():
    while True:
        try:
            if CLIENT and HTTP_SESSION and ENTITY:
                _LOG.info("Fetching Xbox presence data...")
                
                game_info = {
                    "state": "OFF",
                    "title": "Offline",
                    "image": ""
                }
                
                try:
                    batch = await CLIENT.people.get_friends_by_xuid(CLIENT.xuid)
                    people = getattr(batch, "people", None) or []
                    
                    _LOG.debug(f"Retrieved {len(people)} people from API")
                    
                    profile = next((p for p in people if getattr(p, "xuid", None) == CLIENT.xuid), None)
                    
                    if profile:
                        _LOG.debug(f"Found own profile: xuid={CLIENT.xuid}")
                        presence_state = getattr(profile, "presence_state", "Offline")
                        _LOG.debug(f"Presence state: {presence_state}")
                        
                        if presence_state == "Offline":
                            game_info["state"] = "OFF"
                            game_info["title"] = "Offline"
                            game_info["image"] = ""
                        elif presence_state == "Online":
                            game_info["state"] = "ON"
                            presence_text = getattr(profile, "presence_text", None)
                            game_info["title"] = presence_text or "Online"
                            game_info["image"] = ""
                            
                            _LOG.debug(f"Presence text: {presence_text}")

                            presence_details = getattr(profile, "presence_details", None) or []
                            _LOG.debug(f"Found {len(presence_details)} presence details")
                            
                            for detail in presence_details:
                                detail_state = getattr(detail, "state", None)
                                is_primary = getattr(detail, "is_primary", False)
                                is_game = getattr(detail, "is_game", False)
                                title_id = getattr(detail, "title_id", None)
                                
                                _LOG.debug(f"Detail: state={detail_state}, is_primary={is_primary}, is_game={is_game}, title_id={title_id}")
                                
                                if detail_state == "Active" and title_id and is_game and is_primary:
                                    try:
                                        _LOG.info(f"Fetching title info for: {title_id}")
                                        title_response = await CLIENT.titlehub.get_title_info(title_id)
                                        titles = getattr(title_response, "titles", None) or []
                                        
                                        if titles:
                                            title_data = titles[0]
                                            game_info["state"] = "PLAYING"
                                            game_info["title"] = title_data.name
                                            game_info["image"] = title_data.display_image
                                            _LOG.info(f"✅ Found game: {title_data.name}")
                                            break
                                    except Exception as e:
                                        _LOG.error(f"Failed to fetch title info for {title_id}: {e}")
                    else:
                        _LOG.warning(f"Could not find own profile in people list (looking for xuid={CLIENT.xuid})")
                        
                except Exception as e:
                    _LOG.exception("❌ Error fetching presence data", exc_info=e)
                
                _LOG.debug(f"Updating entity with: {game_info}")
                await ENTITY.update_presence(game_info)
            else:
                _LOG.warning("Update loop running but client/entity not ready.")
        except Exception as e:
            _LOG.exception("❌ Error during presence update loop", exc_info=e)
        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)

async def main():
    global API, SETUP_HANDLER

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    loop = asyncio.get_running_loop()
    API = IntegrationAPI(loop)
    SETUP_HANDLER = XboxLiveSetup(API, CONFIG, on_setup_complete)

    API.listens_to(Events.CONNECT)(on_connect)
    API.listens_to(Events.SUBSCRIBE_ENTITIES)(on_subscribe_entities)

    driver_path = str(Path(__file__).resolve().parent.parent / "driver.json")
    await API.init(driver_path, SETUP_HANDLER.handle_command)
    await CONFIG.load(API)
    _LOG.info("🚀 Xbox Live Driver is up and discoverable.")

    if CONFIG.tokens and CONFIG.liveid:
        _LOG.info("Complete configuration found, attempting auto-reconnection...")
        await connect_and_start_client()
    else:
        _LOG.info("Incomplete configuration, requiring setup.")
        await API.set_device_state(DeviceStates.ERROR)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        _LOG.info("Driver stopped by user.")
    finally:
        if HTTP_SESSION and not HTTP_SESSION.is_closed:
            loop.run_until_complete(HTTP_SESSION.aclose())
        loop.close()