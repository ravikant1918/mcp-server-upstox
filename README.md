# Upstox MCP Server 📈

A **Model Context Protocol (MCP)** server that integrates with the **Upstox Trading API**, enabling AI agents to securely access Indian stock market data, perform technical analysis, and view account information in **read-only mode**.

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

---

## ⚠️ Safety Notice

> This MCP server is **STRICTLY READ-ONLY**  
> ❌ No order placement  
> ❌ No order modification  
> ❌ No trading actions  
>
> Trading endpoints are intentionally excluded for safety.

---

## 📦 Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/upstox-mcp.git
cd upstox-mcp
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

Once installed, use the `upstox-mcp` command to start the server.

### Option A — Standard IO (for Claude Desktop)
Default mode for local agent usage.
```bash
upstox-mcp
```

### Option B — HTTP (Streamable)
Recommended for Cursor or remote MCP clients.
```bash
upstox-mcp --transport http
```

### Option C — Deployment via Docker
Run the server in a containerized environment.

1. **Using Docker Compose (Recommended)**:
   ```bash
   docker-compose up -d
   ```

2. **Using Docker CLI**:
   ```bash
   docker build -t upstox-mcp .
   docker run -d -p 8000:8000 --env-file .env upstox-mcp
   ```

Server will be available at: `http://localhost:8000/mcp`

---

## 🔌 MCP Client Configuration

### Claude Desktop
**Config path:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "upstox": {
      "command": "upstox-mcp",
      "env": {
        "UPSTOX_ACCESS_TOKEN": "your_access_token_here"
      }
    }
  }
}
```
*Note: Ensure the directory containing `upstox-mcp` is in your PATH.*

### Cursor (HTTP)
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
- **FastMCP** —MCP framework
- **Upstox** — Trading & market data API
- **Pandas-TA** — Technical indicators

## 📬 Disclaimer
This project is not affiliated with Upstox. Use at your own risk. Ensure compliance with Upstox API terms.
