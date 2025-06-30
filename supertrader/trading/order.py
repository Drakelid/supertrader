"""Order primitives and risk management utilities."""

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
    """Simple position sizing checker."""

    def __init__(self, max_risk_pct: float) -> None:
        self.max_risk_pct = max_risk_pct

    @classmethod
    def from_env(cls) -> "RiskManager":
        """Instantiate using the ``MAX_RISK_PCT`` environment variable."""
        import os

        pct = float(os.getenv("MAX_RISK_PCT", "0.1"))
        return cls(pct)

    def check_order(self, balance: float, order: Order, market_price: Optional[float] = None) -> bool:
        """Return True if the order cost is within allowed risk.

        Parameters
        ----------
        balance:
            Current account equity.
        order:
            The order to evaluate.
        market_price:
            Last traded price used when ``order.price`` is not specified.
        """
        max_allowed = balance * self.max_risk_pct
        price = order.price if order.price is not None else (market_price or 0)
        est_cost = order.quantity * price
        return est_cost <= max_allowed
