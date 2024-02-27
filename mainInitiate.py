import time
from strategy import BitcoinTradingStrategy
from logging_component import Logger

def main():
    # Replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your actual API key and secret key
    api_key = 'API KEY HERE7'
    secret_key = 'SECRET API HERE'

    # Initialize Logger for terminal display
    logger = Logger(log_to_file=False)

    # Log program details
    logger.log_info("Initializing the trading program.")
    logger.log_info("Connecting to Crypto.com exchange using CCXT.")

    # Initialize Trading Strategy with API key and secret key
    strategy = BitcoinTradingStrategy(logger, api_key, secret_key)

    # Execute a market order for each trading pair on program initiation
    logger.log_info("Executing market orders on program initiation.")
    strategy.execute_trade()

    # Run the trading loop
    while True:
        try:
            # Fetch all symbols available on the exchange
            all_symbols = strategy.get_all_symbols()

            # Execute smart trades for each symbol in market pairs
            for symbol in all_symbols:
                logger.log_info(f"Analyzing data for {symbol}")
                strategy.execute_trade_for_symbol(symbol)

            # Sleep for 60 seconds (adjust based on your trading frequency)
            time.sleep(60)

        except Exception as e:
            logger.log_error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
