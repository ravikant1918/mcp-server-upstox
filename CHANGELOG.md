# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-02-05

### Added
- **Professional Trading Enhancements**: Significantly enriched the tool suite for institutional-grade market analysis and session awareness.
- **Market Intelligence & Session Awareness**: Added `resolve_market_time_and_calendar` to provide authoritative IST market status, holiday awareness, and precise date/time resolution for agents.
- **Advanced Market Screener Engine**:
    - `fetch_technical_screener`: Powerful real-time scanning for RSI (Oversold/Overbought) and MACD (Bullish) signals within the NIFTY 50 universe.
    - `fetch_market_movers_and_trending_stocks_funds`: High-performance identification of top gainers, losers, and trending market assets.
- **Deep Portfolio Analytics**:
    - `get_equity_portfolio_holdings`: Comprehensive equity metrics including invested/current value and P&L snapshots.
    - `get_my_trading_positions_today`: Streamlined intraday position tracking with real-time risk disclaimers.
    - `get_specific_stock_position`: Targeted deep-dive into specific symbol performance and quantity metrics.
- **High-Performance Infrastructure**: Integrated `pytz` for professional-grade time zone handling across all temporal operations.

### Changed
- **Unified Schema & Documentation**: Re-engineered all tool docstrings for maximum LLM performance, providing rich context and clear usage examples.
- **Industrial-Strength LTP**: Upgraded `get_ltp` to support massive batch queries (up to 50 instruments) and enriched the output with critical F&O Open Interest (OI) metrics.

### Fixed
- **Architectural Cleanup**: Optimized `server.py` codebase, removing redundant logic and streamlining internal engine calls.

## [2.1.1] - 2026-02-02

### Optimized
- **Global Resource Management**: Implemented a global `ThreadPoolExecutor` to prevent resource exhaustion. Previously, a new thread pool was created for every request, leading to memory leaks.
- **Smart Instrument Caching**: Optimized `InstrumentEngine` to check memory before disk, significantly reducing I/O latency for symbol resolution.

### Changed
- **Production hardening**: Introduced a shared `DEFAULT_EXECUTOR` to avoid creating a thread pool per client and reduce thread explosion under load.
- **Instrument refresh safety**: `InstrumentEngine.refresh_if_needed` now uses an `asyncio.Lock` and performs atomic cache writes (tmp + os.replace) to prevent concurrent downloads and cache corruption.
- **Error handling & observability**: Standardized MCP tool error handling via `mcp_wrapped_tool` and replaced `logger.error(...)` with `logger.exception(...)` to capture tracebacks and improve debuggability.
- **Candle resampling fix**: `CandleEngine` now preserves timestamps as datetimes to enable correct resampling.

### Added
- **Bring Your Own Key (BYOK) Support**: Users can now provide their own Upstox credentials via HTTP headers (`X-Upstox-API-Key`, `X-Upstox-API-Secret`, `X-Upstox-Access-Token`).
- **Multi-User Architecture**: A single server deployment can now serve multiple users securely by using their individual keys.
- **Enhanced Landing Page**: New interactive UI for connection instructions, including a dynamic JSON configuration generator and copy-to-clipboard feature.
- **Tests & CI readiness**: Added unit tests and test scaffolding (including `tests/conftest.py`) covering candle conversion/resampling, config loading, instrument refresh concurrency, `UpstoxClient` exception paths, and the MCP tool wrapper.

## [2.0.0] - 2026-01-26

### Added
- **Granular Technical Analysis Tools**: Over 10+ new tools for individual indicator calculation:
    - `analysis_calculate_moving_averages`
    - `analysis_calculate_rsi`
    - `analysis_calculate_bollinger_bands`
    - `analysis_calculate_macd`
    - `analysis_calculate_adx`
    - `analysis_calculate_stochastic`
    - `analysis_calculate_williams_r`
    - `analysis_calculate_fibonacci_levels`
    - `analysis_calculate_volatility_metrics` (ATR)
    - `analysis_analyze_candlestick_patterns`
- **Historical Data**: New `market_get_historical_data` tool for custom timeframe candle retrieval.
- **Instrument Search**: New `market_search_instruments` and `market_get_instrument_details` for symbol discovery.
- **Account & Orders**:
    - `account_get_user_margin`
    - `account_get_order_book`
    - `account_get_trade_history`
- **Utilities**: Added `upstock_mcp/utils.py` for JSON-safe normalization (handling Pandas NaNs, NumPy floats, Timestamps).

### Changed
- **Tool Namespacing**: All tools are now namespaced (`market_`, `analysis_`, `account_`) for better discoverability and agent UX.
- **Standardized Response Format**: All tools now return a consistent schema: `{success, data, error, metadata}`.
- **Refined Schemas**: Fixed mutable default arguments in tool signatures to ensure stable MCP schema generation.
- **Improved Error Handling**: Tools now return structured error objects instead of simple strings.
- **Upgraded Internal Engines**: 
    - `IndicatorEngine` expanded to support many more indicators.
    - `InstrumentEngine` upgraded with search capabilities.

### Fixed
- **JSON Serialization**: Fixed silent failures when returning Pandas/NumPy data types to MCP clients.
- **Mutable Defaults**: Removed `list[str] = [...]` from tool signatures which caused schema instability in some clients.
- **Symbol Resolution**: Improved symbol-to-key resolution in `InstrumentEngine`.

### Security
- Maintained read-only integrity while expanding data retrieval capabilities.

## [1.0.0] - 2026-01-25

### Added
- Initial release of Upstox MCP Server.
- Basic market data (live quotes, intraday candles).
- Aggregate technical analysis "Super Tool".
- Basic account summary, holdings, and positions.
- Docker support.
