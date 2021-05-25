from tkinter import *
from tkcalendar import *
import datetime


# https://stackoverflow.com/questions/6874525/how-to-handle-a-button-click-event
from bots.lstm_bot import LSTMBot
from bots.statistic_bot import StatisticBot
from bots.utils.utils import get_list_of_prices_for_given_interval
from constants import TICKER, PREDICT_IN_NEXT_DAYS
from datetime import date

from matplotlib import pyplot as plt

class GUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        self.budgetLabel = Label(master, text="Budget")
        self.budgetLabel.grid()

        self.budgetEntry = IntVar()
        self.budgetEntry = Entry(textvariable=self.budgetEntry)
        self.budgetEntry.grid()

        self.dateStartLabel = Label(master, text="Start date")
        self.dateStartLabel.grid()

        self.dateStartEntry = DateEntry(master)
        self.dateStartEntry.grid()

        self.dateEndLabel = Label(master, text="End date")
        self.dateEndLabel.grid()

        self.dateEndEntry = DateEntry(master)
        self.dateEndEntry.grid()

        self.strategyVariable = IntVar()
        self.strategyVariable.set(1)

        self.strategyLabel = Label(master, text="Pick strategy")
        self.strategyLabel.grid()

        self.radioStatistic = Radiobutton(master, text="Statistic", variable=self.strategyVariable, value=1)
        self.radioStatistic.grid()

        self.radioDeep = Radiobutton(master, text="LSTM (In progress)", variable=self.strategyVariable, value=2)
        self.radioDeep.grid()

        self.indicatorsStaticLabel = Label(master, text="Indicators (for statistic strategy only)")
        self.indicatorsStaticLabel.grid()

        self.rsiVariable = IntVar()
        self.rsiCheckButton = Checkbutton(master, text="RSI", variable=self.rsiVariable, onvalue=1, offvalue=0)
        self.rsiCheckButton.grid()

        self.macdVariable = IntVar()
        self.macdCheckButton = Checkbutton(master, text="MACD", variable=self.macdVariable, onvalue=1, offvalue=0)
        self.macdCheckButton.grid()

        self.smaAndEmaVariable = IntVar()
        self.smaAndEmaButton = Checkbutton(master, text="SMA & EMA", variable=self.smaAndEmaVariable, onvalue=1, offvalue=0)
        self.smaAndEmaButton.grid()

        def button_click():
            print("You pressed Submit!")

            # print(self.strategyVariable.get())

            start_date = self.dateStartEntry.get_date()
            end_date = self.dateEndEntry.get_date()

            details = {"use_macd": self.macdVariable.get(),
                       "use_rsi": self.rsiVariable.get(),
                       "use_sma_plus_ema": self.smaAndEmaVariable.get(),
                       "cash": int(self.budgetEntry.get())}

            if self.strategyVariable.get() == 1:
                bot = StatisticBot(start_date, end_date, TICKER, details)
            else:
                bot = LSTMBot(start_date, end_date, TICKER, details)

            print(" ---- SIMULATION STARTED ----")

            bot.run()

            bot.get_status(end_date)

            show_plot(bot)

        self.submitButton = Button(master, text="Submit", command=button_click)
        self.submitButton.grid()


def show_plot(bot):
    # predicted_prices_in_future = bot.predict_prices_in_future(start_date)

    # end_dateeee = date(2021, 5, 10)

    # real_prices_in_future = get_list_of_prices_for_given_interval('BTC-USD', start_date, end_dateeee)

    # plt.plot(predicted_prices_in_future, color="blue")
    # plt.plot(real_prices_in_future, color="red")

    # plt.show()
    pass
