from plotter import *


# market1 = MockupMarket("Market1", VOLUME)
# market2 = MockupMarket("Market2", VOLUME)

market1 = BittrexAPI(VOLUME)
market2 = Market2(VOLUME)




# Generation of data
begin_time = time.time()
latest_time = time.time()
while latest_time - begin_time < TIMEOUT_IN_SECONDS:
    latest_time = time.time()
    market1.pit()
    market2.pit()


# Plotting the data
plotter = Plotter(market1, market2, begin_time)
print("About to plot with {plotter}".format(plotter=plotter))
plotter.plot_arbitrage_on_both_markets()