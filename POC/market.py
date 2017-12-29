from collections import namedtuple
import random
from utils import *

MarketPIT = namedtuple("MarketPIT", "id might magic")
MMTuple = namedtuple("MMTuple", "value timestamp")


class Market:
    def __init__(self, market_id, volume):
        self.market_id = market_id
        self.volume = volume
        self.pits = []

    def __repr__(self):
        return "Market({0})".format(self.market_id)

    def might(self):
        raise NotImplementedError("API for people who want to buy")

    def might_commision(self, mula):
        raise NotImplementedError("nir is gay")

    def magic(self):
        raise NotImplementedError("API for people who want to sell")

    def magic_commision(self, mula):
        raise NotImplementedError("nir is gay")

    def pit(self):
        self.pits.append(MarketPIT(self.market_id, self.might(), self.magic()))


class MockupMarket(Market):
    def __init__(self, market_id, volume):
        Market.__init__(self, market_id, volume)

    def might(self):
        return MMTuple((random.uniform(1, 30)), time.time())

    def magic(self):
        return MMTuple((random.uniform(1, 30)), time.time())

