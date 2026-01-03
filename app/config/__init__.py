from .exceptions import ConfigurationError
from .settings import Settings


settings = Settings()

__all__ = ["settings", "ConfigurationError"]
