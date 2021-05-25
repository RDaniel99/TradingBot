# https://www.investopedia.com/terms/m/macd.asp

from statistics import mean

import bots.indices.ema as ema
import datetime


def compute(ticker, start_date, end_date, signal_length):
    delta = datetime.timedelta(days=signal_length - 1)

    beginning_date = start_date - delta

    ema_12 = ema.compute_12(ticker, beginning_date, end_date)
    ema_26 = ema.compute_26(ticker, beginning_date, end_date)

    macd = []

    for i in range(len(ema_12)):
        macd.append(ema_12[i] - ema_26[i])

    final_macd = []
    for_signal = []

    for i in range(signal_length):
        for_signal.append(macd[i])

    position = signal_length

    final_macd.append(macd[position - 1] - mean(for_signal))

    delta = datetime.timedelta(days=1)

    while start_date < end_date:
        start_date += delta
        for_signal = for_signal[1:]
        for_signal.append(macd[position])
        position += 1

        final_macd.append(macd[position - 1] - mean(for_signal))

    return final_macd

    return macd
