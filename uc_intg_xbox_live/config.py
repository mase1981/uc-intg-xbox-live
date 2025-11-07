"""
Xbox Live configuration module for Unfolded Circle integration.

:copyright: (c) 2025 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime

_LOG = logging.getLogger(__name__)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

@dataclass
class XboxLiveConfig:
    liveid: str | None = None
    tokens: dict | None = field(default_factory=dict)

    async def load(self, api):
        config_path = os.path.join(api.config_dir_path, "config.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            self.liveid = config_data.get("liveid")
            self.tokens = config_data.get("tokens")
            _LOG.info("✅ Configuration loaded successfully.")
        except (FileNotFoundError, json.JSONDecodeError):
            _LOG.info("Configuration file not found or is invalid. Starting fresh.")
        except Exception as e:
            _LOG.exception(f"❌ Failed to load configuration from {config_path}", exc_info=e)

    async def save(self, api):
        config_path = os.path.join(api.config_dir_path, "config.json")
        os.makedirs(api.config_dir_path, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=4, cls=DateTimeEncoder)
        _LOG.info(f"✅ Configuration saved to {config_path}")