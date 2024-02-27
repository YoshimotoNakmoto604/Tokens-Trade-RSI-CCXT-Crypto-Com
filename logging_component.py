# logging_component.py
import logging

class Logger:
    def __init__(self, log_to_file=True):
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Create a logger
        self.logger = logging.getLogger(__name__)

        # Create a file handler and set the formatter
        if log_to_file:
            file_handler = logging.FileHandler('trading_log.txt')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(file_formatter)

            # Add the file handler to the logger
            self.logger.addHandler(file_handler)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_exchange_data(self, symbol, data):
        self.logger.debug(f"{symbol} - Exchange Data: {data}")
