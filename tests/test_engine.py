import sys
import types
import pytest

# Provide dummy binance module so TradingEngine can be imported without
# optional dependencies installed.
binance_stub = types.ModuleType("binance")
binance_stub.AsyncClient = object
binance_stub.BinanceSocketManager = object
sys.modules.setdefault("binance", binance_stub)

from supertrader.trading.engine import TradingEngine, Mode
from supertrader.trading.order import Order, Side, OrderType

class DummyClient:
    def __init__(self):
        self.kwargs = None
    async def create_order(self, **kwargs):
        self.kwargs = kwargs
    async def close_connection(self):
        pass

def test_place_market_order():
    engine = TradingEngine('k','s', risk_manager=None)
    engine.client = DummyClient()
    order = Order(symbol='BTCUSDT', side=Side.BUY, quantity=1, order_type=OrderType.MARKET)
    import asyncio
    asyncio.run(engine.place_order(order))
    assert engine.client.kwargs['type'] == 'MARKET'
    assert engine.client.kwargs['symbol'] == 'BTCUSDT'

class DenyAllRisk:
    def check_order(self, balance, order, market_price=None):
        return False

def test_risk_manager_blocks_order():
    engine = TradingEngine('k','s', risk_manager=DenyAllRisk())
    engine.client = DummyClient()
    order = Order(symbol='BTCUSDT', side=Side.BUY, quantity=1, order_type=OrderType.MARKET)
    import asyncio
    with pytest.raises(RuntimeError):
        asyncio.run(engine.place_order(order))
