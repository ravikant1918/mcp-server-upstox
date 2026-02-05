import argparse
from upstock_mcp.server import mcp

def main():
    parser = argparse.ArgumentParser(
        prog="upstox-mcp",
        description="Upstox MCP Server"
    )

    parser.add_argument(
        "serve",
        nargs="?",
        default="serve",
        help="Run the MCP server (default command)"
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport type (default: stdio)"
    )

    parser.add_argument("--host", default="127.0.0.1", help="Host for HTTP/SSE (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP/SSE (default: 8000)")
    parser.add_argument("--version", action="version", version="upstox-mcp 2.2.0")

    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "http":
        mcp.run(transport="http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)

if __name__ == "__main__":
    main()
