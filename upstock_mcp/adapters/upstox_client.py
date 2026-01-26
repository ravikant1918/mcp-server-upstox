import asyncio
import logging
from typing import Dict, Any, List, Optional
import upstox_client
from upstox_client.rest import ApiException
from concurrent.futures import ThreadPoolExecutor

from upstock_mcp.config import config

# Setup logging
logger = logging.getLogger(__name__)

class UpstoxClient:
    """
    Async wrapper for official Upstox Python SDK.
    Since the SDK is synchronous, we use run_in_executor to avoid blocking the event loop.
    """
    
    def __init__(self):
        # Configure OAuth2 access token for authorization: OAUTH2
        self.configuration = upstox_client.Configuration()
        self.configuration.access_token = config.UPSTOX_ACCESS_TOKEN
        
        # Set API Key if available
        if config.UPSTOX_API_KEY:
            self.configuration.api_key['OAUTH2'] = config.UPSTOX_API_KEY
            
        self.configuration.host = config.UPSTOX_API_BASE_URL
        
        self.api_client = upstox_client.ApiClient(self.configuration)
        
        # Initialize specific APIs
        self.history_api = upstox_client.HistoryApi(self.api_client)
        self.market_quote_api = upstox_client.MarketQuoteApi(self.api_client)
        self.user_api = upstox_client.UserApi(self.api_client)
        self.portfolio_api = upstox_client.PortfolioApi(self.api_client)
        self.order_api = upstox_client.OrderApi(self.api_client) # For read-only order history
        
        # Executor for sync calls
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def _run_sync(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, lambda: func(*args, **kwargs))

    def _serialize_deep(self, data: Any) -> Any:
        """
        Recursively convert SDK objects (which have to_dict()) into standard dicts.
        Also handles dicts/lists containing such objects.
        """
        if hasattr(data, 'to_dict'):
            return self._serialize_deep(data.to_dict())
        
        if isinstance(data, dict):
            return {k: self._serialize_deep(v) for k, v in data.items()}
        
        if isinstance(data, (list, tuple, set)):
            return [self._serialize_deep(item) for item in data]
            
        return data

    # ----------------------------------------------------------------
    # MARKET DATA
    # ----------------------------------------------------------------
    
    async def get_market_quote(self, symbol: str, exchange: str = "NSE_EQ") -> Dict:
        """
        Get live quote.
        """
        # Construct instrument key
        instrument_key = symbol
        if "|" not in symbol and exchange:
             instrument_key = f"{exchange}|{symbol}"

        try:
            # SDK expects instrument_key as comma separated string
            response = await self._run_sync(
                self.market_quote_api.ltp,
                instrument_key,
                '2.0'
            )
            # Use deep serialization to handle objects inside dicts (like MarketQuoteSymbolLtp)
            return self._serialize_deep(response.data) if hasattr(response, 'data') else self._serialize_deep(response)
        except ApiException as e:
            logger.error(f"Upstox API Error (get_market_quote): {e}")
            raise

    async def get_historical_candles(self, instrument_key: str, interval: str, 
                                     to_date: str, from_date: str) -> List[List]:
        """
        Get historical candles.
        interval: 1minute, 30minute, day, week, month
        """
        try:
             # SDK signature: get_historical_candle_data(instrument_key, interval, to_date, from_date, api_version)
             # Note: SDK argument order might vary, checking standard generated code structure
             response = await self._run_sync(
                 self.history_api.get_historical_candle_data1,
                 instrument_key,
                 interval,
                 to_date,
                 from_date,
                 '2.0'
             )
             if hasattr(response, 'data') and hasattr(response.data, 'candles'):
                 return response.data.candles
             return []
        except ApiException as e:
            logger.error(f"Upstox API Error (get_historical_candles): {e}")
            raise

    async def get_intraday_candles(self, instrument_key: str, interval: str) -> List[List]:
        """
        Get intraday candles.
        """
        try:
            response = await self._run_sync(
                self.history_api.get_intra_day_candle_data,
                instrument_key,
                interval,
                '2.0'
            )
            if hasattr(response, 'data') and hasattr(response.data, 'candles'):
                return response.data.candles
            return []
        except ApiException as e:
            logger.error(f"Upstox API Error (get_intraday_candles): {e}")
            raise

    # ----------------------------------------------------------------
    # USER ACCOUNT
    # ----------------------------------------------------------------

    async def get_profile(self) -> Dict:
        try:
            response = await self._run_sync(self.user_api.get_profile, '2.0')
            return self._serialize_deep(response.data) if hasattr(response, 'data') else self._serialize_deep(response)
        except ApiException as e:
            logger.error(f"Upstox API Error (get_profile): {e}")
            raise

    async def get_funds(self) -> Dict:
        try:
            response = await self._run_sync(self.user_api.get_user_fund_margin, '2.0')
            return self._serialize_deep(response.data) if hasattr(response, 'data') else self._serialize_deep(response)
        except ApiException as e:
            logger.error(f"Upstox API Error (get_funds): {e}")
            raise

    async def get_holdings(self) -> List[Dict]:
        try:
            response = await self._run_sync(self.portfolio_api.get_holdings, '2.0')
            return self._serialize_deep(response.data) if hasattr(response, 'data') else self._serialize_deep(response)
        except ApiException as e:
            logger.error(f"Upstox API Error (get_holdings): {e}")
            raise

    async def get_positions(self) -> List[Dict]:
        try:
            response = await self._run_sync(self.portfolio_api.get_positions, '2.0')
            return self._serialize_deep(response.data) if hasattr(response, 'data') else self._serialize_deep(response)
        except ApiException as e:
            logger.error(f"Upstox API Error (get_positions): {e}")
            raise
    
    async def get_orders(self) -> List[Dict]:
        try:
            response = await self._run_sync(self.order_api.get_order_book, '2.0')
            return self._serialize_deep(response.data) if hasattr(response, 'data') else self._serialize_deep(response)
        except ApiException as e:
            logger.error(f"Upstox API Error (get_orders): {e}")
            raise
    
    async def get_trades(self) -> List[Dict]:
        try:
            response = await self._run_sync(self.order_api.get_trade_history, '2.0')
            return self._serialize_deep(response.data) if hasattr(response, 'data') else self._serialize_deep(response)
        except ApiException as e:
            logger.error(f"Upstox API Error (get_trades): {e}")
            raise
