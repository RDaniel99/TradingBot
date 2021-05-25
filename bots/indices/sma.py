# https://www.investopedia.com/terms/s/sma.asp

import datetime
from statistics import mean
from bots.utils.utils import get_list_of_prices_for_given_interval


SMA_10 = 10


def compute_10(ticker, start_date, end_date):
    return compute(ticker, start_date, end_date, SMA_10)


def compute(ticker, start_date, end_date, window_length):
    delta = datetime.timedelta(days=1)
    delta_beginning_of_period = datetime.timedelta(days=window_length - 1)

    beginning_date = start_date - delta_beginning_of_period

    initial_prices = get_list_of_prices_for_given_interval(ticker, beginning_date, end_date)
    position = 0
    prices = []

    while beginning_date <= start_date:
        prices.append(initial_prices[position])
        beginning_date += delta
        position += 1

    sma = [mean(prices)]

    start_date += delta

    while start_date <= end_date:
        prices = prices[1:]
        prices.append(initial_prices[position])
        position += 1

        sma.append(mean(prices))
        start_date += delta

    return sma
