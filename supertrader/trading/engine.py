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
    def __init__(self, api_key: str, api_secret: str, mode: Mode = Mode.LIVE):
        self.api_key = api_key
        self.api_secret = api_secret
        self.mode = mode
        self.client: AsyncClient | None = None

    async def connect(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret, testnet=self.mode==Mode.PAPER)

    async def close(self):
        if self.client:
            await self.client.close_connection()

    async def place_order(self, order: Order):
        if not self.client:
            raise RuntimeError("Client not connected")
        if order.order_type == order.order_type.MARKET:
            await self.client.create_order(symbol=order.symbol, side=order.side.value,
                                           type=order.order_type.value, quantity=order.quantity)
        else:
            await self.client.create_order(symbol=order.symbol, side=order.side.value,
                                           type=order.order_type.value, quantity=order.quantity,
                                           price=order.price, stopPrice=order.stop_price)

    async def run(self, symbols: List[str]):
        if not self.client:
            await self.connect()
        bm = BinanceSocketManager(self.client)
        streams = [bm.symbol_ticker_socket(symbol.lower()) for symbol in symbols]
        async with asyncio.TaskGroup() as tg:
            for stream in streams:
                tg.create_task(self.process_stream(stream))

    async def process_stream(self, stream):
        async with stream as s:
            async for msg in s:
                print(msg)
