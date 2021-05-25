import datetime
from copy import deepcopy
from trading_api import TradingAPI

from bots.constants import BUY_SIGNAL, SELL_SIGNAL


class Bot:
    def __init__(self, start_date, end_date, ticker, details):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.details = details

        self.buys = []
        self.sells = []
        self.api = TradingAPI()

        self.prepare_api()

    def prepare_api(self):
        self.api.add_cash(self.details["cash"])

    def run(self):
        delta = datetime.timedelta(days=1)

        current_date = deepcopy(self.start_date)

        while current_date <= self.end_date:
            self.process(current_date)
            current_date += delta

    def process(self, current_date):
        print(f"Processing {current_date.day}/{current_date.month}/{current_date.year}")

        signal, percentage = self.get_signal(current_date)

        if signal == BUY_SIGNAL:
            self.buy(current_date, percentage)
        elif signal == SELL_SIGNAL:
            self.sell(current_date, percentage)

    def get_signal(self, current_date) -> (int, int):
        pass

    def buy(self, current_date, percentage):
        to_buy_cash = self.api.get_percentage_of_curr_cash(percentage)
        result = self.api.buy(self.ticker, current_date, to_buy_cash)
        if result:
            self.buys.append([current_date, to_buy_cash])

    def sell(self, current_date, percentage):
        to_sell_units = self.api.get_percentage_of_units(self.ticker, percentage)
        result = self.api.sell(self.ticker, current_date, to_sell_units)
        if result:
            self.sells.append([current_date, to_sell_units])

    def get_status(self, yesterday=None):
        self.api.get_status(yesterday)
