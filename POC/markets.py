import statistics
import time
from bittrex.bittrex import Bittrex, API_V2_0
from collections import namedtuple
MMTuple = namedtuple("MMTuple", "value timestamp")


BUY = 'buy'
SELL = 'sell'


my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)


def get_markets():
    markets = my_bittrex.get_markets()
    assert markets['success'], "Failed retrieving markets"
    return [market['MarketName'] for market in markets['result']]


def median_lowest_sell(quantity, market='USDT-BTC'):
    return median_lowest(quantity=quantity, op=SELL, market=market)


def median_highest_buy(quantity, market='USDT-BTC'):
    return median_lowest(quantity=quantity, op=BUY, market=market)


def median_lowest(quantity, op, market='USDT-BTC'):
    ts = time.time()
    order_book = my_bittrex.get_orderbook(market=market)

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

    return median, (ts+ts2)/2