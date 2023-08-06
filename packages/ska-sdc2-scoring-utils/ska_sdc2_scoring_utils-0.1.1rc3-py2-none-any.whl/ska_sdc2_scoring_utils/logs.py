"""Logging fuctions."""
import sys
import logging

LOGFORMAT_VERBOSE = "%(levelname)-7s: %(message)-80s [%(filename)s L%(lineno)d]"

LOGFORMAT = "%(levelname)-7s: %(message)-80s"


def init_logger(level=logging.DEBUG, verbose=False):
    """Initialise the logger."""
    logger = logging.getLogger("")
    handler = logging.StreamHandler(sys.stdout)
    if verbose:
        formatter = logging.Formatter(LOGFORMAT_VERBOSE)
    else:
        formatter = logging.Formatter(LOGFORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
