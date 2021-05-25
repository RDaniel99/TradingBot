import dataset
from datetime import datetime, timedelta

from bots.constants import IS_DEBUG_MODE

MAX_POSSIBLE = 'MAX'


def get_price_for_ticker(ticker, day='today'):
    return dataset.get_price_for_ticker(ticker, day)


class TradingAPI:
    def __init__(self):
        self.curr_amount = 0
        self.curr_cash = 0
        self.wallet = {}
        self.invested = 0
        self.needs_status_update = False
        self.percentage_gains = 0

    def add_cash(self, cash):
        self.curr_cash += cash
        self.invested += cash
        self.needs_status_update = True
        return True

    def withdraw_cash(self, cash):
        if cash == MAX_POSSIBLE:
            self.curr_cash = 0
            self.needs_status_update = True
            return True

        if cash > self.curr_cash:
            return False

        self.curr_cash -= cash
        self.needs_status_update = True
        return True

    def get_curr_cash(self):
        return self.curr_cash

    def get_percentage_of_curr_cash(self, percentage):
        return percentage * self.curr_cash / 100.0

    def get_percentage_of_units(self, ticker, percentage):
        if not self.wallet.__contains__(ticker):
            self.wallet[ticker] = 0

        return percentage * self.wallet[ticker] / 100.0

    def buy(self, ticker, date, cash, at_beginning=True, logs=IS_DEBUG_MODE):
        if cash == MAX_POSSIBLE:
            cash = self.curr_cash

        if cash < 0.0001:
            return

        if cash - self.curr_cash > 0.001:
            if logs:
                print(f'Not enough cash for order')

            return False

        buy_price = dataset.get_price_for_ticker(ticker, date, at_beginning)

        if not self.wallet.__contains__(ticker):
            self.wallet[ticker] = 0

        self.wallet[ticker] += cash / buy_price
        self.curr_cash -= cash

        if logs:
            print(f'[{date}] Buy with ${cash}: {cash / buy_price} units of {ticker} for {buy_price}')

        self.needs_status_update = True
        return True

    def sell(self, ticker, date, units, at_beginning=False, logs=IS_DEBUG_MODE):
        if not self.wallet.__contains__(ticker):
            if logs:
                print(f'Not enough units to sell')

            return False

        if units < 0.0000001:
            return False

        if units == MAX_POSSIBLE:
            units = self.wallet[ticker]

        if units - self.wallet[ticker] > 0.0001:
            if logs:
                print(f'Not enough units to sell')

            return False

        sell_price = dataset.get_price_for_ticker(ticker, date, at_beginning)

        cash = sell_price * units
        self.curr_cash += cash
        self.wallet[ticker] -= units

        if logs:
            print(f'[{date}] Sell for ${cash}: {units} units of {ticker} for {sell_price}')

        self.needs_status_update = True
        return True

    def get_status(self, yesterday=None, logs=IS_DEBUG_MODE):
        if not self.needs_status_update:
            return self.percentage_gains

        if logs:
            print('Total cash amount: ' + str(self.curr_cash))
            print('Invested cash: ' + str(self.invested))
            print('Current status of wallet:')

        total_cash_in_wallet = 0

        for ticker in self.wallet:
            if yesterday is None:
                yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

            curr_price = dataset.get_price_for_ticker(ticker, yesterday)
            total_cash_in_wallet += curr_price * self.wallet[ticker]

            if logs:
                print(f'-- {self.wallet[ticker]} of {ticker} (curr_price = {curr_price} per unit)')

        if logs:
            print(f'Total cash in wallet in current day: {total_cash_in_wallet}')

        total_cash_in_total = total_cash_in_wallet + self.curr_cash
        percentage = (total_cash_in_total - self.invested) / self.invested * 100.0
        sign = '+'
        if percentage < 0.0:
            sign = ''

        self.percentage_gains = percentage
        self.needs_status_update = False
        if logs:
            print(f'Percentage gains/loss: {sign}{percentage}%')

        return self.percentage_gains
