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
                if pit_of_market2.magic.timestamp - pit_of_market1.might.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    break
                if pit_of_market2.might.timestamp - pit_of_market1.magic.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    break
                if pit_of_market1.might.timestamp - pit_of_market2.magic.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    continue
                if pit_of_market1.magic.timestamp - pit_of_market2.might.timestamp > ARBITRAGE_DELTA_TIME_IN_SECONDS:
                    continue

                selected_might = pit_of_market1.might if pit_of_market1.might.value > pit_of_market2.might.value \
                    else pit_of_market2.might
                selected_magic = pit_of_market1.magic if pit_of_market1.magic.value < pit_of_market2.magic.value \
                    else pit_of_market2.magic
                timestamps.append(mean([selected_might.timestamp, selected_magic.timestamp]))
                arbitrage.append(selected_might.value - selected_magic.value)

        pretty_timestamps = [timestamp - self.begin_time for timestamp in timestamps]
        plt.plot(pretty_timestamps, arbitrage)
        plt.axis([min(pretty_timestamps), max(pretty_timestamps), min(arbitrage), max(arbitrage)])
        print("timestamps[{0}] = {1}\narbi[{2}] = {3}".
              format(len(pretty_timestamps), pretty_timestamps, len(arbitrage), arbitrage))
        plt.show()

