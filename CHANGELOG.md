# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
