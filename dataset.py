import pandas as pd
from pandas_datareader import data
from constants import stock_tickers
from copy import deepcopy
import datetime

cache = {}


def from_date_to_int(date):
    return 10000 * date.year + 100 * date.month + date.day


def get_data(ticker, start, end='today'):
    start_as_int = from_date_to_int(start)
    end_as_int = from_date_to_int(end)

    another_start = pd.to_datetime(start)
    another_end = pd.to_datetime(end)

    if cache.__contains__((ticker, start_as_int, end_as_int)):
        return cache[(ticker, start_as_int, end_as_int)]

    result = data.DataReader(ticker, 'yahoo', another_start, another_end)

    cache[(ticker, start_as_int, end_as_int)] = result
    return result


def fill_cache(ticker, price, start, end='today'):
    start_as_int = from_date_to_int(start)
    end_as_int = from_date_to_int(end)

    cache[(ticker, start_as_int, end_as_int)] = price


def get_data_for_given_day(ticker, day):
    return get_data(ticker, day, day)


def get_dates_list(start, end):
    return pd.date_range(start, end)


def get_price_for_ticker(ticker, day, at_beginning=True):
    ticker_data = get_data_for_given_day(ticker, day)

    if isinstance(ticker_data, float):
        return ticker_data

    if at_beginning:
        return ticker_data['Open'][0]

    return ticker_data['Close'][0]

