import os
from pydantic import ValidationError
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPSTOX_ACCESS_TOKEN: str = os.getenv("UPSTOX_ACCESS_TOKEN", "")
    UPSTOX_API_BASE_URL: str = "https://api.upstox.com"
    
    # Validation
    @classmethod
    def validate(cls):
        if not cls.UPSTOX_ACCESS_TOKEN:
            # We don't raise error immediately to allow server to start and report error via tools if needed,
            # but strictly speaking for a secure server we might want to enforcement.
            # Following the prompt "Tokens only from ENV", we should probably warn or fail if missing.
            print("WARNING: UPSTOX_ACCESS_TOKEN is not set in environment variables.")

config = Config()
