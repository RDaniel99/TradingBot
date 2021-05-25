# https://www.investopedia.com/terms/r/rsi.asp

import datetime
from statistics import mean

from bots.utils.utils import get_list_of_prices_for_given_interval

RSI_14 = 14


def get_percentage(previous_price, current_price):
    return 100 * current_price / previous_price - 100


def compute_14(ticker, start_date, end_date):
    return compute(ticker, start_date, end_date, RSI_14)


def compute(ticker, start_date, end_date, window_length):
    delta = datetime.timedelta(days=1)
    delta_beginning_of_period = datetime.timedelta(days=window_length)

    beginning_date = start_date - delta_beginning_of_period

    initial_prices = get_list_of_prices_for_given_interval(ticker, beginning_date, end_date)
    position = 0
    prices = []
    gains = []
    losses = []

    while beginning_date <= start_date:
        if position > 0:
            percentage = get_percentage(initial_prices[position - 1], initial_prices[position])

            if percentage > 0:
                gains.append(percentage)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-percentage)

        prices.append(initial_prices[position])
        beginning_date += delta
        position += 1

    rsi = []

    mean_gain = mean(gains)
    mean_loss = mean(losses)

    rsi.append(100 - 100 / (1 + mean_gain / mean_loss))

    start_date += delta

    while start_date <= end_date:
        prices = prices[1:]

        prices.append(initial_prices[position])
        position += 1

        percentage = get_percentage(prices[window_length - 1], prices[window_length])

        mean_gain = (window_length - 1) * mean_gain + max(0, percentage)
        mean_loss = (window_length - 1) * mean_loss + max(0, -percentage)

        mean_gain /= window_length
        mean_loss /= window_length

        rsi.append(100 - 100 / (1 + mean_gain / mean_loss))

        start_date += delta

    return rsi
