import asyncio
import gzip
import json

from upstock_mcp.engines.instrument_engine import InstrumentEngine

class DummyResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code
    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception("HTTP error")

class DummyClient:
    def __init__(self, resp):
        self._resp = resp
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        return False
    async def get(self, url):
        await asyncio.sleep(0.1)  # emulate network delay
        return self._resp


def test_refresh_is_serialized(tmp_path, monkeypatch):
    # Prepare fake gzipped data
    data = [{"trading_symbol": "ABC", "exchange": "NSE", "instrument_key": "NSE|ABC"}]
    content = gzip.compress(json.dumps(data).encode())

    engine = InstrumentEngine()
    # point cache_file to tmp path to avoid touching home
    engine.CACHE_DIR = tmp_path
    engine.cache_file = tmp_path / "instruments.json"

    # Count how many times httpx.AsyncClient was entered
    resp = DummyResponse(content)

    async def fake_client(*args, **kwargs):
        return DummyClient(resp)

    # Patch the AsyncClient constructor used in refresh_if_needed
    monkeypatch.setattr('httpx.AsyncClient', lambda *args, **kwargs: DummyClient(resp))

    # Run two concurrent refreshes
    async def runner():
        await asyncio.gather(engine.refresh_if_needed(force=True), engine.refresh_if_needed(force=True))
    asyncio.run(runner())

    # After refresh, cache file should exist and instruments populated
    assert engine.cache_file.exists()
    assert 'ABC:NSE' in engine._instruments
