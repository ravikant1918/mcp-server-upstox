import warnings
import os
import sys

# Suppress pandas and other library warnings that might interfere with stdio
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

from fastmcp import FastMCP
import json
from datetime import datetime, timedelta

from upstock_mcp.adapters.upstox_client import UpstoxClient
from upstock_mcp.engines.candle_engine import CandleEngine
from upstock_mcp.engines.indicator_engine import IndicatorEngine
from upstock_mcp.engines.pattern_engine import PatternEngine
from upstock_mcp.engines.context_engine import ContextEngine
from upstock_mcp.engines.account_engine import AccountEngine
from upstock_mcp.engines.instrument_engine import InstrumentEngine

# Initialize Engines
mcp = FastMCP("Upstox")
client = UpstoxClient()
instruments = InstrumentEngine()

async def _get_instrument_key(symbol: str, exchange: str) -> str:
    """Helper to resolve symbol to key with lazy loading."""
    await instruments.refresh_if_needed()
    key = instruments.resolve(symbol, exchange)
    return key if key else f"{exchange}|{symbol}"


# ----------------------------------------------------------------
# MARKET DATA TOOLS
# ----------------------------------------------------------------

@mcp.tool()
async def get_live_quote(symbol: str, exchange: str = "NSE_EQ") -> dict:
    """
    Fetch the most recent market quote (LTP, OHLC, Volume) for a given trading symbol.
    
    This tool automatically resolves standard symbols (like 'RELIANCE') to the specific instrument keys 
    required by the Upstox API using an internal mapping engine.
    
    :param symbol: Standard trading symbol (e.g., RELIANCE, TATAMOTORS, SBIN).
    :param exchange: The stock exchange. Defaults to 'NSE_EQ' (NSE Equity). Also supports 'BSE_EQ'.
    :return: A dictionary containing 'last_price', 'ohlc' (open, high, low, close), 'volume', and 'timestamp'.
    """
    symbol = symbol.upper()
    instrument_key = await _get_instrument_key(symbol, exchange)
    try:
        data = await client.get_market_quote(instrument_key, exchange)
        return data
    except Exception as e:
        return {"error": f"Error fetching quote for {symbol}: {str(e)}"}

@mcp.tool()
async def get_intraday_candles(symbol: str, interval: str = "1minute", exchange: str = "NSE_EQ") -> list:
    """
    Retrieve intraday OHLCV (Open, High, Low, Close, Volume) candle data for a symbol.
    
    The server automatically handles Down-sampling/Aggregation. If you request a 5-minute or 15-minute 
    interval that isn't natively supported for the current timeframe by Upstox, the server will 
    fetch 1-minute data and aggregate it for you.
    
    :param symbol: Standard trading symbol (e.g., INFOSYS).
    :param interval: The timeframe for each candle. 
                     Supported: '1minute', '3minute', '5minute', '10minute', '15minute', '30minute'.
    :param exchange: Exchange segment. Defaults to 'NSE_EQ'.
    :return: A list of objects, each containing 'timestamp', 'open', 'high', 'low', 'close', 'volume', and 'oi'.
    """
    symbol = symbol.upper()
    instrument_key = await _get_instrument_key(symbol, exchange)
    
    # Handle aggregation for non-native intervals
    fetch_interval = interval
    needs_resample = False
    if interval in ["3minute", "5minute", "10minute", "15minute"]:
        fetch_interval = "1minute"
        needs_resample = True

    try:
        raw_candles = await client.get_intraday_candles(instrument_key, fetch_interval)
        df = CandleEngine.to_dataframe(raw_candles)
        
        if needs_resample and not df.empty:
            df = CandleEngine.resample_candles(df, interval)
            
        return df.to_dict(orient='records')
    except Exception as e:
        return [{"error": f"Error fetching intraday data for {symbol}: {str(e)}"}]

# ----------------------------------------------------------------
# TECHNICAL ANALYSIS TOOLS
# ----------------------------------------------------------------

@mcp.tool()
async def get_technical_analysis(
    symbol: str, 
    exchange: str = "NSE_EQ", 
    interval: str = "1day", 
    indicators: list[str] = ["RSI", "EMA_20", "EMA_50", "MACD"]
) -> dict:
    """
    Comprehensive multi-indicator technical analysis 'Super Tool'.
    
    Combines live price data, calculated technical indicators, candlestick pattern detection, 
    trend context, and support/resistance levels into a single detailed report.
    
    :param symbol: Standard trading symbol (e.g., RELIANCE).
    :param exchange: Exchange segment. Defaults to 'NSE_EQ'.
    :param interval: Analysis timeframe. Supports '1minute', '5minute', '15minute', '30minute', '1day', '1week'.
    :param indicators: List of indicators to calculate. 
                       Supported: 'RSI', 'MACD', 'VWAP', 'ATR', 'BBANDS', 'EMA_x', 'SMA_x' 
                       (e.g., 'EMA_20', 'EMA_200').
    :return: A holistic dict with 'price', 'indicators', 'patterns' (e.g. Doji, Hammer), 
             'context' (Trend strength/bias), and 'levels' (Support/Resistance).
    """
    symbol = symbol.upper()
    instrument_key = await _get_instrument_key(symbol, exchange)

    
    # Handle aggregation
    fetch_interval = interval
    needs_resample = False
    if interval in ["3minute", "5minute", "10minute", "15minute"]:
        fetch_interval = "1minute"
        needs_resample = True
    elif interval == "1day":
        fetch_interval = "day"

    try:
        to_date = datetime.now().strftime('%Y-%m-%d')
        # Fetch enough data for indicators (EMA_200 needs more data)
        days_back = 100 if fetch_interval == "day" else 5
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d') 
        
        raw_candles = await client.get_historical_candles(instrument_key, fetch_interval, to_date, from_date)
        df = CandleEngine.to_dataframe(raw_candles)
        
        if df.empty:
            return {"error": f"No historical data found for {symbol}"}
            
        if needs_resample:
            df = CandleEngine.resample_candles(df, interval)
            
        df = IndicatorEngine.add_indicators(df, indicators)
        patterns = PatternEngine.detect_patterns(df)
        context = ContextEngine.analyze_trend(df)
        sr = IndicatorEngine.get_support_resistance(df)
        latest = CandleEngine.get_latest_candle(df)
        
        response = {
            "symbol": symbol,
            "interval": interval,
            "timestamp": latest.get('timestamp', str(datetime.now())),
            "price": latest.get('close'),
            "indicators": {k: v for k, v in latest.items() if k not in ['open','high','low','close','volume','oi','timestamp']},
            "patterns": patterns,
            "context": context,
            "levels": sr
        }
        return response
    except Exception as e:
        return {"error": f"Error in technical analysis for {symbol}: {str(e)}"}

# ----------------------------------------------------------------
# ACCOUNT TOOLS
# ----------------------------------------------------------------

@mcp.tool()
async def get_account_summary() -> dict:
    """
    Get a high-level overview of the linked Upstox account.
    
    Aggregates data across funds, holdings, and positions to provide a snapshot of total exposure, 
    portfolio P&L, and available capital.
    
    :return: A dictionary containing 'funds' (available margin), 'portfolio_summary' (total investment, 
             P&L), and counts of active holdings and positions.
    """
    try:
        funds = await client.get_funds()
        holdings = await client.get_holdings()
        positions = await client.get_positions()
        portfolio_summary = AccountEngine.summarize_portfolio(holdings, positions)
        
        return {
            "funds": funds,
            "portfolio_summary": portfolio_summary,
            "holdings_count": len(holdings),
            "positions_count": len(positions)
        }
    except Exception as e:
         return {"error": str(e)}

@mcp.tool()
async def get_holdings_list() -> list:
    """
    Fetch a detailed list of all long-term equity holdings in the account.
    
    Returns specific details for each holding including quantity, average buy price, 
    last traded price, and unrealized P&L.
    
    :return: A list of holding dictionaries.
    """
    try:
        holdings = await client.get_holdings()
        return holdings
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
async def get_positions_list() -> list:
    """
    Fetch a detailed list of all active intraday or short-term positions.
    
    Provides real-time data on open positions including net quantity, product type (MIS/CNC/etc.), 
    and realized/unrealized P&L for the day.
    
    :return: A list of position dictionaries.
    """
    try:
        positions = await client.get_positions()
        return positions
    except Exception as e:
         return [{"error": str(e)}]

if __name__ == "__main__":
    import os
    # Default to stdio, but allow sse/http via environment variable
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    if transport in ["sse", "http"]:
        # 'http' is for SSE based transport in FastMCP
        mcp.run(transport=transport, host="127.0.0.1", port=8000)
    else:
        mcp.run(transport="stdio")
