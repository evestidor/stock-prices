import logging
import time

from src.bovespa import B3Facade
from src.publisher import Publisher

logging.basicConfig(level=logging.INFO)
pika_logger = logging.getLogger('pika')
pika_logger.setLevel(logging.CRITICAL)


class LoggedPublisher(Publisher):

    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger('Publisher')
        self._logger_templates = {
            'new_price': '[{created}] {symbol} - {amount}'
        }

    def publish_price(self, price):
        super().publish_price(price)
        message = self._logger_templates['new_price'].format(**vars(price))
        self._logger.info(message)


def main():
    symbols = B3Facade.list_symbols()
    publisher = LoggedPublisher()
    interval = 3600  # 1 hour

    while True:
        prices = B3Facade.list_prices(*symbols)
        publisher.publish_prices(*prices)
        time.sleep(interval)


main()
