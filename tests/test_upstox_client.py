import pytest
from unittest.mock import patch
import logging
import asyncio

from upstock_mcp.adapters.upstox_client import UpstoxClient
from upstox_client.rest import ApiException


def test_get_profile_logs_exception_and_raises(caplog):
    client = UpstoxClient()

    async def raise_api(*args, **kwargs):
        raise ApiException("boom")

    # Ensure the attribute exists so the attribute lookup happens without error
    client.user_api.get_profile = lambda *args, **kwargs: None

    # Patch the _run_sync to simulate ApiException
    with patch.object(UpstoxClient, "_run_sync", side_effect=raise_api):
        caplog.set_level(logging.ERROR)
        with pytest.raises(ApiException):
            asyncio.run(client.get_profile())
        assert "Upstox API Error (get_profile)" in caplog.text
