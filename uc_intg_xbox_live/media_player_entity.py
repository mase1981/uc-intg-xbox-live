import logging
from ucapi.media_player import MediaPlayer

_LOG = logging.getLogger("XBOX_ENTITY")

async def empty_command_handler(entity, command, value):
    """A dummy command handler that logs commands but does nothing."""
    _LOG.info(f"Command '{command}' received with value '{value}'. No action taken.")
    return True

class XboxPresenceMediaPlayer(MediaPlayer):
    """Media Player entity to represent Xbox presence."""

    def __init__(self, api, live_id: str, gamertag: str):
        super().__init__(
            identifier=f"xbox-presence-{live_id}",
            name=gamertag,
            features=["POWER", "PLAY"],
            attributes={
                "state": "OFF",
                "media_title": "Offline",
                "media_artist": "Xbox Live",
                "media_image_url": "", # Initialize as empty string to prevent ucapi log errors
                "media_type": "GAME",
            },
            cmd_handler=empty_command_handler
        )
        self.api = api
        _LOG.info(f"✅ XboxPresenceMediaPlayer entity '{gamertag}' initialized.")

    async def update_presence(self, presence_data: dict):
        """Updates the entity's attributes based on new presence data from the driver."""
        new_state = presence_data.get("state")
        new_title = presence_data.get("title")
        new_art_uri = presence_data.get("image")

        attributes_to_update = {}

        if self.attributes.get("state") != new_state:
            attributes_to_update["state"] = new_state
        
        if self.attributes.get("media_title") != new_title:
            attributes_to_update["media_title"] = new_title

        if self.attributes.get("media_image_url") != new_art_uri:
            attributes_to_update["media_image_url"] = new_art_uri

        if attributes_to_update:
            self.api.configured_entities.update_attributes(self.id, attributes_to_update)
            _LOG.info(f"Entity updated: {attributes_to_update}")