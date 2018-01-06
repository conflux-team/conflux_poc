from market import *
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, market1, market2, begin_time):
        self.market1 = market1
        self.market2 = market2
        self.begin_time = begin_time

    def __repr__(self):
        return "Plotter[Market1({market_1_len}), Market2({market_2_len})]".\
            format(market_1_len=len(self.market1.pits), market_2_len=len(self.market2.pits))

    def plot_arbitrage_on_both_markets(self):
        timestamps = []
        arbitrages = []
        for pit_of_market1 in self.market1.pits:
            filt1 = list(filter(lambda x: abs(pit_of_market1.median_highest_buy.timestamp - x.median_lowest_sell.timestamp) < ARBITRAGE_DELTA_TIME_IN_SECONDS, self.market2.pits))
            filt2 = list(filter(lambda x: abs(pit_of_market1.median_lowest_sell.timestamp - x.median_highest_buy.timestamp) < ARBITRAGE_DELTA_TIME_IN_SECONDS, self.market2.pits))

            if not filt1 and not filt2:
                continue
            if not filt1:
                filt1 = [MarketPIT(-1, 0, MMTuple(MAX_PRICE_IN_SHMEKELS, -1))]
            if not filt2:
                filt2 = [MarketPIT(-1, MMTuple(MIN_PRICE_IN_SHMEKELS, -1), -1)]

            min_of_sellers = list(sorted(filt1, key=lambda x: x.median_lowest_sell.value))[0]
            max_of_buyers = list(sorted(filt2, key=lambda x: x.median_highest_buy.value, reverse=True))[0]

            if pit_of_market1.median_highest_buy.value - min_of_sellers.median_lowest_sell.value > \
                max_of_buyers.median_highest_buy.value - pit_of_market1.median_lowest_sell.value:
                timestamp = mean([pit_of_market1.median_highest_buy.timestamp, min_of_sellers.median_lowest_sell.timestamp])
                arbitrage = pit_of_market1.median_highest_buy.value - min_of_sellers.median_lowest_sell.value
                self.market2.pits.remove(min_of_sellers)

            else:
                timestamp = mean([pit_of_market1.median_lowest_sell.timestamp, max_of_buyers.median_highest_buy.timestamp])
                arbitrage = max_of_buyers.median_highest_buy.value - pit_of_market1.median_lowest_sell.value
                self.market2.pits.remove(max_of_buyers)

            timestamps.append(timestamp)
            arbitrages.append(arbitrage)

        pretty_timestamps = [timestamp - self.begin_time for timestamp in timestamps]

        print(pretty_timestamps)
        print()
        print(arbitrages)

        plt.plot(pretty_timestamps, arbitrages)

        plt.axis([min(pretty_timestamps) - 5, max(pretty_timestamps) + 5, min(arbitrages), max(arbitrages)])
        plt.show()

