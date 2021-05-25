from datetime import date

# General
crypto_tickers = ['BTC-USD', 'ETH-USD', 'XRP-USD']
stock_tickers = ['TSLA', 'AAPL', 'MSFT', 'GOOGL']
# TICKER = stock_tickers[0]
TICKER = crypto_tickers[1]
RISK = None  # TODO

# Statistical

# LSTM
EPOCHS = 100
BATCH_SIZE = 32
PREDICT_IN_NEXT_DAYS = 10
GO_BACK_WITH_DAYS = 730
DROPOUT_RATIO = 0.4
