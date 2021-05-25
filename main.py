import sys

from bots.lstm_bot import LSTMBot
from ui.GUI import GUI
import bots.indices.sma as sma
import bots.indices.ema as ema
import bots.indices.rsi as rsi
import bots.indices.macd as macd
from datetime import date
import dataset
from bots.utils.utils import get_list_of_prices_for_given_interval
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime
import bots.utils.utils as utils

from bots.statistic_bot import StatisticBot


def fill_BTC():
    ticker = 'BTC-USD'
    filename = 'BTC-USD_2015_1_1_2021_5_1.txt'
    START = date(2015, 1, 1)
    END = date(2021, 5, 1)
    utils.fill_crypto_cache(ticker, START, END, filename)


def fill_XRP():
    ticker = 'XRP-USD'
    filename = 'XRP-USD_2015_1_1_2021_5_1.txt'
    START = date(2015, 1, 1)
    END = date(2021, 5, 1)
    utils.fill_crypto_cache(ticker, START, END, filename)


def fill_ETH():
    ticker = 'ETH-USD'
    filename = 'ETH-USD_2015_8_7_2021_5_1.txt'
    START = date(2015, 8, 7)
    END = date(2021, 5, 1)
    utils.fill_crypto_cache(ticker, START, END, filename)


def fill_TSLA():
    ticker = 'TSLA'
    filename = 'TSLA_2015_1_2_2021_4_30.txt'
    START = date(2015, 1, 2)
    END = date(2021, 4, 30)
    utils.fill_stock_cache(ticker, START, END, filename)


def fill_cache():
    # Crypto
    fill_BTC()
    fill_XRP()
    fill_ETH()

    # Stocks
    fill_TSLA()


if __name__ == "__main__":
    fill_cache()

    # START = date(2018, 1, 1)
    # START_AFTER_10_DAYS = date(2018, 1, 24)
    # END = date(2020, 12, 31)

    # details = {"use_macd": True, "use_rsi": True, "use_sma_plus_ema": False, "cash": 1000}

    # bot = LSTMBot(START, END, 'BTC-USD', details)

    # predicted_prices_in_future = bot.predict_prices_in_future(START)
    # real_prices_in_future = get_list_of_prices_for_given_interval('BTC-USD', START, START_AFTER_10_DAYS)

    # print(predicted_prices_in_future)
    # print(real_prices_in_future)

    # sys.exit(0)

    # real_prices = get_list_of_prices_for_given_interval('BTC-USD', START, END)
    # predicted = bot.predicted

    guiFrame = GUI()
    guiFrame.mainloop()

    #     prices.append(dataset.get_price_for_ticker('BTC-USD', START))
    #     START += delta

    # with open('BTC-USD_2015_1_1_2021_5_1.txt', 'w') as f:
    #     for item in prices:
    #         f.write("%s\n" % item)

    # print(str(len(prices)) + " wrote in file")

    # START_COPY = START
    # delta = datetime.timedelta(days=1)

    # days = []

    # while START_COPY <= END:
    #    days.append(START_COPY)
    #    START_COPY += delta

    # bot = StatisticBot(START, END, 'BTC-USD', details)

    # print("Started")
    # bot.run()

    # bot.get_status(END + delta)

    # price_btc = get_list_of_prices_for_given_interval('BTC-USD', START, END)
    # print(price_btc)

    # sma = sma.compute_10('BTC-USD', START, date(2021, 4, 1))
    # print(sma)

    # ema = ema.compute_10('BTC-USD', START, date(2021, 4, 1))
    # print(ema)

    # rsi = bot.rsi
    # rsi = rsi.compute_14('BTC-USD', START, date(2021, 4, 1))
    # print(rsi)

    # macd = macd.compute('BTC-USD', START, date(2021, 4, 1), 9)
    # print(macd)

    # days = [x + 1 for x in range((END - START).days + 1)]

    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    # ax = plt.gca()
    # formatter = mdates.DateFormatter("%Y-%m-%d")
    # ax.xaxis.set_major_formatter(formatter)
    # locator = mdates.DayLocator()
    # ax.xaxis.set_major_locator(locator)
    # plt.plot(days, real_prices, color="blue")
    # plt.plot(days, predicted, color="red")

    # for buy in bot.buys:
    #    x_axis = buy[0]
    #    y_axis = price_btc[(x_axis - START).days]

    #    plt.plot([x_axis], [y_axis], color='green', marker='o', markersize=4)

    # for sell in bot.sells:
    #    x_axis = sell[0]
    #    y_axis = price_btc[(x_axis - START).days]

    #    plt.plot(x_axis, y_axis, color='red', marker='o', markersize=4)

    # plt.plot(sma, color="red")
    # plt.plot(ema, color="green")
    # plt.plot(rsi, color="red")
    # ax.bar(days, macd)
    # plt.show()
