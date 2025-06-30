"""Asynchronous trading engine for Binance."""

import asyncio
from enum import Enum
from typing import List

from binance import AsyncClient, BinanceSocketManager

from .order import Order

class Mode(Enum):
    LIVE = "live"
    PAPER = "paper"
    BACKTEST = "backtest"

class TradingEngine:
    """Manage websocket connections and order placement."""

    def __init__(self, api_key: str, api_secret: str, mode: Mode = Mode.LIVE, *, risk_manager=None) -> None:
        """Create engine.

        Parameters
        ----------
        api_key, api_secret:
            Binance credentials.
        mode:
            Trading mode.
        risk_manager:
            Optional ``RiskManager`` for position sizing.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.mode = mode
        self.client: AsyncClient | None = None
        self.risk_manager = risk_manager

    async def connect(self) -> None:
        self.client = await AsyncClient.create(self.api_key, self.api_secret, testnet=self.mode==Mode.PAPER)

    async def close(self) -> None:
        if self.client:
            await self.client.close_connection()

    async def place_order(self, order: Order) -> None:
        if not self.client:
            raise RuntimeError("Client not connected")
        if self.risk_manager and not self.risk_manager.check_order(0, order):
            raise RuntimeError("Order violates risk limits")
        if order.order_type == order.order_type.MARKET:
            await self.client.create_order(symbol=order.symbol, side=order.side.value,
                                           type=order.order_type.value, quantity=order.quantity)
        else:
            await self.client.create_order(symbol=order.symbol, side=order.side.value,
                                           type=order.order_type.value, quantity=order.quantity,
                                           price=order.price, stopPrice=order.stop_price)

    async def run(self, symbols: List[str]) -> None:
        if not self.client:
            await self.connect()
        bm = BinanceSocketManager(self.client)
        streams = [bm.symbol_ticker_socket(symbol.lower()) for symbol in symbols]
        async with asyncio.TaskGroup() as tg:
            for stream in streams:
                tg.create_task(self.process_stream(stream))

    async def process_stream(self, stream) -> None:
        async with stream as s:
            async for msg in s:
                print(msg)
