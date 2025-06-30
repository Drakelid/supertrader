from supertrader.trading.order import Order, Side, OrderType, RiskManager


def test_risk_manager_allows_small_order():
    rm = RiskManager(0.1)
    order = Order(symbol="BTCUSDT", side=Side.BUY, quantity=0.1, order_type=OrderType.MARKET)
    assert rm.check_order(1000, order, market_price=100)


def test_risk_manager_blocks_large_order():
    rm = RiskManager(0.1)
    order = Order(symbol="BTCUSDT", side=Side.BUY, quantity=2, order_type=OrderType.MARKET)
    assert not rm.check_order(1000, order, market_price=1000)


def test_risk_manager_from_env(monkeypatch):
    monkeypatch.setenv("MAX_RISK_PCT", "0.2")
    rm = RiskManager.from_env()
    order = Order(symbol="BTCUSDT", side=Side.BUY, quantity=1, order_type=OrderType.MARKET)
    assert rm.check_order(1000, order, market_price=100)
