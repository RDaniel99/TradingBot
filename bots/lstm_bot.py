from bots.bot import Bot
import math
from copy import deepcopy
import matplotlib.pyplot as plt
import keras
import pandas as pd
import numpy as np
from datetime import date
import datetime
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping


from bots.constants import SELL_SIGNAL, BUY_SIGNAL, HOLD_SIGNAL
from bots.utils.utils import get_list_of_prices_for_given_interval
from constants import PREDICT_IN_NEXT_DAYS, EPOCHS, BATCH_SIZE, GO_BACK_WITH_DAYS, DROPOUT_RATIO
from trading_api import get_price_for_ticker


class LSTMBot(Bot):
    def __init__(self, start_date, end_date, ticker, details):
        super().__init__(start_date, end_date, ticker, details)

        self.model = None
        self.X_train = None
        self.Y_train = None
        self.X_test = None
        self.Y_test = None

        self.scaler = MinMaxScaler(feature_range=(0, 1))

        self.predicted = None

        self.prepare()

    def prepare(self):
        print("Start preparing model")
        self.preprocess_training_data()
        self.build_model()
        self.preprocess_test_data()
        self.train_model()
        print("Model prepared successfully")
        # self.predict_prices()

    def preprocess_training_data(self):
        print("-- Preprocess Training Data")
        start_training_date = self.start_date - datetime.timedelta(days=GO_BACK_WITH_DAYS)

        training_prices = get_list_of_prices_for_given_interval(self.ticker, start_training_date, self.start_date)
        training_prices = np.array(training_prices)
        training_prices = np.reshape(training_prices, (training_prices.size, 1))
        training_prices = self.scaler.fit_transform(training_prices)

        self.X_train = []
        self.Y_train = []

        for i in range(60, len(training_prices)):
            self.X_train.append(training_prices[i - 60:i])
            self.Y_train.append(training_prices[i])

        self.X_train = np.array(self.X_train)
        self.Y_train = np.array(self.Y_train)

        ceva = np.random.permutation(len(self.X_train))

        self.X_train = self.X_train[ceva]
        self.Y_train = self.Y_train[ceva]

        self.Y_train = np.reshape(self.Y_train, (self.Y_train.shape[0],))

        self.X_train = np.reshape(self.X_train, (self.X_train.shape[0], self.X_train.shape[1], 1))

    def preprocess_test_data(self):
        print("-- Preprocess test data")
        start_test_date = self.start_date - datetime.timedelta(days=60)

        test_prices = get_list_of_prices_for_given_interval(self.ticker, start_test_date, self.end_date)
        test_prices = np.array(test_prices)
        test_prices = np.reshape(test_prices, (test_prices.size, 1))
        test_prices = self.scaler.fit_transform(test_prices)

        self.X_test = []
        self.Y_test = []

        for i in range(60, len(test_prices)):
            self.X_test.append(test_prices[i - 60:i])
            self.Y_test.append(test_prices[i])

        self.X_test = np.array(self.X_test)
        self.Y_test = np.array(self.Y_test)

        self.Y_test = np.reshape(self.Y_test, (self.Y_test.shape[0],))

        self.X_test = np.reshape(self.X_test, (self.X_test.shape[0], self.X_test.shape[1], 1))

    def train_model(self):
        print("-- Start training")
        self.model.fit(self.X_train, self.Y_train, epochs=EPOCHS, batch_size=BATCH_SIZE)

    def predict_prices(self):
        self.predicted = self.scaler.inverse_transform(self.model.predict(self.X_test))

    def build_model(self):
        print("-- Build Model")
        self.model = Sequential()

        self.model.add(LSTM(units=100, return_sequences=True, input_shape=(self.X_train.shape[1], 1)))

        self.model.add(LSTM(units=100, return_sequences=True))

        self.model.add(LSTM(units=100, return_sequences=True))

        self.model.add(LSTM(units=100, return_sequences=True))

        self.model.add(LSTM(units=100))
        self.model.add(Dropout(DROPOUT_RATIO))

        self.model.add(Dense(units=1))

        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def get_signal(self, current_date) -> (int, int):
        predicted_prices = self.predict_prices_in_future(current_date)
        yesterday_price = get_price_for_ticker(self.ticker, current_date - datetime.timedelta(days=1))

        max_price = yesterday_price
        max_position = -1

        min_price = yesterday_price
        min_position = -1

        for i in range(len(predicted_prices)):
            if max_price < predicted_prices[i]:
                max_price = predicted_prices[i]
                max_position = i

            if min_price > predicted_prices[i]:
                min_price = predicted_prices[i]
                min_position = i

        # TODO: Add risk parameter
        if max_position == -1:
            return SELL_SIGNAL, 100

        if min_position == -1:
            return BUY_SIGNAL, 100

        if max_position < min_position:
            return BUY_SIGNAL, 50

        if min_position < max_position:
            return SELL_SIGNAL, 50

        return HOLD_SIGNAL, 100

    def predict_prices_in_future(self, current_date, next_days=PREDICT_IN_NEXT_DAYS):
        first_date = current_date - datetime.timedelta(days=60)

        input_prices = get_list_of_prices_for_given_interval(self.ticker, first_date,
                                                             current_date - datetime.timedelta(days=1))
        input_copy = get_list_of_prices_for_given_interval(self.ticker, first_date,
                                                           current_date - datetime.timedelta(days=1))
        input_prices = np.array(input_prices)
        input_prices = np.reshape(input_prices, (input_prices.size, 1))
        input_prices = self.scaler.fit_transform(input_prices)
        input_prices = np.reshape(input_prices, (1, input_prices.size, 1))

        predicted_prices = []

        while next_days > 0:
            predicted_price = self.scaler.inverse_transform(self.model.predict(input_prices))
            predicted_prices.append(float(predicted_price[0][0]))

            input_copy = input_copy[1:]
            input_copy.append(float(predicted_price[0][0]))

            input_prices = np.array(input_copy)
            input_prices = np.reshape(input_prices, (input_prices.size, 1))
            input_prices = self.scaler.fit_transform(input_prices)
            input_prices = np.reshape(input_prices, (1, input_prices.size, 1))

            next_days -= 1

        return predicted_prices
