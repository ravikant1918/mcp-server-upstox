# Upstox MCP Server 📈

A **Model Context Protocol (MCP)** server that integrates with the **Upstox Trading API**, enabling AI agents like Claude to securely access Indian stock market data, perform technical analysis, and view account information in **read-only mode**.

---

## 🚀 Features

### 📊 Market Data
- **Live quotes** - Last Traded Price (LTP), OHLC, Volume
- **Intraday candles** - 1min, 3min, 5min, 10min, 15min, 30min intervals
- **Historical data** - Daily, weekly, monthly candles
- **NSE & BSE** - Support for both exchanges

### 📈 Technical Analysis
- **Momentum Indicators** - RSI, MACD
- **Trend Indicators** - EMA, SMA, VWAP
- **Volatility Indicators** - Bollinger Bands, ATR
- **Candlestick Patterns** - Doji, Hammer, Engulfing, and more
- **Smart Context** - Trend direction, strength, bias summary
- **Support & Resistance** - Automatically calculated levels

### 👤 Account Management (Read-Only)
- **Profile details** - User information
- **Funds summary** - Available margin, used margin
- **Holdings** - Long-term equity positions with P&L
- **Positions** - Active intraday/short-term trades
- **Portfolio overview** - Total exposure, investment value

### 🤖 MCP Native
- **AI-First Design** - Built specifically for AI agents
- **Tool-Based Architecture** - Natural language to API calls
- **Multi-Agent Support** - Works with Claude, Cursor, custom agents
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

### Remote MCP (via mcp-remote)

For running the server remotely or in a separate process:

```json
{
  "mcpServers": {
    "Upstox-HTTP": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://127.0.0.1:8000/mcp"
      ],
      "env": {
        "UPSTOX_API_KEY": "YOUR_API_KEY",
        "UPSTOX_API_SECRET": "YOUR_API_SECRET",
        "UPSTOX_ACCESS_TOKEN": "YOUR_ACCESS_TOKEN"
      }
    }
  }
}
```

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

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `get_live_quote` | Live price, OHLC, volume | `symbol`, `exchange` |
| `get_intraday_candles` | Intraday OHLCV data | `symbol`, `interval`, `exchange` |
| `get_historical_candles` | Historical market data | `symbol`, `interval`, `from_date`, `to_date` |
| `get_technical_analysis` | Multi-indicator analysis | `symbol`, `interval`, `indicators`, `exchange` |
| `get_account_summary` | Funds + portfolio overview | None |
| `get_holdings_list` | All equity holdings | None |
| `get_positions_list` | Active positions | None |

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

### Version 1.1 (Planned)
- [ ] Automatic token refresh mechanism
- [ ] Caching layer for improved performance
- [ ] More candlestick pattern detection
- [ ] Custom indicator support

### Version 2.0 (Future)
- [ ] Database integration for historical tracking
- [ ] Portfolio performance analytics
- [ ] Backtesting framework
- [ ] Alert system
- [ ] Multi-user support

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