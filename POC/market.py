import random
from utils import *
from markets import *

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


class Market1(Market):
    def __init__(self, volume):
        Market.__init__(self, "USDT-BTC", volume)

    def median_highest_buy(self):
        _median_highest_buy = median_highest_buy(quantity=self.volume, market=self.market_id)

        return MMTuple(1.0025 * _median_highest_buy[0], _median_highest_buy[1])

    def median_lowest_sell(self):
        _median_lowest_sell = median_lowest_sell(quantity=self.volume, market=self.market_id)
        return MMTuple(0.9975 * _median_lowest_sell[0], _median_lowest_sell[1])

class Market2(Market):
    def __init__(self, volume):
        Market.__init__(self, "USDT-LTC", volume)

    def median_highest_buy(self):
        _median_highest_buy = median_highest_buy(quantity=self.volume, market=self.market_id)

        return MMTuple(1.0025 * _median_highest_buy[0], _median_highest_buy[1])

    def median_lowest_sell(self):
        _median_lowest_sell = median_lowest_sell(quantity=self.volume, market=self.market_id)
        return MMTuple(0.9975 * _median_lowest_sell[0], _median_lowest_sell[1])