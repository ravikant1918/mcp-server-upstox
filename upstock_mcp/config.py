import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

# Setup logging for config
logger = logging.getLogger("upstock_mcp.config")

class Settings(BaseSettings):
    # Credentials
    UPSTOX_ACCESS_TOKEN: str = ""
    UPSTOX_API_KEY: str = ""
    UPSTOX_API_SECRET: str = ""
    
    # API Settings
    UPSTOX_API_BASE_URL: str = "https://api.upstox.com"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def validate_and_warn(self):
        """Log warnings for missing optional configuration."""
        if not self.UPSTOX_ACCESS_TOKEN:
             logger.warning("UPSTOX_ACCESS_TOKEN is not set in environment or .env file.")
        if not self.UPSTOX_API_KEY:
             logger.warning("UPSTOX_API_KEY is not set. Some features may be limited.")

config = Settings()
# Run validation (warnings) on import
config.validate_and_warn()
