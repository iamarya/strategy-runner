import logging

from utils.custom_logger import CustomFormatter


def setup():
    # Define format for logs
    fmt ='%(asctime)s | %(levelname)8s | %(module)25s | %(message)s'
    
    # Create stdout handler for logging to the console (logs all five levels)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))
    logging.basicConfig(level=logging.ERROR, handlers=[stdout_handler])

    logging.getLogger('engine').setLevel(logging.DEBUG)
    logging.getLogger('exchange').setLevel(logging.INFO)
    logging.getLogger('strategy').setLevel(logging.INFO)
    logging.getLogger('strategy.swing_trading_strategy').setLevel(logging.INFO)
    logging.getLogger('db').setLevel(logging.INFO)
    logging.getLogger('indicators').setLevel(logging.INFO)
    logging.getLogger('models').setLevel(logging.INFO)
    logging.getLogger('utils').setLevel(logging.INFO)
    logging.getLogger('services').setLevel(logging.DEBUG)
