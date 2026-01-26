import gzip
import json
import logging
import os
import pathlib
import httpx
import asyncio
from typing import List, Dict, Optional

# Setup logging
logger = logging.getLogger(__name__)

class InstrumentEngine:
    """
    Handles resolution of trading symbols to Upstox instrument keys.
    Downloads and caches the instrument master file from Upstox assets.
    """
    
    CACHE_DIR = pathlib.Path.home() / ".upstox_mcp_cache"
    NSE_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
    
    def __init__(self):
        self._instruments: Dict[str, str] = {} # "SYMBOL:EXCHANGE" -> instrument_key
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.CACHE_DIR / "instruments.json"
        
    async def refresh_if_needed(self, force: bool = False):
        """
        Refresh cache if missing or force requested.
        Loads into memory.
        """
        if not self.cache_file.exists() or force:
            logger.info("Downloading Upstox instrument master...")
            try:
                async with httpx.AsyncClient(follow_redirects=True) as client:
                    response = await client.get(self.NSE_URL)
                    response.raise_for_status()
                    
                    # Decompress and parse
                    content = gzip.decompress(response.content)
                    data = json.loads(content)
                    
                    # Filter and structure for quick lookup
                    # data is a list of dicts: [ {instrument_key, trading_symbol, exchange, ...}, ... ]
                    lookup = {}
                    for item in data:
                        symbol = item.get("trading_symbol")
                        exchange = item.get("exchange")
                        key = item.get("instrument_key")
                        if symbol and exchange and key:
                            lookup[f"{symbol}:{exchange}"] = key
                            
                    # Save to local cache
                    with open(self.cache_file, "w") as f:
                        json.dump(lookup, f)
                
                logger.info(f"Cached {len(lookup)} instruments.")
                        
            except Exception as e:
                logger.error(f"Failed to refresh instruments: {e}")
                if not self._instruments: # If we have nothing in memory, this is critical
                     return
        
        # Load from cache file to memory
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r") as f:
                    self._instruments = json.load(f)
                logger.info(f"Loaded {len(self._instruments)} instruments from cache.")
            except Exception as e:
                logger.error(f"Error loading instrument cache: {e}")

    def resolve(self, symbol: str, exchange: str = "NSE_EQ") -> Optional[str]:
        """
        Map symbol + exchange to instrument_key.
        Returns None if not found.
        """
        symbol = symbol.upper()
        exchange = exchange.upper()
        
        # Try exact match first
        key = self._instruments.get(f"{symbol}:{exchange}")
        if key:
            return key
            
        # Fallback: if exchange is NSE_EQ, sometimes people just mean NSE
        if exchange == "NSE_EQ":
            return self._instruments.get(f"{symbol}:NSE")
            
        return None

    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Search for instruments matching the query string in symbol.
        """
        query = query.upper()
        results = []
        for key_pair, instrument_key in self._instruments.items():
            symbol, exchange = key_pair.split(":")
            if query in symbol:
                results.append({
                    "symbol": symbol,
                    "exchange": exchange,
                    "instrument_key": instrument_key
                })
        return results[:50] # Limit to 50 results

    def get_details(self, symbol: str, exchange: str = "NSE_EQ") -> Optional[Dict]:
        """
        Get full details for a specific instrument.
        """
        instrument_key = self.resolve(symbol, exchange)
        if not instrument_key:
            return None
            
        return {
            "symbol": symbol.upper(),
            "exchange": exchange.upper(),
            "instrument_key": instrument_key
        }
