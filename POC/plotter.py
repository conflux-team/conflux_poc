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
        arbitrage = []
        for pit_of_market1 in self.market1.pits:
            for pit_of_market2 in self.market2.pits:
                if pit_of_market2.median_lowest_sell.timestamp - pit_of_market1.median_highest_buy.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    break
                if pit_of_market2.median_highest_buy.timestamp - pit_of_market1.median_lowest_sell.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    break
                if pit_of_market1.median_highest_buy.timestamp - pit_of_market2.median_lowest_sell.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    continue
                if pit_of_market1.median_lowest_sell.timestamp - pit_of_market2.median_highest_buy.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    continue

                selected_median_highest_buy = pit_of_market1.median_highest_buy if pit_of_market1.median_highest_buy.value > pit_of_market2.median_highest_buy.value \
                    else pit_of_market2.median_highest_buy
                selected_median_lowest_sell = pit_of_market1.median_lowest_sell if pit_of_market1.median_lowest_sell.value < pit_of_market2.median_lowest_sell.value \
                    else pit_of_market2.median_lowest_sell
                timestamps.append(mean([selected_median_highest_buy.timestamp, selected_median_lowest_sell.timestamp]))
                arbitrage.append(selected_median_highest_buy.value - selected_median_lowest_sell.value)

        pretty_timestamps = timestamps
        plt.plot(pretty_timestamps, arbitrage)
        print("timestamps[{0}] = {1}\narbi[{2}] = {3}".
              format(len(pretty_timestamps), pretty_timestamps, len(arbitrage), arbitrage))

        plt.axis([min(pretty_timestamps), max(pretty_timestamps), min(arbitrage), max(arbitrage)])
        plt.show()

