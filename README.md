# Upstox MCP Server: Global Model Context Protocol for Indian Equity Markets 📈

<a href="https://glama.ai/mcp/servers/@ravikant1918/neurodev-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@ravikant1918/neurodev-mcp/badge" />
</a>

[![GitHub Star](https://img.shields.io/github/stars/ravikant1918/mcp-server-upstox?style=social)](https://github.com/ravikant1918/mcp-server-upstox)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Support](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP Version](https://img.shields.io/badge/MCP-1.26.0-orange.svg)](https://modelcontextprotocol.io/)

The **Official-style Upstox MCP Server** provides a high-performance **Model Context Protocol (MCP)** integration for the **Upstox Trading API**. It enables AI agents like **Claude Desktop**, **Cursor IDE**, and custom LLM applications to securely access real-time **Indian stock market data (NSE, BSE, MCX)**, perform advanced **technical analysis (RSI, MACD, Bollinger Bands)**, and manage portfolio information in a **strictly read-only mode**. 

Optimized for **algorithmic trading**, **market analysis**, and **automated research** on **Nifty 50**, **Bank Nifty**, and thousands of Indian equities.

> 📖 **Featured on Modern AI Day:** [The USB Port for AI: Connecting Claude to Real-Time Market Data](https://medium.com/@ravikantyadav1918/the-usb-port-for-ai-how-the-upstox-mcp-server-connects-claude-to-real-time-market-data-ba179358e891)
>
> 🌐 **Live Demo Instance:** [https://mcp-server-upstox.onrender.com/mcp](https://mcp-server-upstox.onrender.com/mcp)

---

## 🛠️ Technical Stack

- **Framework:** [FastMCP](https://github.com/jlowin/fastmcp) (MCP Python SDK)
- **API Engine:** [FastAPI](https://fastapi.tiangolo.com/) & [Uvicorn](https://www.uvicorn.org/)
- **Data Science:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Technical Analysis:** [Pandas-TA](https://github.com/twopirllc/pandas-ta)
- **Client Integration:** [Httpx](https://www.python-httpx.org/), [Upstox Python SDK](https://github.com/upstox/upstox-python)
- **Deployment:** [Docker](https://www.docker.com/), [Render](https://render.com/)


---

## ⚡ Quick Start (Remote BYOK)

Connect Claude Desktop to your remote instance in seconds using **Bring Your Own Key (BYOK)** support:

```json
{
  "mcpServers": {
    "Upstox-Remote": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp-server-upstox.onrender.com/mcp",
        "--header", "X-Upstox-API-Key:YOUR_API_KEY",
        "--header", "X-Upstox-API-Secret:YOUR_API_SECRET",
        "--header", "X-Upstox-Access-Token:YOUR_ACCESS_TOKEN"
      ]
    }
  }
}
```

---

## 🚀 Features

### 📊 Market Data
- **Live quotes** - `market_get_live_quote`
- **Search Instruments** - `market_search_instruments`
- **Historical data** - `market_get_historical_data` (Custom ranges)
- **Intraday candles** - `market_get_intraday_candles`

### 📈 Technical Analysis
- **Granular Indicators** - Individual tools for RSI, MACD, ADX, Bollinger Bands, etc.
- **Fibonacci Levels** - `analysis_calculate_fibonacci_levels`
- **Candlestick Patterns** - `analysis_analyze_candlestick_patterns`
- **Smart Context** - `analysis_get_technical_analysis` (Super Tool)

### 👤 Account Management (Read-Only)
- **Margin Details** - `account_get_user_margin`
- **Order Book** - `account_get_order_book`
- **Trade History** - `account_get_trade_history`
- **Portfolio** - Holdings and Positions lists

### 🤖 MCP Native
- **AI-First Design** - Built specifically for AI agents
- **Tool-Based Architecture** - Natural language to API calls
- **Multi-User Support** - Secure "Bring Your Own Key" (BYOK) architecture
- **Conversational Interface** - No complex API knowledge needed

---

## ⚠️ Safety Notice

> **This MCP server is STRICTLY READ-ONLY**  
> ❌ No order placement  
> ❌ No order modification  
> ❌ No fund transfers  
> ❌ No trading actions  
>
> Trading endpoints are intentionally excluded for your safety and security.

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Upstox Trading Account
- Upstox API credentials

### 1️⃣ Clone Repository
```bash
git clone https://github.com/ravikant1918/mcp-server-upstox.git
cd mcp-server-upstox
```

### 2️⃣ Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -e .
```

### 4️⃣ Verify Installation
```bash
upstox-mcp --version
```

---

## 🔐 Configuration

### Getting Upstox API Credentials

1. **Login to Upstox Developer Console**
   - Visit: https://api.upstox.com/
   - Login with your Upstox account

2. **Create an App**
   - Go to "My Apps"
   - Click "Create App"
   - Fill in details:
     - App Name: "MCP Server"
     - Redirect URL: `http://localhost:8000/callback`
     - Select read-only permissions

3. **Get API Keys**
   - Note down your `API Key` and `API Secret`

4. **Generate Access Token**
   - Follow Upstox OAuth flow
   - Or use Upstox's token generation tool
   - Token is valid for 24 hours (needs daily refresh)

### Environment Configuration

Create a `.env` file in the project root:

```env
# Required
UPSTOX_ACCESS_TOKEN=your_access_token_here

# Optional (for token auto-refresh)
UPSTOX_API_KEY=your_api_key
UPSTOX_API_SECRET=your_api_secret
```

**Security Best Practices:**
- Never commit `.env` file to version control
- Add `.env` to `.gitignore`
- Rotate tokens regularly
- Use read-only API scopes only

---

## ▶️ Running the Server

### Option A — Standard IO (for Claude Desktop)
Default mode for local AI agent usage:

```bash
upstox-mcp
# or
upstox-mcp --transport stdio
```

### Option B — HTTP Mode (for Cursor or Remote Access)
Recommended for web-based AI agents:

```bash
upstox-mcp --transport http
# Server will start on http://localhost:8000
```

Custom port:
```bash
upstox-mcp --transport http --port 8080
```

### Option C — Docker Deployment

#### Using Docker Compose (Recommended)
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

#### Using Docker CLI
```bash
# Build image
docker build -t upstox-mcp .

# Run container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name upstox-mcp \
  upstox-mcp

# View logs
docker logs -f upstox-mcp

# Stop container
docker stop upstox-mcp
```

Server will be available at: `http://localhost:8000/mcp`

---

## 🔌 MCP Client Configuration

### Claude Desktop

**Config Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "Upstox": {
      "command": "/absolute/path/to/venv/bin/upstox-mcp",
      "args": ["--transport", "stdio"],
      "env": {
        "UPSTOX_ACCESS_TOKEN": "YOUR_ACCESS_TOKEN"
      }
    }
  }
}
```

**Finding the absolute path:**
```bash
# On macOS/Linux
which upstox-mcp

# On Windows (PowerShell)
(Get-Command upstox-mcp).Path
```

### Cursor IDE

1. Open Cursor Settings
2. Go to **Features** → **MCP**
3. Add new server:
   - **Name**: Upstox
   - **Type**: HTTP
   - **URL**: `http://localhost:8000/mcp`

### Remote MCP (via mcp-remote) — BYOK Support

For running the server remotely or in a multi-user environment (e.g., Render), you can pass your credentials via headers. This is known as **Bring Your Own Key (BYOK)**.

```json
{
  "mcpServers": {
    "Upstox-Remote": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp-server-upstox.onrender.com/mcp",
        "--header", "X-Upstox-API-Key:YOUR_API_KEY",
        "--header", "X-Upstox-API-Secret:YOUR_API_SECRET",
        "--header", "X-Upstox-Access-Token:YOUR_ACCESS_TOKEN"
      ]
    }
  }
}
```

> [!TIP]
> This allows multiple users to use the same server instance securely without sharing credentials on the server side.

---

## 🧠 Example Prompts (For AI Agents)

### Market Data Queries
```
"What's the current price of RELIANCE?"
"Show me OHLC data for INFY"
"Get live quote for TATAMOTORS on NSE"
"What's the volume on SBIN today?"
```

### Technical Analysis
```
"Run technical analysis on BHARTIARTL"
"Show RSI and MACD for HDFCBANK"
"Is TCS in a bullish or bearish trend?"
"Find support and resistance levels for WIPRO"
"Analyze ICICIBANK with EMA-20 and EMA-50"
```

### Intraday Analysis
```
"Show me 5-minute candles for RELIANCE"
"Get 1-minute chart data for INFY"
"Display 15-minute intraday data for SBIN"
```

### Account Information
```
"Show my Upstox account summary"
"What's my available margin?"
"List all my holdings"
"Show my current positions and P&L"
"What's my total portfolio value?"
"How much profit/loss do I have in TRIDENT?"
```

### Complex Analysis
```
"Analyze all my holdings technically and rank them by strength"
"Compare HDFC Bank vs ICICI Bank - which is better?"
"Find oversold stocks in my watchlist (RSI < 30)"
"Which of my holdings are above their 50-day EMA?"
"Show me stocks breaking resistance levels today"
```

---

## 🧰 Available MCP Tools

| Category | Tool Name | Description |
| :--- | :--- | :--- |
| **Market** | `market_get_live_quote` | Last Traded Price, OHLC, Volume |
| **Market** | `market_search_instruments` | Search for trading symbols |
| **Market** | `market_get_instrument_details` | Detailed instrument metadata |
| **Market** | `market_get_historical_data` | Custom historical candle data |
| **Market** | `market_get_intraday_candles` | Real-time intraday charts |
| **Analysis** | `analysis_calculate_rsi` | Momentum analysis (RSI) |
| **Analysis** | `analysis_calculate_macd` | Trend & momentum (MACD) |
| **Analysis** | `analysis_calculate_adx` | Trend strength (ADX) |
| **Analysis** | `analysis_calculate_moving_averages` | Trend analysis (SMA/EMA) |
| **Analysis** | `analysis_calculate_bollinger_bands` | Volatility study |
| **Analysis** | `analysis_calculate_support_resistance` | Pivot-based levels |
| **Analysis** | `analysis_calculate_volatility_metrics` | Risk assessment (ATR) |
| **Analysis** | `analysis_calculate_stochastic` | Momentum oscillator |
| **Analysis** | `analysis_calculate_williams_r` | %R Momentum |
| **Analysis** | `analysis_calculate_fibonacci_levels`| Retracement levels |
| **Analysis** | `analysis_analyze_candlestick_patterns`| Pattern detection |
| **Analysis** | `analysis_get_technical_analysis`| Holistic multi-indicator report |
| **Account** | `account_get_summary` | Portfolio snapshot |
| **Account** | `account_get_user_margin` | Available funds |
| **Account** | `account_get_holdings_list` | Equity holdings |
| **Account** | `account_get_positions_list` | Active positions |
| **Account** | `account_get_order_book` | Daily orders |
| **Account** | `account_get_trade_history` | Daily executions |

> [!NOTE]
> All tools return a standardized JSON response: `{ "success": true, "data": ..., "error": null, "metadata": ... }`.

### Tool Details

#### `get_live_quote`
```python
{
  "symbol": "RELIANCE",      # Stock symbol
  "exchange": "NSE_EQ"       # NSE_EQ or BSE_EQ (default: NSE_EQ)
}
```

#### `get_intraday_candles`
```python
{
  "symbol": "INFY",
  "interval": "5minute",     # 1minute, 3minute, 5minute, 10minute, 15minute, 30minute
  "exchange": "NSE_EQ"
}
```

#### `get_technical_analysis`
```python
{
  "symbol": "SBIN",
  "interval": "1day",        # 1minute, 5minute, 15minute, 30minute, 1day, 1week
  "indicators": [            # Array of indicators
    "RSI",                   # Relative Strength Index
    "MACD",                  # Moving Average Convergence Divergence
    "EMA_20",                # Exponential Moving Average (20 period)
    "EMA_50",
    "SMA_200",               # Simple Moving Average (200 period)
    "BBANDS",                # Bollinger Bands
    "VWAP",                  # Volume Weighted Average Price
    "ATR"                    # Average True Range
  ],
  "exchange": "NSE_EQ"
}
```

**Supported Indicators:**
- **RSI** - Momentum oscillator (14 period default)
- **MACD** - Trend-following indicator
- **EMA_x** - Exponential Moving Average (e.g., EMA_20, EMA_50, EMA_200)
- **SMA_x** - Simple Moving Average (e.g., SMA_50, SMA_200)
- **BBANDS** - Bollinger Bands (volatility)
- **VWAP** - Volume Weighted Average Price
- **ATR** - Average True Range (volatility)

**Returns:**
- Price data
- Calculated indicators
- Detected candlestick patterns
- Trend context (Bullish/Bearish/Sideways)
- Support and resistance levels

---

## 🏗️ Architecture

```
┌─────────────────┐
│   AI Agent      │  (Claude Desktop, Cursor, etc.)
│  (Claude/GPT)   │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│   FastMCP       │  (MCP Server Framework)
│   Server        │
└────────┬────────┘
         │
         │ Python Functions
         │
┌────────▼────────┐
│   Upstox API    │  (Read-Only Access)
│   Client        │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│   Upstox        │  (Live Market Data)
│   Backend       │
└─────────────────┘
```

---

## 📊 Technical Stack

- **Framework**: FastMCP (Model Context Protocol)
- **API Client**: Upstox Python SDK
- **Technical Analysis**: pandas-ta
- **Web Server**: Uvicorn (for HTTP mode)
- **Containerization**: Docker, Docker Compose

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Invalid token" Error
**Problem**: Access token expired (tokens are valid for 24 hours)

**Solution**:
```bash
# Generate new token from Upstox
# Update .env file with new token
# Restart the MCP server
```

#### 2. "Command not found: upstox-mcp"
**Problem**: Package not installed or not in PATH

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall package
pip install -e .
```

#### 3. Claude Desktop Not Detecting Server
**Problem**: Configuration file path or format issue

**Solution**:
- Verify config file location
- Check JSON syntax (use a JSON validator)
- Ensure absolute path to executable
- Restart Claude Desktop

#### 4. "No data returned" for Intraday Candles
**Problem**: Market closed or no recent trading activity

**Solution**:
- Check if market is open (9:15 AM - 3:30 PM IST, Mon-Fri)
- Try a different interval
- Verify symbol is correct

#### 5. Rate Limiting
**Problem**: Too many API calls in short time

**Solution**:
- Add delays between requests
- Implement caching (future enhancement)
- Use batch queries when possible

---

## 🚧 Limitations

1. **Token Expiry**: Access tokens expire every 24 hours and need manual refresh
2. **Read-Only**: Cannot place trades (by design for safety)
3. **API Rate Limits**: Subject to Upstox API rate limiting
4. **Market Hours**: Live data only available during trading hours
5. **Historical Data**: Limited by Upstox API data retention policies

---

## 🗺️ Roadmap

### Version 1.1 (Done)
- [x] Caching layer for improved performance
- [x] Basic candlestick pattern detection

### Version 2.0 (Done) 🚀
- [x] **Granular Technical Indicators**: 10+ new specialized TA tools
- [x] **Namespaced Tools**: Logical grouping (`market_`, `analysis_`, `account_`)
- [x] **Historical Data**: Custom timeframe retrieval
- [x] **Instrument Search**: Find symbols by name
- [x] **JSON-Safe Response Schema**: Robust serialization for all agents
- [x] **Order & Trade Tracking**: Real-time access to daily activity

### Version 2.1 (Done) 🚀
- [x] **BYOK Support**: Pass credentials via HTTP headers
- [x] **Multi-User Support**: Secure architecture for shared deployments
- [x] **Dynamic Instructions**: Interactive landing page with setup guides

### Version 3.0 (Planned)
- [ ] Automatic token refresh mechanism
- [ ] Database integration for long-term historical tracking
- [ ] Portfolio performance analytics
- [ ] Alert system
- [ ] Machine learning predictions

### Version 3.0 (Vision)
- [ ] Machine learning predictions
- [ ] Strategy builder
- [ ] Social trading features
- [ ] Mobile app integration

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/ravikant1918/mcp-server-upstox.git

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
flake8 .
```

---

## 🗺️ Roadmap

### Q1 2026: Foundation & Core Analysis (Current)
- [x] Initial MCP implementation for Upstox
- [x] Comprehensive technical indicator tools
- [x] Bring Your Own Key (BYOK) support for remote deployments
- [x] Dynamic JSON configuration generator

### Q2 2026: Advanced Insights
- [ ] Sector-wise market analysis tools
- [ ] Option Chain analysis (Greeks calculation)
- [ ] Corporate actions tracking (Dividends, Splits)
- [ ] Multi-instrument correlation analysis

### Q3 2026: Ecosystem Expansion
- [ ] Integrated Backtesting engine wrapper
- [ ] Webhook support for real-time alerts
- [ ] Native support for more MCP clients (e.g., Goose, Windsurf)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙌 Credits & Acknowledgments

- **FastMCP** - MCP server framework
- **Upstox** - Trading API and market data
- **pandas-ta** - Technical analysis indicators
- **Anthropic** - Claude AI and MCP protocol

---

## 📬 Disclaimer

**IMPORTANT**: This project is not affiliated with, endorsed by, or sponsored by Upstox. 

**Trading Disclaimer**: 
- Trading in stocks involves substantial risk of loss
- This tool is for informational and educational purposes only
- Not financial advice - consult a licensed financial advisor
- Past performance does not guarantee future results
- The developers are not responsible for any trading losses
- Always do your own research before making investment decisions

**API Usage**: 
- Ensure compliance with Upstox API terms of service
- Respect API rate limits
- Use responsibly and ethically

---

## 📞 Support

### Documentation
- [Upstox API Docs](https://upstox.com/developer/api-documentation)
- [MCP Protocol Spec](https://modelcontextprotocol.io)
- [FastMCP Guide](https://github.com/jlowin/fastmcp)

### Get Help
- **Issues**: [GitHub Issues](https://github.com/ravikant1918/mcp-server-upstox/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ravikant1918/mcp-server-upstox/discussions)
- **Email**: developerrk1918@gmail.com

### Community
- Star ⭐ this repo if you find it useful
- Share with fellow traders
- Report bugs and suggest features
- Contribute code or documentation

---

## 🎯 Quick Start Summary

```bash
# 1. Clone and install
git clone https://github.com/ravikant1918/mcp-server-upstox.git
cd mcp-server-upstox
pip install -e .

# 2. Configure
echo "UPSTOX_ACCESS_TOKEN=your_token" > .env

# 3. Run
upstox-mcp

# 4. Use with Claude
# Add to Claude Desktop config, restart, and start chatting!
```

---

**Made with ❤️ for Indian Traders**

*Happy Trading! 📈🚀*