# coding=utf-8
import logging

# set up logs to file
import sys


# Some colors for the console
class AnsiColors:
    WHITE = '\033[97m'
    GRAY = '\033[37m'
    BROWN = '\033[33m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLACK = '\033[90m'
    ENDCOLOR = '\033[0m'


logformat = "%(asctime)s [%(levelname)s] " \
            "%(module)s::%(filename)s::%(funcName)s():L%(lineno)s:" \
            + AnsiColors.BLUE + "%(message)s" + AnsiColors.ENDCOLOR
LOG_FILENAME = 'static/logging.txt'
logging.basicConfig(filename=LOG_FILENAME, filemode='w')
logger = logging.getLogger()
handler = logging.StreamHandler(stream=sys.stderr)
formatter = logging.Formatter(logformat, datefmt="[%Y-%m-%d %H:%M:%S %z]")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
