import logging
from urllib.parse import urlparse, parse_qs
import httpx
from pythonxbox.authentication.manager import AuthenticationManager
from pythonxbox.scripts import CLIENT_ID, CLIENT_SECRET

_LOG = logging.getLogger("XBOX_LIVE_AUTH")
OAUTH2_DESKTOP_REDIRECT_URI = "https://login.live.com/oauth20_desktop.srf"

class XboxAuth:
    def __init__(self, session: httpx.AsyncClient):
        self.session = session
        self.auth_mgr = AuthenticationManager(
            session, CLIENT_ID, CLIENT_SECRET, OAUTH2_DESKTOP_REDIRECT_URI
        )
        _LOG.info("XboxAuth initialized.")

    def generate_auth_url(self) -> str:
        """Generates the Microsoft login URL."""
        return self.auth_mgr.generate_authorization_url()

    async def process_redirect_url(self, redirect_url: str) -> dict | None:
        """Processes the redirect URL to get tokens."""
        _LOG.info("Processing redirect URL...")
        try:
            parsed_url = urlparse(redirect_url)
            query_params = parse_qs(parsed_url.query)
            auth_code = query_params.get("code", [None])[0]

            if not auth_code:
                _LOG.error("Authorization code not found in redirect URL.")
                return None

            await self.auth_mgr.request_tokens(auth_code)
            _LOG.info("✅ OAuth2 tokens successfully retrieved.")
            # Use model_dump() as shown in your working example
            return self.auth_mgr.oauth.model_dump()
        except Exception:
            _LOG.exception("Error during token exchange.")
            return None
