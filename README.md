# Upstox MCP Server

A Model Context Protocol (MCP) server for the Upstox API.

## Features

- **Market Data**: Live quotes, intraday candles (1m-30m), historical candles.
- **Technical Analysis**: Built-in Pandas-TA integration (RSI, EMA, MACD, etc).
- **Account**: Read-only access to funds, holdings, positions.
- **Transports**: HTTP/SSE (FastAPI) and Standard IO.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -e .
   ```
   *Or manually: `pip install fastapi uvicorn pandas pandas-ta upstox-python-sdk mcp`*

2. **Credentials**:
   Create a `.env` file:
   ```env
   UPSTOX_ACCESS_TOKEN=your_token_here
   ```

## Running the Server

FastMCP automatically supports both Standard IO and SSE transports.

### Option A: Standard IO (Default)
Best for Claude Desktop or command-line usage.

```bash
python upstock_mcp/server.py
```

### Option B: SSE (HTTP Streamable)
Recommended for web deployments or remote clients.

```bash
fastmcp run upstock_mcp/server.py
```
*Note: This starts the server on `http://localhost:8000/sse` by default.*

### Option C: Claude Desktop Config
Config path: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "upstock": {
      "command": "python3",
      "args": ["/absolute/path/to/upstock-mcp/upstock_mcp/server.py"],
      "env": {
        "UPSTOX_ACCESS_TOKEN": "your_token"
      }
    }
  }
}
```
