from bots.bot import Bot
import bots.indices.macd as macd
import bots.indices.rsi as rsi
import bots.indices.sma as sma
import bots.indices.ema as ema
from bots.constants import BUY_SIGNAL, SELL_SIGNAL, HOLD_SIGNAL


class StatisticBot(Bot):
    def __init__(self, start_date, end_date, ticker, details):
        super().__init__(start_date, end_date, ticker, details)

        self.rsi = None
        self.rsi_flag = None

        self.macd = None

        self.ema = None
        self.sma = None

        print("Preparing indicators...")
        self.get_indicators()
        print("Prepared indicators successfully")

    def get_indicators(self):
        use_macd = self.details["use_macd"]
        use_rsi = self.details["use_rsi"]
        use_sma_plus_ema = self.details["use_sma_plus_ema"]

        if use_rsi:
            print("-- Preparing RSI (window_length = 14)")
            self.rsi = rsi.compute_14(self.ticker, self.start_date, self.end_date)
            print("-- Prepared RSI")

        if use_macd:
            print("-- Preparing MACD (signal_length = 9)")
            self.macd = macd.compute(self.ticker, self.start_date, self.end_date, 9)
            print("-- Prepared MACD")

        if use_sma_plus_ema:
            print("-- Preparing SMA (window_length = 10)")
            self.sma = sma.compute_10(self.ticker, self.start_date, self.end_date)
            print("-- Prepared SMA")
            print("-- Preparing EMA (window_length = 10)")
            self.ema = ema.compute_10(self.ticker, self.start_date, self.end_date)
            print("-- Prepared EMA")

    def get_signal(self, current_date) -> (int, int):
        delta = current_date - self.start_date
        position = delta.days

        votes = 0
        buy_votes = 0
        sell_votes = 0
        hold_votes = 0

        if self.rsi is not None:
            buy_vote, sell_vote, hold_vote = self.get_signal_rsi(position)
            buy_votes += buy_vote
            sell_votes += sell_vote
            hold_votes += hold_vote
            print(f"-- RSI: Buy : {buy_vote} ; Sell : {sell_vote} ; Hold : {hold_vote}")
            votes += 1

        if self.macd is not None:
            buy_vote, sell_vote, hold_vote = self.get_signal_macd(position)
            buy_votes += buy_vote
            sell_votes += sell_vote
            hold_votes += hold_vote
            print(f"-- MACD: Buy : {buy_vote} ; Sell : {sell_vote} ; Hold : {hold_vote}")
            votes += 1

        if self.sma is not None and self.ema is not None:
            buy_vote, sell_vote, hold_vote = self.get_signal_sma_and_ema(position)
            buy_votes += buy_vote
            sell_votes += sell_vote
            hold_votes += hold_vote
            print(f"-- SMA+EMA: Buy : {buy_vote} ; Sell : {sell_vote} ; Hold : {hold_vote}")
            votes += 1

        if buy_votes > sell_votes:  # and buy_votes >= hold_votes:
            buy_votes -= sell_votes
            buy_votes -= 0.5 * hold_votes

            if buy_votes > 0.0:
                percentage = buy_votes / votes * 100.0
                return BUY_SIGNAL, percentage

        if sell_votes > buy_votes:  # and sell_votes >= hold_votes:
            sell_votes -= buy_votes
            sell_votes -= 0.5 * hold_votes

            if sell_votes > 0.0:
                percentage = sell_votes / votes * 100.0
                return SELL_SIGNAL, percentage

        return HOLD_SIGNAL, 100

    def get_signal_rsi(self, position):
        if self.rsi[position] > 65:
            if self.rsi_flag is None:
                self.rsi_flag = 'Flag'
                return 1, 0, 0  # buy

            return 0, 0, 1  # hold
        else:
            if self.rsi_flag is not None:
                self.rsi_flag = None
                return 0, 1, 0  # sell

        return 0, 0, 1  # hold

    def get_signal_macd(self, position):
        if self.macd[position] > 0:
            if position > 0 and self.macd[position - 1] < 0:
                return 1, 0, 0  # buy

            return 0, 0, 1  # hold

        if self.macd[position] < 0:
            if position > 0 and self.macd[position - 1] > 0:
                return 0, 1, 0  # sell

        return 0, 0, 1  # hold

    def get_signal_sma_and_ema(self, position):
        ema_minus_sma = self.ema[position] - self.sma[position]

        if ema_minus_sma > 0:
            if position > 0:
                if self.ema[position - 1] < self.sma[position - 1]:
                    return 1, 0, 0  # buy

                return 0, 0, 1  # hold

        if ema_minus_sma < 0:
            if position > 0:
                if self.ema[position - 1] > self.sma[position - 1]:
                    return 0, 1, 0  # sell

        return 0, 0, 1  # hold
