from typing import List

from evestidor_event_stream import EventStream
from src.domain import Price


class Publisher:

    def __init__(self):
        self._queue = EventStream(host='evestidor-event-stream')

    def publish_prices(self, *prices: List[Price]):
        for price in prices:
            self.publish_price(price)

    def publish_price(self, price: Price):
        self._queue.send(
            exchange_name='stock_prices',
            routing_key='stock.prices.update',
            data={
                'symbol': price.symbol,
                'date': price.created.strftime('%Y-%m-%d'),
                'price': price.amount,
            }
        )
