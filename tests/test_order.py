from supertrader.trading.order import Order, Side, OrderType, RiskManager


def test_risk_manager_allows_small_order():
    rm = RiskManager(0.1)
    order = Order(symbol="BTCUSDT", side=Side.BUY, quantity=0.1, order_type=OrderType.MARKET, price=100)
    assert rm.check_order(1000, order)


def test_risk_manager_blocks_large_order():
    rm = RiskManager(0.1)
    order = Order(symbol="BTCUSDT", side=Side.BUY, quantity=2, order_type=OrderType.MARKET, price=1000)
    assert not rm.check_order(1000, order)
