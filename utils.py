# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

import re, whichcraft, os


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


def print_welcome():
    _print_title("DroidCarve")
    print("\n\nDroidCarve is capable of analyzing an Android APK file.\nIt automates various reverse engineering "
          "tasks.\n\nFor a full list of features, please see the help function.\n\n")
    _print_title("==")
    print("\n")


def _print_title(text, ch='=', length=78):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    print(banner)


def ask_question(question, answers):
    print(question)

    i = 0

    while i <= len(answers):
        for a in answers[i:i + 10]:
            print('[{}] '.format(i) + a)
            i = i + 1

        try:
            if len(answers) > 10:
                choice = int(input("\nEnter a number or press <enter> to see more: "))
            else:
                choice = int(input("Enter a number:"))
            if choice <= len(answers):
                return answers[choice]
            else:
                print_red("Not a valid choice.")
                ask_question(question, answers)
        except ValueError:
            pass


def prettyprintdict(dictionary):
    for key, value in dictionary.items():
        print_blue(key + " ({}) ".format(str(len(value))))
        for clazz in value:
            print_purple("\t - {} ".format(clazz['name']))


def read_file(filename, binary=True):
    """
    Open and read a file
    :param filename: filename to open and read
    :param binary: True if the file should be read as binary
    :return: bytes if binary is True, str otherwise
    """
    with open(filename, 'rb' if binary else 'r') as f:
        return f.read()


def adb_available():
    path = whichcraft.which("adb")
    if path is None:
        return False
    return True
