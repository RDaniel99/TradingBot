import dataset
import datetime
from datetime import date


def get_list_of_prices_for_given_interval(ticker, start_date, end_date):
    delta = datetime.timedelta(days=1)

    prices = []

    while start_date <= end_date:
        prices.append(dataset.get_price_for_ticker(ticker, start_date))

        start_date += delta

    return prices


def fill_crypto_cache(ticker, START, END, filename):
    delta = datetime.timedelta(days=1)
    prices = []

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                prices.append(float(line))
            except:
                prices.append(prices[len(prices) - 1])

    idx = 0
    while START <= END:
        dataset.fill_cache(ticker, prices[idx], START, START)
        START += delta
        idx += 1


def get_date_from_string(date_as_string):
    month = 0
    idx = 0

    while date_as_string[idx] != '/':
        month = month * 10 + int(date_as_string[idx]) - int('0')
        idx += 1

    idx += 1

    day = 0

    while date_as_string[idx] != '/':
        day = day * 10 + int(date_as_string[idx]) - int('0')
        idx += 1

    idx += 1

    year = 0

    while idx < len(date_as_string):
        year = year * 10 + int(date_as_string[idx]) - int('0')
        idx += 1

    return date(year, month, day)


def fill_stock_cache(ticker, START, END, filename):
    delta = datetime.timedelta(days=1)
    start_day = START

    previous_price = None

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.split('\t')
            dt = get_date_from_string(data[0])

            while start_day < dt:
                dataset.fill_cache(ticker, previous_price, start_day, start_day)
                start_day += delta

            price = float(data[1])
            previous_price = price

            dataset.fill_cache(ticker, price, dt, dt)
