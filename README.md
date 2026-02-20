# Upstox MCP Server: Global Model Context Protocol for Indian Equity Markets 📈

The **Official-style Upstox MCP Server** provides a high-performance
Model Context Protocol (MCP) integration for the Upstox Trading API.

It enables AI agents like Claude Desktop, Cursor IDE, and custom LLM
applications to securely access real-time Indian stock market data (NSE,
BSE, MCX) in strictly read-only mode.

------------------------------------------------------------------------

## 🚀 Install from PyPI

``` bash
pip install upstock-mcp
```

PyPI Page: https://pypi.org/project/upstock-mcp/

------------------------------------------------------------------------

## ⚡ Quick Start

``` bash
# Install
pip install upstock-mcp

# Run (stdio mode for Claude)
upstox-mcp

# Or HTTP mode
upstox-mcp --transport http
```

Server will run at: http://localhost:8000/mcp

------------------------------------------------------------------------

## 🔐 Configuration

Create a `.env` file:

    UPSTOX_ACCESS_TOKEN=your_access_token_here

Optional:

    UPSTOX_API_KEY=your_api_key
    UPSTOX_API_SECRET=your_api_secret

Note: Access tokens expire every 24 hours.

------------------------------------------------------------------------

## 🎯 Features

### Market Data

-   Live Quotes (LTP, OHLC, Volume)
-   Historical Data
-   Intraday Candles
-   Market Movers
-   Instrument Search

### Technical Analysis

-   RSI
-   MACD
-   SMA / EMA
-   Bollinger Bands
-   ATR
-   Fibonacci Levels
-   Support & Resistance
-   Candlestick Pattern Detection

### Account (Read-Only)

-   Portfolio Holdings
-   Positions
-   Margin Info
-   Order Book
-   Trade History

------------------------------------------------------------------------

## 🤖 MCP Compatible

Works with: - Claude Desktop - Cursor IDE - Any MCP-compatible AI agent

------------------------------------------------------------------------

## 🐳 Docker

``` bash
docker build -t upstox-mcp .
docker run -p 8000:8000 --env-file .env upstox-mcp
```

------------------------------------------------------------------------

## 🔒 Security

This server is strictly read-only.

No order placement\
No fund transfers\
No trading operations

Designed for research and analysis only.

------------------------------------------------------------------------

## 🧪 Example Prompts

-   What's the current price of RELIANCE?
-   Show RSI and MACD for INFY
-   Analyze SBIN technically
-   Show my portfolio summary

------------------------------------------------------------------------

## 📄 License

MIT License

------------------------------------------------------------------------

## ⚠ Disclaimer

This project is not affiliated with Upstox.

Trading involves risk.\
This tool is for educational and informational purposes only.
