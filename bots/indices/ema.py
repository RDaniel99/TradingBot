# https://www.investopedia.com/terms/e/ema.asp

import datetime
import bots.indices.sma
from bots.utils.utils import get_list_of_prices_for_given_interval

smoothing = 2
EMA_200 = 200
EMA_50 = 50
EMA_10 = 10
EMA_12 = 12
EMA_26 = 26


def compute_12(ticker, start_date, end_date):
    return compute(ticker, start_date, end_date, EMA_12)


def compute_26(ticker, start_date, end_date):
    return compute(ticker, start_date, end_date, EMA_26)


def compute_10(ticker, start_date, end_date):
    return compute(ticker, start_date, end_date, EMA_10)


def compute_50(ticker, start_date, end_date):
    return compute(ticker, start_date, end_date, EMA_50)


def compute_200(ticker, start_date, end_date):
    return compute(ticker, start_date, end_date, EMA_200)


def compute(ticker, start_date, end_date, window_length):
    delta = datetime.timedelta(days=1)

    initial_prices = get_list_of_prices_for_given_interval(ticker, start_date, end_date)
    position = 0

    ema_previous_day = bots.indices.sma.compute(ticker, start_date, start_date, window_length)[0]

    ema = []
    alpha = smoothing / (1 + window_length)

    while start_date <= end_date:
        price = initial_prices[position]
        position += 1

        ema_today = ema_previous_day * (1 - alpha) + price * alpha

        ema.append(ema_today)
        ema_previous_day = ema_today

        start_date += delta

    return ema
