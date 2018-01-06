import random
from utils import *
from bittrex.bittrex import Bittrex, API_V2_0
import requests
import time
import statistics
from collections import namedtuple

MarketPIT = namedtuple("MarketPIT", "id median_highest_buy median_lowest_sell")
MMTuple = namedtuple("MMTuple", "value timestamp")


class Market:
    def __init__(self, market_id, volume):
        self.market_id = market_id
        self.volume = volume
        self.pits = []

    def __repr__(self):
        return "Market({0})".format(self.market_id)

    def median_highest_buy(self):  # might
        raise NotImplementedError("API for people who want to buy")

    def median_highest_buy_commision(self, mula):
        raise NotImplementedError("nir is gay")

    def median_lowest_sell(self):  # magic
        raise NotImplementedError("API for people who want to sell")

    def median_lowest_sell_commision(self, mula):
        raise NotImplementedError("nir is gay")

    def pit(self):
        self.pits.append(MarketPIT(self.market_id, self.median_highest_buy(), self.median_lowest_sell()))


class MockupMarket(Market):
    def __init__(self, market_id, volume):
        Market.__init__(self, market_id, volume)

    def median_highest_buy(self):
        return MMTuple((random.uniform(1, 30)), time.time())

    def median_highest_buy_commision(self, mula):
        pass

    def median_lowest_sell(self):
        return MMTuple((random.uniform(1, 30)), time.time())

    def median_lowest_sell_commision(self, mula):
        pass


class BittrexAPI(Market):
    BUY = 'buy'
    SELL = 'sell'

    def __init__(self, volume):
        Market.__init__(self, "USDT-BTC", volume)
        self.my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)


    def median_highest_buy(self):
        return self.median_lowest(quantity=self.volume, op=self.SELL, market=self.market_id)

    def median_highest_buy_commision(self, mula):
        return 1.0025 * mula

    def median_lowest_sell(self):
        return self.median_lowest(quantity=self.volume, op=self.BUY, market=self.market_id)

    def median_lowest_sell_commision(self, mula):
        return 0.9975 * mula

    def median_lowest(self, quantity, op, market):
        ts = time.time()
        order_book = self.my_bittrex.get_orderbook(market=market)

        assert order_book['success'], "Failed retrieving order book"

        order_book['result'][op].sort(key=lambda x: x['Rate'], reverse=(op == 'buy'))

        to_med = []
        total = 0

        for order in order_book['result'][op]:
            to_med.append(order['Rate'])
            total += order['Quantity']
            if total >= quantity:
                break

        median = statistics.median(to_med)
        print("Median Rate: {}, Total Quantity: {}".format(median, total))
        ts2 = time.time()
        print("Time Took: {}".format(ts2 - ts))
        median_after_commision = self.median_highest_buy_commision(median) if op == self.SELL else\
            self.median_lowest_sell_commision(median)
        return MMTuple(median_after_commision, (ts + ts2) / 2)


class BitfinexAPI(Market):
    BUY = "asks"
    SELL = "bids"

    def __init__(self, volume):
        Market.__init__(self, "btcusd", volume)

    def median_highest_buy(self):

        _median_highest_buy = self.median_highest(op=self.SELL, volume=self.volume, market_id=self.market_id)
        return MMTuple(1.0025 * _median_highest_buy[0], _median_highest_buy[1])

    def median_lowest_sell(self):
        _median_lowest_sell = median_highest(op=self.BUY, quantity=self.volume, market=self.market_id)
        return MMTuple(0.9975 * _median_lowest_sell[0], _median_lowest_sell[1])

    def median_highest_buy_commision(self, mula):
        return 1.002 * mula

    def median_lowest_sell_commision(self, mula):
        return 0.99 * mula

    def median_lowest(self, op, volume, market_id):
        ts = time.time()
        order_book = requests.get("https://api.bitfinex.com/v1/book/{0}".format(market_id))

        assert order_book.status_code == 200, "Failed retrieving order book"

        order_book[op].sort(key=lambda x: x['price'], reverse=(op == 'bids'))

        to_med = []
        total = 0

        for order in order_book[op]:
            to_med.append(order['price'])
            total += order['amount']
            if total >= volume:
                break

        median = statistics.median(to_med)
        print("Median Rate: {}, Total Quantity: {}".format(median, total))
        ts2 = time.time()
        print("Time Took: {}".format(ts2 - ts))

        median_after_commision = self.median_highest_buy_commision(median) if op == self.SELL else \
            self.median_lowest_sell_commision(median)
        return MMTuple(median_after_commision, (ts + ts2) / 2)
