import re


class TextStyle:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_purple(text):
    print(TextStyle.PURPLE + text + TextStyle.ENDC)


def print_blue(text):
    print(TextStyle.BLUE + text + TextStyle.ENDC)


def print_red(text):
    print(TextStyle.RED + text + TextStyle.ENDC)


def is_valid_regex(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False
