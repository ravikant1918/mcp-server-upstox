import sys
import types

# Minimal fake fastmcp to allow importing and registering tools in tests
fastmcp = types.SimpleNamespace()

class DummyMCP:
    def __init__(self, name=None):
        self.name = name
    def tool(self, name=None):
        def decorator(fn):
            # simply return the function - registration not needed in tests
            return fn
        return decorator
    def custom_route(self, path, methods=None):
        def decorator(fn):
            return fn
        return decorator
    def run(self, *args, **kwargs):
        return None

fastmcp.FastMCP = DummyMCP
fastmcp.Context = object
sys.modules['fastmcp'] = fastmcp

# Minimal fake upstox_client SDK
upstox_client = types.SimpleNamespace()

class ApiException(Exception):
    pass

class Configuration:
    def __init__(self):
        self.access_token = None
        self.api_key = {}
        self.host = None

class ApiClient:
    def __init__(self, config):
        self.config = config

class BaseApi:
    def __init__(self, api_client=None):
        self.api_client = api_client

# Attach dummy APIs used in the adapter
upstox_client.Configuration = Configuration
upstox_client.ApiClient = ApiClient
upstox_client.HistoryApi = BaseApi
upstox_client.MarketQuoteApi = BaseApi
upstox_client.UserApi = BaseApi
upstox_client.PortfolioApi = BaseApi
upstox_client.OrderApi = BaseApi
upstox_client.rest = types.SimpleNamespace(ApiException=ApiException)

sys.modules['upstox_client'] = upstox_client
sys.modules['upstox_client.rest'] = upstox_client.rest
