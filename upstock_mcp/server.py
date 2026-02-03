import warnings
import os
import sys
import logging
from functools import wraps

from fastmcp import FastMCP, Context
from starlette.requests import Request
from starlette.responses import HTMLResponse
from datetime import datetime, timedelta
from upstock_mcp.adapters.upstox_client import UpstoxClient
from upstock_mcp.engines.candle_engine import CandleEngine
from upstock_mcp.engines.indicator_engine import IndicatorEngine
from upstock_mcp.engines.pattern_engine import PatternEngine
from upstock_mcp.engines.context_engine import ContextEngine
from upstock_mcp.engines.account_engine import AccountEngine
from upstock_mcp.engines.instrument_engine import InstrumentEngine
from upstock_mcp.utils import format_response, format_error
from upstock_mcp.templates import HTML_CONTENT
from concurrent.futures import ThreadPoolExecutor

# Module logger
logger = logging.getLogger(__name__)

# Initialize Engines
mcp = FastMCP("Upstox")

# Global Resource Pool
# Use a single executor for all client instances to prevent resource exhaustion
global_executor = ThreadPoolExecutor(max_workers=20, thread_name_prefix="upstox_worker")

async def _get_client(ctx: Context) -> UpstoxClient:
    """Helper to get authorized client from context headers or environment."""
    headers = {}
    if ctx and hasattr(ctx, "request_context") and ctx.request_context:
        # ctx.request_context is a RequestContext dataclass, not a dict
        request = getattr(ctx.request_context, "request", None)
        if request and hasattr(request, "headers"):
            headers = request.headers
    
    # Check for credentials in headers (BYOK support)
    # Headers are case-insensitive in Starlette
    api_key = headers.get("x-upstox-api-key")
    api_secret = headers.get("x-upstox-api-secret")
    access_token = headers.get("x-upstox-access-token")
    
    if api_key or api_secret or access_token:
        return UpstoxClient(access_token=access_token, api_key=api_key, api_secret=api_secret, executor=global_executor)
        
    return UpstoxClient(executor=global_executor)


# Tool wrapper to standardize error handling and logging for MCP tools
def mcp_wrapped_tool(name: str, error_type: str = "ToolError"):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(**kwargs):
            """Generic wrapper that only accepts keyword arguments to be compatible with FastMCP tool parsing (disallows *args)."""
            try:
                return await fn(**kwargs)
            except Exception as e:
                logger.exception("Unhandled error in tool %s", name)
                return format_response(error=format_error(str(e), error_type))
        # Register the wrapper as the MCP tool
        mcp.tool(name=name)(wrapper)
        return wrapper
    return decorator


@mcp.custom_route("/", methods=["GET"])
async def root_page(request: Request) -> HTMLResponse:
    """Home page for the Upstox MCP Server."""
    return HTMLResponse(HTML_CONTENT)

instruments = InstrumentEngine()

async def _get_instrument_key(symbol: str, exchange: str) -> str:
    """Helper to resolve symbol to key with lazy loading."""
    await instruments.refresh_if_needed()
    key = instruments.resolve(symbol, exchange)
    return key if key else f"{exchange}|{symbol}"


# ----------------------------------------------------------------
# MARKET DATA TOOLS
# ----------------------------------------------------------------

@mcp_wrapped_tool(name="market_get_live_quote", error_type="MarketDataError")
async def get_live_quote(symbol: str, exchange: str = "NSE_EQ", ctx: Context = None) -> dict:
    """
    Fetch the most recent market quote (LTP, OHLC, Volume) for a given trading symbol.
    """
    client = await _get_client(ctx)
    symbol = symbol.upper()
    instrument_key = await _get_instrument_key(symbol, exchange)
    try:
        data = await client.get_market_quote(instrument_key, exchange)
        return format_response(data=data, metadata={"symbol": symbol, "exchange": exchange})
    except Exception as e:
        # Let the wrapper handle logging and standardized error response
        return format_response(error=format_error(str(e), "MarketDataError"), metadata={"symbol": symbol})

@mcp_wrapped_tool(name="market_search_instruments", error_type="InstrumentSearchError")
async def search_instruments(query: str) -> dict:
    """
    Search for instruments by symbol or name.
    """
    try:
        await instruments.refresh_if_needed()
        results = instruments.search(query)
        return format_response(data=results, metadata={"query": query})
    except Exception as e:
        return format_response(error=format_error(str(e), "InstrumentSearchError"))

@mcp_wrapped_tool(name="market_get_instrument_details", error_type="InstrumentDetailsError")
async def get_instrument_details(symbol: str, exchange: str = "NSE_EQ") -> dict:
    """
    Get detailed information about a specific instrument.
    """
    try:
        await instruments.refresh_if_needed()
        details = instruments.get_details(symbol, exchange)
        if not details:
            return format_response(error=format_error(f"Instrument {symbol} not found on {exchange}", "NotFoundError"))
        return format_response(data=details, metadata={"symbol": symbol, "exchange": exchange})
    except Exception as e:
        return format_response(error=format_error(str(e), "InstrumentDetailsError"))

@mcp_wrapped_tool(name="market_get_intraday_candles", error_type="IntradayDataError")
async def get_intraday_candles(symbol: str, interval: str = "1minute", exchange: str = "NSE_EQ", ctx: Context = None) -> dict:
    """
    Retrieve intraday OHLCV (Open, High, Low, Close, Volume) candle data for a symbol.
    """
    client = await _get_client(ctx)
    symbol = symbol.upper()
    instrument_key = await _get_instrument_key(symbol, exchange)
    
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
            
        return format_response(data=df.to_dict(orient='records'), metadata={"symbol": symbol, "interval": interval})
    except Exception as e:
        return format_response(error=format_error(str(e), "IntradayDataError"), metadata={"symbol": symbol})

@mcp_wrapped_tool(name="market_get_historical_data", error_type="HistoricalDataError")
async def get_historical_data(
    symbol: str, 
    exchange: str = "NSE_EQ", 
    interval: str = "1day",
    start_time: str | None = None,
    end_time: str | None = None,
    ctx: Context = None
) -> dict:
    """
    Retrieve historical OHLC (Open, High, Low, Close) candlestick data.
    """
    client = await _get_client(ctx)
    symbol = symbol.upper()
    instrument_key = await _get_instrument_key(symbol, exchange)
    
    if not end_time:
        end_time = datetime.now().strftime('%Y-%m-%d')
    if not start_time:
        start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    interval_map = {
        "1minute": "1minute", "30minute": "30minute", "day": "day", 
        "1day": "day", "week": "week", "month": "month"
    }
    api_interval = interval_map.get(interval, "day")

    try:
        raw_candles = await client.get_historical_candles(instrument_key, api_interval, end_time, start_time)
        df = CandleEngine.to_dataframe(raw_candles)
        return format_response(data=df.to_dict(orient='records'), metadata={"symbol": symbol, "interval": interval})
    except Exception as e:
        return format_response(error=format_error(str(e), "HistoricalDataError"), metadata={"symbol": symbol})

# ----------------------------------------------------------------
# TECHNICAL ANALYSIS TOOLS
# ----------------------------------------------------------------

@mcp_wrapped_tool(name="analysis_get_technical_analysis", error_type="TechnicalAnalysisError")
async def get_technical_analysis(
    symbol: str, 
    exchange: str = "NSE_EQ", 
    interval: str = "1day", 
    indicators: list[str] | None = None,
    ctx: Context = None
) -> dict:
    """
    Comprehensive multi-indicator technical analysis 'Super Tool'.
    """
    client = await _get_client(ctx)
    if indicators is None:
        indicators = ["RSI", "EMA_20", "EMA_50", "MACD"]

    symbol = symbol.upper()
    instrument_key = await _get_instrument_key(symbol, exchange)
    
    fetch_interval = interval
    needs_resample = False
    if interval in ["3minute", "5minute", "10minute", "15minute"]:
        fetch_interval = "1minute"
        needs_resample = True
    elif interval == "1day":
        fetch_interval = "day"

    try:
        to_date = datetime.now().strftime('%Y-%m-%d')
        days_back = 100 if fetch_interval == "day" else 5
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d') 
        
        raw_candles = await client.get_historical_candles(instrument_key, fetch_interval, to_date, from_date)
        df = CandleEngine.to_dataframe(raw_candles)
        
        if df.empty:
            return format_response(error=format_error(f"No historical data found for {symbol}", "NoDataError"))
            
        if needs_resample:
            df = CandleEngine.resample_candles(df, interval)
            
        df = IndicatorEngine.add_indicators(df, indicators)
        patterns = PatternEngine.detect_patterns(df)
        context = ContextEngine.analyze_trend(df)
        sr = IndicatorEngine.get_support_resistance(df)
        latest = CandleEngine.get_latest_candle(df)
        
        data = {
            "symbol": symbol,
            "interval": interval,
            "timestamp": latest.get('timestamp', str(datetime.now())),
            "price": latest.get('close'),
            "indicators": {k: v for k, v in latest.items() if k not in ['open','high','low','close','volume','oi','timestamp']},
            "patterns": patterns,
            "context": context,
            "levels": sr
        }
        return format_response(data=data, metadata={"symbol": symbol, "interval": interval})
    except Exception as e:
        return format_response(error=format_error(str(e), "TechnicalAnalysisError"), metadata={"symbol": symbol})

# --- Granular Technical Analysis ---

async def _get_df_for_analysis(symbol: str, exchange: str, interval: str, client: UpstoxClient, days_back: int = 100) -> any:
    instrument_key = await _get_instrument_key(symbol, exchange)
    
    fetch_interval = interval
    needs_resample = False
    if interval in ["3minute", "5minute", "10minute", "15minute"]:
        fetch_interval = "1minute"
        needs_resample = True
    elif interval == "1day":
        fetch_interval = "day"

    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d') 
    
    raw_candles = await client.get_historical_candles(instrument_key, fetch_interval, to_date, from_date)
    df = CandleEngine.to_dataframe(raw_candles)
    
    if not df.empty and needs_resample:
        df = CandleEngine.resample_candles(df, interval)
    return df

@mcp_wrapped_tool(name="analysis_calculate_moving_averages", error_type="AnalysisError")
async def calculate_moving_averages(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", periods: list[int] | None = None, ctx: Context = None) -> dict:
    """Calculate SMA and EMA for trend analysis."""
    client = await _get_client(ctx)
    if periods is None:
        periods = [20, 50, 200]
    df = await _get_df_for_analysis(symbol, exchange, interval, client, days_back=250)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    
    indicators = [f"EMA_{p}" for p in periods] + [f"SMA_{p}" for p in periods]
    df = IndicatorEngine.add_indicators(df, indicators)
    latest = df.iloc[-1].to_dict()
    data = {k: v for k, v in latest.items() if any(x in k for x in ['EMA', 'SMA'])}
    return format_response(data=data, metadata={"symbol": symbol, "periods": periods})

@mcp_wrapped_tool(name="analysis_calculate_rsi", error_type="AnalysisError")
async def calculate_rsi(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", period: int = 14, ctx: Context = None) -> dict:
    """Calculate Relative Strength Index (RSI) for momentum analysis."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    df = IndicatorEngine.add_indicators(df, ['RSI'])
    rsi_val = float(df.iloc[-1]['RSI_14'])
    return format_response(data={"rsi": rsi_val}, metadata={"symbol": symbol, "period": period})

@mcp_wrapped_tool(name="analysis_calculate_bollinger_bands", error_type="AnalysisError")
async def calculate_bollinger_bands(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Calculate Bollinger Bands for volatility analysis."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    df = IndicatorEngine.add_indicators(df, ['BBANDS'])
    latest = df.iloc[-1].to_dict()
    data = {k: v for k, v in latest.items() if 'BBU' in k or 'BBL' in k or 'BBM' in k}
    return format_response(data=data, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_calculate_support_resistance", error_type="AnalysisError")
async def calculate_support_resistance(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Identify key support and resistance levels."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client, days_back=200)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    data = IndicatorEngine.get_support_resistance(df)
    return format_response(data=data, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_calculate_volatility_metrics", error_type="AnalysisError")
async def calculate_volatility_metrics(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Calculate various volatility metrics (ATR) for risk assessment."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    df = IndicatorEngine.add_indicators(df, ['ATR'])
    atr_val = float(df.iloc[-1].filter(like='ATRr').iloc[0])
    return format_response(data={"atr": atr_val}, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_calculate_macd", error_type="AnalysisError")
async def calculate_macd(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Calculate MACD for trend and momentum analysis."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    df = IndicatorEngine.add_indicators(df, ['MACD'])
    latest = df.iloc[-1].to_dict()
    data = {k: v for k, v in latest.items() if 'MACD' in k}
    return format_response(data=data, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_calculate_stochastic", error_type="AnalysisError")
async def calculate_stochastic(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Calculate Stochastic Oscillator for momentum analysis."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    df = IndicatorEngine.add_indicators(df, ['STOCH'])
    latest = df.iloc[-1].to_dict()
    data = {k: v for k, v in latest.items() if 'STOCH' in k}
    return format_response(data=data, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_calculate_williams_r", error_type="AnalysisError")
async def calculate_williams_r(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Calculate Williams %R for momentum analysis."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    df = IndicatorEngine.add_indicators(df, ['WILLR'])
    willr_val = float(df.iloc[-1].filter(like='WILLR').iloc[0])
    return format_response(data={"williams_r": willr_val}, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_calculate_adx", error_type="AnalysisError")
async def calculate_adx(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Calculate ADX for trend strength analysis."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    df = IndicatorEngine.add_indicators(df, ['ADX'])
    latest = df.iloc[-1].to_dict()
    data = {k: v for k, v in latest.items() if 'ADX' in k or 'DMP' in k or 'DMN' in k}
    return format_response(data=data, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_calculate_fibonacci_levels", error_type="AnalysisError")
async def calculate_fibonacci_levels(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Calculate Fibonacci retracement and extension levels."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client, days_back=365)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    data = IndicatorEngine.calculate_fibonacci_levels(df)
    return format_response(data=data, metadata={"symbol": symbol})

@mcp_wrapped_tool(name="analysis_analyze_candlestick_patterns", error_type="AnalysisError")
async def analyze_candlestick_patterns(symbol: str, exchange: str = "NSE_EQ", interval: str = "1day", ctx: Context = None) -> dict:
    """Identify common candlestick patterns."""
    client = await _get_client(ctx)
    df = await _get_df_for_analysis(symbol, exchange, interval, client)
    if df.empty:
        return format_response(error=format_error("No data", "NoDataError"))
    patterns = PatternEngine.detect_patterns(df)
    return format_response(data=patterns, metadata={"symbol": symbol})

# ----------------------------------------------------------------
# ACCOUNT TOOLS
# ----------------------------------------------------------------

@mcp_wrapped_tool(name="account_get_summary", error_type="AccountSummaryError")
async def get_account_summary(ctx: Context = None) -> dict:
    """
    Get a high-level overview of the linked Upstox account.
    
    :return: A standardized response with portfolio overview.
    """
    client = await _get_client(ctx)
    try:
        funds = await client.get_funds()
        holdings = await client.get_holdings()
        positions = await client.get_positions()
        portfolio_summary = AccountEngine.summarize_portfolio(holdings, positions)
        
        data = {
            "funds": funds,
            "portfolio_summary": portfolio_summary,
            "holdings_count": len(holdings),
            "positions_count": len(positions)
        }
        return format_response(data=data)
    except Exception as e:
         return format_response(error=format_error(str(e), "AccountSummaryError"))

@mcp_wrapped_tool(name="account_get_user_margin", error_type="MarginFetchError")
async def get_user_margin(ctx: Context = None) -> dict:
    """
    Get available margin and fund details.
    
    :return: A standardized response with margin details.
    """
    client = await _get_client(ctx)
    try:
        funds = await client.get_funds()
        return format_response(data=funds)
    except Exception as e:
        return format_response(error=format_error(str(e), "MarginFetchError"))

@mcp_wrapped_tool(name="account_get_holdings_list", error_type="HoldingsFetchError")
async def get_holdings_list(ctx: Context = None) -> dict:
    """
    Fetch a detailed list of all long-term equity holdings in the account.
    
    :return: A standardized response with holdings data.
    """
    client = await _get_client(ctx)
    try:
        holdings = await client.get_holdings()
        return format_response(data=holdings)
    except Exception as e:
        return format_response(error=format_error(str(e), "HoldingsFetchError"))

@mcp_wrapped_tool(name="account_get_positions_list", error_type="PositionsFetchError")
async def get_positions_list(ctx: Context = None) -> dict:
    """
    Fetch a detailed list of all active intraday or short-term positions.
    
    :return: A standardized response with positions data.
    """
    client = await _get_client(ctx)
    try:
        positions = await client.get_positions()
        return format_response(data=positions)
    except Exception as e:
         return format_response(error=format_error(str(e), "PositionsFetchError"))

@mcp_wrapped_tool(name="account_get_order_book", error_type="OrderBookFetchError")
async def get_order_book(ctx: Context = None) -> dict:
    """
    Fetch the list of all orders for the day.
    
    :return: A standardized response with order book data.
    """
    client = await _get_client(ctx)
    try:
        orders = await client.get_orders()
        return format_response(data=orders)
    except Exception as e:
         return format_response(error=format_error(str(e), "OrderBookFetchError"))

@mcp_wrapped_tool(name="account_get_trade_history", error_type="TradeHistoryFetchError")
async def get_trade_history(ctx: Context = None) -> dict:
    """
    Fetch the list of all executions (trades) for the day.
    
    :return: A standardized response with trade data.
    """
    client = await _get_client(ctx)
    try:
        trades = await client.get_trades()
        return format_response(data=trades)
    except Exception as e:
         return format_response(error=format_error(str(e), "TradeHistoryFetchError"))

if __name__ == "__main__":
    import os
    # Default to stdio, but allow sse/http via environment variable
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    if transport in ["sse", "http"]:
        # 'http' is for SSE based transport in FastMCP
        mcp.run(transport=transport, host="127.0.0.1", port=8000)
    else:
        mcp.run(transport="stdio")
