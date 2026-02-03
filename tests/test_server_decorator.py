import logging
import asyncio

from upstock_mcp.server import mcp_wrapped_tool


def test_mcp_wrapped_tool_logs_and_returns_error(caplog):
    @mcp_wrapped_tool(name="test_tool", error_type="TestError")
    async def failing():
        raise RuntimeError("kaboom")

    caplog.set_level(logging.ERROR)
    resp = asyncio.run(failing())

    assert isinstance(resp, dict)
    assert resp.get("success") is False
    assert resp.get("error") and resp["error"]["type"] == "TestError"
    assert "Unhandled error in tool test_tool" in caplog.text
