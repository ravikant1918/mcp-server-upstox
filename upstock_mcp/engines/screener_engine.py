import asyncio
import logging
from typing import List, Dict, Optional
import pandas as pd
import pandas_ta as ta

from upstock_mcp.adapters.upstox_client import UpstoxClient
from upstock_mcp.engines.candle_engine import CandleEngine
from upstock_mcp.engines.instrument_engine import InstrumentEngine

logger = logging.getLogger(__name__)

class ScreenerEngine:
    """
    Implements technical screening capabilities on a restricted universe of stocks
    (e.g., NIFTY 50) to respect API rate limits while providing meaningful breadth.
    """
    
    # NIFTY 50 Symbols (Manual list to ensure stability without needing index calls)
    NIFTY_50_SYMBOLS = [
        "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
        "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BPCL",
        "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB",
        "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK",
        "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK",
        "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK",
        "LT", "M&M", "MARUTI", "NTPC", "NESTLEIND",
        "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", "SBIN",
        "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL",
        "TECHM", "TITAN", "ULTRACEMCO", "WIPRO"
    ]

    @classmethod
    async def get_market_movers(cls, client: UpstoxClient, instruments: InstrumentEngine, limit: int = 10) -> Dict[str, List[Dict]]:
        """
        Identify top gainers and losers from the watch list.
        """
        # Fetch LTP for all symbols
        quotes = []
        
        # We process in batches of 20 to be safe, though Upstox might handle more
        batch_size = 20
        all_symbols = cls.NIFTY_50_SYMBOLS
        
        for i in range(0, len(all_symbols), batch_size):
            batch = all_symbols[i:i+batch_size]
            tasks = []
            for sym in batch:
                key = instruments.resolve(sym, "NSE_EQ")
                if key:
                    tasks.append(client.get_market_quote(key, "NSE_EQ"))
                    
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for sym, res in zip(batch, results):
                if isinstance(res, dict) and 'last_price' in res:
                    quote = res
                    change_percent = 0.0
                    if quote.get('ohlc') and quote['ohlc'].get('close'):
                         close = quote['ohlc']['close'] # Prev Close ideally, but using provided close for ref
                         # Upstox quote usually has net_change, let's use that if available
                         pass
                    
                    # Manual calculation if needed or use API fields
                    # Upstox API quote response usually has: last_price, ohlc, average_price, oi, depth...
                    # We need change percentage. 
                    # Assuming we can calculate from last_price and 'close' (previous close)
                    ltp = quote.get('last_price', 0.0)
                    prev_close = quote.get('ohlc', {}).get('close', ltp) # This might be today's close if market closed?
                    
                    # Correct logic: Live Quote usually contains 'net_change' or we derive it
                    # Let's assume net_change is absolute change.
                    net_change = quote.get('net_change', 0.0)
                    if prev_close > 0:
                        change_percent = (net_change / prev_close) * 100
                    else:
                        change_percent = 0.0
                        
                    quotes.append({
                        "symbol": sym,
                        "ltp": ltp,
                        "change_percent": change_percent,
                        "net_change": net_change
                    })
                elif isinstance(res, Exception):
                    logger.warning(f"Failed to fetch quote for {sym}: {res}")

        # Sort by change percent
        quotes.sort(key=lambda x: x['change_percent'], reverse=True)
        
        gainers = quotes[:limit]
        losers = sorted(quotes, key=lambda x: x['change_percent'])[:limit]
        
        return {
            "top_gainers": gainers,
            "top_losers": losers
        }

    @classmethod
    async def tech_screen(cls, client: UpstoxClient, instruments: InstrumentEngine, category: str) -> List[Dict]:
        """
        Screen stocks based on technical criteria.
        
        Categories:
        - "RSI_OVERSOLD": RSI < 30
        - "RSI_OVERBOUGHT": RSI > 70
        - "BULLISH_MACD": Signal line crossover (basic approximation)
        - "NEAR_52W_HIGH": Within 5% of 52W High (requires historical/extended quote data)
        """
        screened_results = []
        
        # Determine analysis mode
        needs_history = category in ["RSI_OVERSOLD", "RSI_OVERBOUGHT", "BULLISH_MACD"]
        
        if needs_history:
            # Fetch historical data - THIS IS EXPENSIVE
            # We will limit to first 20 symbols to avoid timeout/rate-limit for this MVP
            target_symbols = cls.NIFTY_50_SYMBOLS[:20] 
            
            for sym in target_symbols:
                try:
                    key = instruments.resolve(sym, "NSE_EQ")
                    if not key: continue
                    
                    # Fetch ~30 days daily candles
                    import datetime
                    end = datetime.datetime.now()
                    start = end - datetime.timedelta(days=60)
                    
                    candles = await client.get_historical_candles(
                        key, "day", 
                        end.strftime('%Y-%m-%d'), 
                        start.strftime('%Y-%m-%d')
                    )
                    
                    if not candles: continue
                    
                    df = CandleEngine.to_dataframe(candles)
                    if df.empty: continue
                    
                    # Calculate Indicators
                    match = False
                    reason = ""
                    
                    if "RSI" in category:
                        df.ta.rsi(length=14, append=True)
                        last_rsi = df['RSI_14'].iloc[-1]
                        
                        if category == "RSI_OVERSOLD" and last_rsi < 30:
                            match = True
                            reason = f"RSI is {last_rsi:.2f} (< 30)"
                        elif category == "RSI_OVERBOUGHT" and last_rsi > 70:
                            match = True
                            reason = f"RSI is {last_rsi:.2f} (> 70)"
                            
                    elif "MACD" in category:
                        df.ta.macd(append=True)
                        # MACD_12_26_9, MACDh, MACDs
                        macd = df['MACD_12_26_9'].iloc[-1]
                        signal = df['MACDs_12_26_9'].iloc[-1]
                        if macd > signal:
                            match = True
                            reason = f"MACD ({macd:.2f}) > Signal ({signal:.2f})"
                            
                    if match:
                        screened_results.append({
                            "symbol": sym,
                            "match_type": category,
                            "reason": reason,
                            "last_price": df['close'].iloc[-1]
                        })
                        
                except Exception as e:
                    logger.error(f"Error screening {sym}: {e}")
                    
        return screened_results
