# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

import re, whichcraft, os, random, string, hashlib

BAKSMALI_PATH = os.getcwd() + "/bin/baksmali.jar"


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


'''
Check if there is a baksmali tool.
'''


def has_baksmali():
    return os.path.isfile(BAKSMALI_PATH)


def path_to_dict(path):
    d = {'key': get_path_hash(path), 'title': os.path.basename(path), 'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
        d['isLeaf'] = True
    return d


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_path_hash(path):
    return hashlib.sha224(path.encode('utf-8')).hexdigest()


def xml_parser(xml):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    process_element(root)


services = []
activities = []
permissions = []

manifest = {
    "activities": [],
    "permissions": [],
    "services": [],
    "features": [],
    "providers": [],
    "receivers": [],
    "meta_data": []
}


def process_element(element):
    if element.tag == "activity":
        manifest["activities"].append(
            {
                'name': element.attrib['name'],
                'intent': filter_intent(element, 'activity', element.attrib['name'])
            }
        )

    if element.tag == "uses-permission" or element.tag == "permission":
        manifest["permissions"].append(element.attrib['name'])

    if element.tag == "service":
        manifest["services"].append(
            {
                'name': element.attrib['name'],
                'exported': element.attrib['exported'],
                'intent': filter_intent(element, 'service', element.attrib['name'])
            }
        )

    if element.tag == "uses-feature":
        manifest["features"].append(element.attrib['name'])

    if element.tag == "provider":
        manifest["providers"].append({
            'name': element.attrib['name'],
            'exported': element.attrib['exported'],
            'authorities': element.attrib['authorities'],
        })

    if element.tag == "receiver":

        item = {'name': element.attrib['name'], 'intent': filter_intent(element, 'receiver', element.attrib['name'])}

        if 'permission' in element.attrib.keys():
            item['permission'] = element.attrib['permission']

        if 'exported' in element.attrib.keys():

            if element.attrib['exported'] == 'true':
                item['exported'] = True
            else:
                item['exported'] = False

        manifest['receivers'].append(item)

    if element.tag == "meta-data":

        item = {'name': element.attrib['name']}
        for key in element.attrib.keys():
            item[key] = element.attrib[key]
        manifest['meta_data'].append(item)

    for child in element:
        process_element(child)


def filter_intent(element, type, name):
    result = {
        'name': None,
        'category': None
    }
    if element.tag == type and element.attrib['name'] == name:
        for child in element:
            if child.tag == 'intent-filter':
                intent_filter = child
                for item in intent_filter:
                    if item.tag == "action":
                        _, value = item.attrib.popitem()
                        result['name'] = value
                    if item.tag == "category":
                        _, value = item.attrib.popitem()
                        result['category'] = value

    return None if (not result["name"] and not result["category"]) else result