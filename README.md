# Upstox MCP Server 📈

A **Model Context Protocol (MCP)** server that integrates with the **Upstox Trading API**, enabling AI agents to securely access Indian stock market data, perform technical analysis, and view account information in **read-only mode**.

Built using **FastMCP**, the production-grade Python framework for MCP servers.

---

## 🚀 Features

### 📊 Market Data
- Live quotes (LTP, OHLC, volume)
- Intraday candles (1m, 5m, 15m, 30m)
- Historical candle data

### 📈 Technical Analysis
- RSI, EMA, SMA, MACD, VWAP
- Candlestick pattern detection
- Trend context (Bullish / Bearish / Sideways)
- Support & resistance levels

### 👤 Account (Read-Only)
- Profile details
- Funds & margin summary
- Holdings
- Open positions

### 🤖 MCP Native
- Designed for AI agents
- Tool-first architecture
- Supports Claude Desktop, Cursor, and custom agents

### 🔌 Transports
- **STDIO** (Claude Desktop, CLI agents)
- **HTTP / SSE** (Cursor, web agents)

---

## ⚠️ Safety Notice

> This MCP server is **STRICTLY READ-ONLY**  
> ❌ No order placement  
> ❌ No order modification  
> ❌ No trading actions  
>
> Trading endpoints are intentionally excluded for safety.

---

## 🛠️ Tech Stack

- Python 3.10+
- [FastMCP](https://pypi.org/project/fastmcp/)
- Upstox Python SDK
- Pandas + Pandas-TA
- FastAPI (via FastMCP HTTP transport)

---

## 📦 Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/mcp-server-upstox.git
cd mcp-server-upstox
```

### 2️⃣ Install Dependencies
```bash
pip install -e .
```

---

## 🔐 Configuration

Create a `.env` file in the project root:
```env
UPSTOX_ACCESS_TOKEN=your_access_token_here
```

*The access token must be generated using Upstox OAuth and should have read-only scopes.*

---

## ▶️ Running the Server

The best way to run the server is using the `fastmcp` CLI, which handles transport switching automatically.

### Option A — Standard IO (Default)
Best for Claude Desktop or local agent usage.
```bash
fastmcp run upstock_mcp/server.py
```

### Option B — HTTP / SSE (Streamable)
Recommended for Cursor, web agents, or remote MCP clients.
```bash
fastmcp run upstock_mcp/server.py --transport http
```

*Note: The `--transport` flag defaults to `stdio`. Other supported transports include `http`, `sse`, and `inspector` (for the built-in web UI).*

Server will be available at:
`http://localhost:8000/mcp`

---

## 🔌 MCP Client Configuration

### Claude Desktop
**Config path:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "upstox": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-server-upstox/upstock_mcp/server.py"],
      "env": {
        "UPSTOX_ACCESS_TOKEN": "your_access_token_here"
      }
    }
  }
}
```

### Cursor (HTTP / SSE)
Open Cursor Settings → Features → MCP. Add a new server:
- **Name**: Upstox
- **Type**: http
- **URL**: `http://localhost:8000/mcp`

---

## 🧠 Example Prompts (AI Agent)

### Market Data
- "What's the current price of RELIANCE?"
- "Show 1-minute candles for INFOSYS"

### Technical Analysis
- "Run RSI and EMA-20 analysis on TATAMOTORS"
- "Is SBIN trending bullish or bearish today?"

### Account
- "Show my available margin in Upstox"
- "List my current holdings"
- "What are my open positions and P&L?"

---

## 🧰 Available Tools

| Tool Name | Description |
| --- | --- |
| `get_live_quote` | Live price, OHLC, volume |
| `get_intraday_candles` | Intraday OHLCV data |
| `get_historical_candles` | Historical market data |
| `get_technical_analysis` | RSI, EMA, MACD, trend, S/R |
| `get_account_summary` | Funds + overview |
| `get_holdings_list` | All equity holdings |
| `get_positions_list` | Active positions |

---

## 🏗️ Architecture
AI Agent (Claude / Cursor) ↓ MCP ↓ FastMCP Server ↓ Upstox API (Read-Only)

---

## 📄 License
MIT License

## 🙌 Credits
- **FastMCP** — Production MCP framework
- **Upstox** — Trading & market data API
- **Pandas-TA** — Technical indicators

## 📬 Disclaimer
This project is not affiliated with Upstox. Use at your own risk. Ensure compliance with Upstox API terms.
