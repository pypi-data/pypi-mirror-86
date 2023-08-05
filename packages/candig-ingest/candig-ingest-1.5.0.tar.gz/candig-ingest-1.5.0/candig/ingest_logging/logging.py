from datetime import date
import logging
import sys
import time


def getLogger(path=None):
    """
    Configure an logger object

    Args:
        path<string>: Path to directory where the logs will be saved.

    Returns:
        Logger object
    """
    # Change here if you want another date format
    formatter = logging.Formatter(
        fmt="%(asctime)s UTC %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if path:
        if path[-1] != '/':
            path += '/'
    elif path is None:
        path = ""

    # Change here if you want change the file name
    handler = logging.FileHandler(
        filename="{}{}.log".format(path, str(date.today())))
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logging.Formatter.converter = time.gmtime
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger
