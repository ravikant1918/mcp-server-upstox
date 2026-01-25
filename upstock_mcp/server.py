from fastmcp import FastMCP
import json
from datetime import datetime, timedelta

from upstock_mcp.adapters.upstox_client import UpstoxClient
from upstock_mcp.engines.candle_engine import CandleEngine
from upstock_mcp.engines.indicator_engine import IndicatorEngine
from upstock_mcp.engines.pattern_engine import PatternEngine
from upstock_mcp.engines.context_engine import ContextEngine
from upstock_mcp.engines.account_engine import AccountEngine

# Initialize FastMCP
mcp = FastMCP("Upstox 📈")
client = UpstoxClient()

# ----------------------------------------------------------------
# MARKET DATA TOOLS
# ----------------------------------------------------------------

@mcp.tool()
async def get_live_quote(symbol: str, exchange: str = "NSE_EQ") -> str:
    """
    Get live market quote (LTP, Volume, OHLC) for a symbol.
    
    :param symbol: Trading symbol (e.g., RELIANCE)
    :param exchange: Exchange (NSE_EQ, BSE_EQ). Default NSE_EQ.
    """
    try:
        data = await client.get_market_quote(symbol, exchange)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_intraday_candles(symbol: str, interval: str = "1minute", exchange: str = "NSE_EQ") -> str:
    """
    Get intraday OHLCV candles for a symbol.
    
    :param symbol: Trading symbol (e.g., RELIANCE)
    :param interval: Timeframe (1minute, 3minute, 5minute, 10minute, 15minute, 30minute)
    :param exchange: Exchange (NSE_EQ, BSE_EQ)
    """
    instrument_key = f"{exchange}|{symbol}"
    try:
        raw_candles = await client.get_intraday_candles(instrument_key, interval)
        df = CandleEngine.to_dataframe(raw_candles)
        return df.to_json(orient='records', date_format='iso')
    except Exception as e:
        return json.dumps({"error": str(e)})

# ----------------------------------------------------------------
# TECHNICAL ANALYSIS TOOLS
# ----------------------------------------------------------------

@mcp.tool()
async def get_technical_analysis(
    symbol: str, 
    exchange: str = "NSE_EQ", 
    interval: str = "1day", 
    indicators: list[str] = ["RSI", "EMA_20", "EMA_50", "MACD"]
) -> str:
    """
    Get comprehensive technical analysis: indicators, patterns, trend context, and support/resistance levels.
    
    :param symbol: Trading symbol
    :param exchange: Exchange
    :param interval: Timeframe (e.g., 1day, 1hour, 15minute, 5minute)
    :param indicators: List of indicators (RSI, EMA_20, EMA_50, SMA_200, MACD, VWAP, BBANDS, ATR)
    """
    instrument_key = f"{exchange}|{symbol}"
    try:
        api_interval = "day" if interval == "1day" else interval
        
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d') 
        
        raw_candles = await client.get_historical_candles(instrument_key, api_interval, to_date, from_date)
        df = CandleEngine.to_dataframe(raw_candles)
        
        if df.empty:
            return json.dumps({"error": "No data found"})
            
        df = IndicatorEngine.add_indicators(df, indicators)
        patterns = PatternEngine.detect_patterns(df)
        context = ContextEngine.analyze_trend(df)
        sr = IndicatorEngine.get_support_resistance(df)
        latest = CandleEngine.get_latest_candle(df)
        
        response = {
            "symbol": symbol,
            "timestamp": latest.get('timestamp', str(datetime.now())),
            "price": latest.get('close'),
            "indicators": {k: v for k, v in latest.items() if k not in ['open','high','low','close','volume','oi','timestamp']},
            "patterns": patterns,
            "context": context,
            "levels": sr
        }
        return json.dumps(response, default=str, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

# ----------------------------------------------------------------
# ACCOUNT TOOLS
# ----------------------------------------------------------------

@mcp.tool()
async def get_account_summary() -> str:
    """Get read-only account summary: funds, holdings, and positions overview."""
    try:
        funds = await client.get_funds()
        holdings = await client.get_holdings()
        positions = await client.get_positions()
        portfolio_summary = AccountEngine.summarize_portfolio(holdings, positions)
        
        return json.dumps({
            "funds": funds,
            "portfolio_summary": portfolio_summary,
            "holdings_count": len(holdings),
            "positions_count": len(positions)
        }, default=str, indent=2)
    except Exception as e:
         return json.dumps({"error": str(e)})

@mcp.tool()
async def get_holdings_list() -> str:
    """Get detailed list of current long-term holdings."""
    try:
        holdings = await client.get_holdings()
        return json.dumps(holdings, default=str, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_positions_list() -> str:
    """Get detailed list of current short-term positions."""
    try:
        positions = await client.get_positions()
        return json.dumps(positions, default=str, indent=2)
    except Exception as e:
         return json.dumps({"error": str(e)})

if __name__ == "__main__":
    import os
    # Default to stdio, but allow sse/http via environment variable
    # Usage for SSE: export MCP_TRANSPORT=sse && python upstock_mcp/server.py
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    if transport in ["sse", "http"]:
        print(f"Starting FastMCP server with {transport.upper()} transport...")
        # 'http' and 'sse' are both supported. 'http' is the newer 'streamable http'
        mcp.run(transport=transport, host="0.0.0.0", port=8000)
    else:
        mcp.run(transport="stdio")
