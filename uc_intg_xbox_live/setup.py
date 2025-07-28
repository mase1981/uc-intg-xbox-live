import logging
import httpx
import ssl
import certifi
from ucapi import (
    DriverSetupRequest,
    AbortDriverSetup,
    SetupComplete,
    SetupError,
    IntegrationSetupError,
    RequestUserInput,
)
from config import XboxLiveConfig
from auth import XboxAuth

_LOG = logging.getLogger("XBOX_LIVE_SETUP")

class XboxLiveSetup:
    def __init__(self, api, config: XboxLiveConfig, on_setup_complete):
        self.api = api
        self.config = config
        self.on_setup_complete = on_setup_complete
        self.auth_session: httpx.AsyncClient | None = None

    async def handle_command(self, request):
        if isinstance(request, DriverSetupRequest):
            if request.reconfigure or not self.config.tokens:
                self.config.liveid = request.setup_data.get("liveid", "").strip()
                self.config.giantbomb_api_key = request.setup_data.get("giantbomb_api_key", "").strip()

                if not self.config.liveid or not self.config.giantbomb_api_key:
                    return SetupError(IntegrationSetupError.INVALID_INPUT)

                _LOG.info(f"Live ID and Giant Bomb Key captured. Starting new auth flow.")
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                self.auth_session = httpx.AsyncClient(verify=ssl_context)
                auth_handler = XboxAuth(self.auth_session)
                auth_url = auth_handler.generate_auth_url()

                return RequestUserInput(
                    {"en": "Xbox Authentication"},
                    [
                        {"id": "auth_url", "label": {"en": "Login URL"}, "field": {"text": {"value": auth_url, "read_only": True}}},
                        {"id": "redirect_url", "label": {"en": "Paste the full redirect URL here"}, "field": {"text": {"value": ""}}},
                    ]
                )
            else:
                _LOG.info("Configuration already exists. Completing setup.")
                await self.on_setup_complete()
                return SetupComplete()

        if hasattr(request, 'input_values') and "redirect_url" in request.input_values:
            redirect_url = request.input_values.get("redirect_url", "").strip()
            if not self.auth_session:
                return SetupError(IntegrationSetupError.OTHER)

            auth_handler = XboxAuth(self.auth_session)
            try:
                tokens = await auth_handler.process_redirect_url(redirect_url)
            finally:
                await self._cleanup_session()

            if not tokens:
                return SetupError(IntegrationSetupError.AUTHENTICATION_FAILED)

            self.config.tokens = tokens
            await self.config.save(self.api)
            await self.on_setup_complete()
            return SetupComplete()

        if isinstance(request, AbortDriverSetup):
            await self._cleanup_session()
            return

        return SetupError(IntegrationSetupError.OTHER)

    async def _cleanup_session(self):
        if self.auth_session and not self.auth_session.is_closed:
            await self.auth_session.aclose()