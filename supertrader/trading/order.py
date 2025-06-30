from dataclasses import dataclass
from enum import Enum
from typing import Optional

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class Order:
    symbol: str
    side: Side
    quantity: float
    order_type: OrderType
    price: Optional[float] = None
    stop_price: Optional[float] = None

class RiskManager:
    def __init__(self, max_risk_pct: float):
        self.max_risk_pct = max_risk_pct

    def check_order(self, balance: float, order: Order) -> bool:
        max_allowed = balance * self.max_risk_pct
        # simple check based on quantity*price if provided
        est_cost = order.quantity * (order.price or 0)
        return est_cost <= max_allowed
