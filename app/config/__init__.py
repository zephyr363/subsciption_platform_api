from .exceptions import ConfigurationError
from .settings import Settings

try:
    settings = Settings()
except Exception as err:
    raise ConfigurationError("Failed to load configuration settings.") from err

__all__ = ["settings", "ConfigurationError"]
