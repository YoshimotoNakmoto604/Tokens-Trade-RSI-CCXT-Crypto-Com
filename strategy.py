import ccxt
import time
import numpy as np
from pprint import pprint
from logging_component import Logger

class BitcoinTradingStrategy:
    def __init__(self, logger, api_key, secret_key):
        self.logger = logger
        self.api_key = api_key
        self.secret_key = secret_key
        self.exchange = ccxt.cryptocom({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
        })

    def execute_trade(self):
        try:
            # Fetch all symbols available on the exchange
            all_symbols = self.exchange.load_markets().keys()

            # Run the trading loop for each symbol
            for symbol in all_symbols:
                self.logger.log_info(f"Analyzing data for {symbol}")
                self.execute_trade_for_symbol(symbol)
                time.sleep(3)  # Introduce a 3-second delay for each token

        except ccxt.NetworkError as ne:
            self.logger.log_error(f"Network error: {ne}")
        except ccxt.ExchangeError as ee:
            self.logger.log_error(f"Exchange error: {ee}")
        except ccxt.BaseError as be:
            self.logger.log_error(f"Base error: {be}")
        except Exception as e:
            self.logger.log_error(f"An unexpected error occurred: {e}")

    def execute_trade_for_symbol(self, symbol):
        try:
            # Fetch ticker data for the symbol
            ticker = self.exchange.fetch_ticker(symbol)

            # Implement trading strategy based on various metrics
            mean_average = self.calculate_7_day_mean(symbol)
            candle_data = self.fetch_candle_data(symbol)
            rsi = self.calculate_rsi(symbol)

            # Log market data
            self.logger.log_info(f"Symbol: {symbol}")
            self.logger.log_info(f"Last Price: {ticker['last']}")
            self.logger.log_info(f"7-Day Mean Average: {mean_average}")
            self.logger.log_info("Candle Data:")
            pprint(candle_data)
            self.logger.log_info(f"RSI: {rsi}")

            # Make trading decision based on RSI and your strategy conditions
            if self.should_buy(rsi):
                self.logger.log_info(f"{symbol} - Executing buy order")
                self.execute_buy(symbol)
            elif self.should_sell(rsi):
                self.logger.log_info(f"{symbol} - Executing sell order")
                self.execute_sell(symbol)

        except ccxt.NetworkError as ne:
            self.logger.log_error(f"Network error for {symbol}: {ne}")
        except ccxt.ExchangeError as ee:
            self.logger.log_error(f"Exchange error for {symbol}: {ee}")
        except ccxt.BaseError as be:
            self.logger.log_error(f"Base error for {symbol}: {be}")
        except Exception as e:
            self.logger.log_error(f"An unexpected error occurred for {symbol}: {e}")

    def calculate_7_day_mean(self, symbol):
        # Fetch historical close prices for the specified number of days
        close_prices = self.fetch_close_prices(symbol, days=7)
        mean_average = np.mean(close_prices)
        return mean_average

    def fetch_close_prices(self, symbol, days=7):
        # Fetch historical close prices for the specified number of days
        ohlcv_data = self.exchange.fetch_ohlcv(symbol, timeframe='1d', limit=days)
        close_prices = [entry[4] for entry in ohlcv_data]
        return close_prices

    def fetch_candle_data(self, symbol):
        # Fetch candlestick data for the symbol
        candle_data = self.exchange.fetch_ohlcv(symbol, timeframe='1h', limit=5)
        return candle_data

    def calculate_rsi(self, symbol, period=14):
        # Fetch historical close prices for the specified number of days
        close_prices = self.fetch_close_prices(symbol, days=period + 1)  # Add one extra day for calculating RSI

        # Calculate RSI using the close prices
        price_changes = np.diff(close_prices)
        gains = price_changes[price_changes > 0]
        losses = -price_changes[price_changes < 0]

        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        for i in range(period, len(price_changes)):
            if price_changes[i] > 0:
                avg_gain = ((avg_gain * (period - 1)) + price_changes[i]) / period
                avg_loss = (avg_loss * (period - 1)) / period
            else:
                avg_gain = (avg_gain * (period - 1)) / period
                avg_loss = ((avg_loss * (period - 1)) - price_changes[i]) / period

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def should_buy(self, rsi):
        # Implement buy condition here
        # Example: Buy if the RSI is below 43
        return rsi < 45

    def should_sell(self, rsi):
        # Implement sell condition here
        # Example: Sell if the RSI is above 73
        return rsi > 64

    def execute_buy(self, symbol):
        try:
            # Implement buy logic here
            # Example: Buy $1.50 USD worth of the trading pair
            amount_to_buy = 0.75
            order = self.exchange.create_market_buy_order(symbol, amount_to_buy)
            self.logger.log_info(f"{symbol} - Buy Order Executed: {order}")
        except ccxt.AuthenticationError as e:
            self.logger.log_error(f"Authentication error for {symbol}: {e}")

    def execute_sell(self, symbol):
        try:
            # Implement sell logic here
            # Example: Sell all available quantity of the trading pair
            quantity = self.get_available_balance(symbol)
            if quantity > 0:
                order = self.exchange.create_market_sell_order(symbol, quantity=quantity)
                self.logger.log_info(f"{symbol} - Sell Order Executed: {order}")
            else:
                self.logger.log_info(f"{symbol} - No available balance for selling")
        except ccxt.AuthenticationError as e:
            self.logger.log_error(f"Authentication error for {symbol}: {e}")

    def get_available_balance(self, symbol):
        # Fetch available balance for the specified symbol
        balance = self.exchange.fetch_balance()
        available_balance = balance['free'][symbol] if symbol in balance['free'] else 0
        return available_balance
