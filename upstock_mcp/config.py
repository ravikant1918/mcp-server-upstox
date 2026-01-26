import os
from pydantic import ValidationError
from typing import Optional
from dotenv import load_dotenv

# Prioritize environment variables passed from the process (like MCP clients).
# load_dotenv by default does NOT override variables already set in the environment.
load_dotenv()

class Config:
    # Credentials
    UPSTOX_ACCESS_TOKEN: str = os.getenv("UPSTOX_ACCESS_TOKEN", "")
    UPSTOX_API_KEY: str = os.getenv("UPSTOX_API_KEY", "")
    UPSTOX_API_SECRET: str = os.getenv("UPSTOX_API_SECRET", "")
    
    # API Settings
    UPSTOX_API_BASE_URL: str = "https://api.upstox.com"
    
    # Validation
    @classmethod
    def validate(cls):
        if not cls.UPSTOX_ACCESS_TOKEN:
             print("WARNING: UPSTOX_ACCESS_TOKEN is not set in environment or .env file.")
        if not cls.UPSTOX_API_KEY:
             print("WARNING: UPSTOX_API_KEY is not set. Some features may be limited.")

config = Config()
# Run validation on import
config.validate()
