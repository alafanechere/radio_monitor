import logging
from logging.handlers import RotatingFileHandler


def setup_telex_logger(name):
    formatter = logging.Formatter(fmt='%(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    file_handler = RotatingFileHandler('tracklisting.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(file_handler)

    return logger