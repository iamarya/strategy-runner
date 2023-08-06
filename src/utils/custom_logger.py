import logging


class CustomFormatter(logging.Formatter):
    # https://talyian.github.io/ansicolors/

    grey = '\x1b[38;21m'
    blue = '\x1b[34m'
    pink = '\x1b[35m'
    red = '\x1b[31m'
    bold_red = '\x1b[41m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.pink + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)