from plotter import *
from threading import Thread
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentError


def do_work(symbol1, symbol2):
    market1 = BittrexAPI(symbol1, VOLUME)
    market2 = BitfinexAPI(symbol2, VOLUME)

    # Generation of data
    begin_time = time.time()
    latest_time = time.time()
    while latest_time - begin_time < TIMEOUT_IN_SECONDS:
        latest_time = time.time()
        t1 = Thread(target=market1.pit)
        t2 = Thread(target=market2.pit)

        t1.start()
        t2.start()
        t1.join()
        t2.join()
        time.sleep(1.5)

    # Plotting the data
    plotter = Plotter(market1, market2, begin_time)
    print("About to plot with {plotter}".format(plotter=plotter))
    plotter.plot_arbitrage_on_both_markets()


def main():
    arg_parser = ArgumentParser(usage="%(prog)s symbol1 symbol2", formatter_class=RawTextHelpFormatter,
                                description="""
Presets: \n\tUSDT-BTC btcusd\n\tUSDT-LTC ltcusd\n\tUSDT-XRP xrpusd""")

    arg_parser.add_argument('symbols', type=str, nargs=2, help='symbol1 symbol2')

    params = arg_parser.parse_args()

    if len(params.symbols) != 2:
        raise ArgumentError("Insert 2 symbols")

    do_work(*params.symbols)


if __name__ == '__main__':
    main()
