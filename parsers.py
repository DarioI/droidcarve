# This file is part of DroidCarve.
#
# Copyright (C) 2019, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

import os, re
import constants

from xml.dom import minidom
from axmlparserpy.axmlprinter import AXMLPrinter
import xml.dom.minidom

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_crypto(class_being_called):
    if class_being_called in constants.CRYPTO_CLASSES:
        return class_being_called
    return None


def is_method_call(line):
    match = re.search("invoke-\w+(?P<invoke>.*)", line)
    if match:
        return True
    else:
        return False


def extract_method_call(data):
    # Default values
    c_dst_class = data
    c_dst_method = None
    c_local_args = None
    c_dst_args = None
    c_ret = None

    # The call looks like this
    #  <destination class>) -> <method>(args)<return value>
    match = re.search(
        '(?P<local_args>\{.*\}),\s+(?P<dst_class>.*);->' +
        '(?P<dst_method>.*)\((?P<dst_args>.*)\)(?P<return>.*)', data)

    if match:
        c_dst_class = match.group('dst_class')
        c_dst_method = match.group('dst_method')
        c_dst_args = match.group('dst_args')
        c_local_args = match.group('local_args')
        c_ret = match.group('return')

    method = {
        # Destination class
        'to_class': c_dst_class,

        # Destination method
        'to_method': c_dst_method,

        # Local arguments
        'local_args': c_local_args,

        # Destination arguments
        'dst_args': c_dst_args,

        # Return value
        'return': c_ret
    }

    return method


def is_class(line):
    match = re.search("\.class\s+(?P<class>.*);", line)
    if match:
        return True
    else:
        return False


def is_const_string(line):
    match = re.search("const-string\s+(?P<const>.*)", line)
    if match:
        return True
    else:
        return False


def extract_const_string(data):
    match = re.search('(?P<var>.*),\s+"(?P<value>.*)"', data)

    if match:

        string = {
            # Variable
            'name': match.group('var'),

            # Value of string
            'value': match.group('value')
        }

        return string
    else:
        return None


def extract_class(data, file_path):
    class_info = data.split(" ")
    c = {
        # Last element is the class name
        'name': class_info[-1],

        # Package name
        'package': ".".join(class_info[-1].split('/')[:-1]),

        # Class deepth
        'depth': len(class_info[-1].split("/")),

        # All elements refer to the type of class
        'type': " ".join(class_info[:-1]),

        # Properties
        'properties': [],

        # File
        'file-path': file_path,

        # Const strings
        'const-strings': [],

        # Methods
        'methods': []
    }

    return c


def is_method_call(line):
    match = re.search("invoke-\w+(?P<invoke>.*)", line)
    if match:
        return True
    else:
        return False


def _is_smali_code(code_line):
    code_line = code_line.lstrip().replace("\n", "")

    if code_line.startswith(constants.CLASS_ANNOTATION):
        return False

    if code_line.startswith(constants.ANNOTATION):
        return False

    if code_line.startswith(constants.INTERFACE_ANNOTATION):
        return False

    if code_line.startswith(constants.SUPER_ANNOTATION):
        return False

    if code_line.startswith(constants.SOURCE_ANNOTATION):
        return False

    if code_line.startswith(constants.END):
        return False

    return True


def _get_opcode(code_line):
    return code_line.split(" ")[0]


def is_class_method(line):
    match = re.search("\.method\s+(?P<method>.*)$", line)
    if match:
        return True
    else:
        return False


def extract_class_method(data):
    method_info = data.split(" ")

    # A method looks like:
    #  <name>(<arguments>)<return value>
    m_name = method_info[-1]
    m_args = None
    m_ret = None

    # Search for name, arguments and return value
    match = re.search(
        "(?P<name>.*)\((?P<args>.*)\)(?P<return>.*)", method_info[-1])

    if match:
        m_name = match.group('name')
        m_args = match.group('args')
        m_ret = match.group('return')

    method = {
        # Method name
        'name': m_name,

        # Arguments
        'args': m_args,

        # Return value
        'return': m_ret,

        # Additional info such as public static etc.
        'type': " ".join(method_info[:-1]),

        # Calls
        'calls': []
    }

    return method


def is_dynamic(class_being_called):
    if class_being_called in constants.DYNAMIC_LOADING_CLASSES:
        return class_being_called
    return None


def is_safetynet(class_being_called):
    if class_being_called in constants.SAFETYNET_CLASSES:
        return class_being_called
    return None


def is_url(string):
    return re.match(url_regex, string);


class CodeParser:

    def __init__(self, code_path):
        self.code_path = code_path
        self.classes = []
        self.strings = []
        self.urls = []
        self.crypto_calls = {}
        self.dynamic_load_calls = {}
        self.safetynet_calls = {}

    '''
    Extract class name from a smali source line. Every class name is represented
    as a classdescriptor that starts zith 'L' and ends with ';'.
    '''

    def extract_class_name(self, class_line):
        for el in class_line.split(" "):
            if el.startswith("L") and el.endswith(";"):
                return el

    def start(self):
        for subdir, dirs, files in os.walk(self.code_path):
            for file in files:
                full_path = os.path.join(subdir, file)
                with open(full_path, 'r') as f:
                    continue_loop = True
                    line_number = 1
                    temp_clazz = {}
                    for line in f:
                        if is_class(line):
                            temp_clazz = extract_class(line, full_path)
                            self.classes.append(temp_clazz)

                        if is_const_string(line):
                            string = extract_const_string(line)['value']
                            self.strings.append(string)
                            if is_url(string):
                                self.urls.append(string)
                            if temp_clazz:
                                temp_clazz["const-strings"].append(string)

                        elif '.method' in line:  # class methods
                            if is_class_method(line):
                                class_method = extract_class_method(line)


                        elif 'invoke' in line:
                            if is_method_call(line):
                                method_call = extract_method_call(line)
                                self.process_crypto(method_call, temp_clazz)
                                self.proces_dynamic(method_call, temp_clazz)
                                self.proces_safetynet(method_call, temp_clazz)

                    if not continue_loop:
                        continue

        print("Found %s classes" % str(len(self.classes)))
        print("Found %s strings" % str(len(self.strings)))

    def process_crypto(self, method_call, temp_clazz):
        if is_crypto(method_call['to_class']):
            if method_call['to_class'] in self.crypto_calls:
                self.crypto_calls[method_call['to_class']].append(temp_clazz)
            else:
                self.crypto_calls[method_call['to_class']] = [temp_clazz]

    def proces_dynamic(self, method_call, temp_clazz):
        if is_dynamic(method_call['to_class']):
            if method_call['to_class'] in self.dynamic_load_calls:
                self.dynamic_load_calls[method_call['to_class']].append(temp_clazz)
            else:
                self.dynamic_load_calls[method_call['to_class']] = [temp_clazz]

    def proces_safetynet(self, method_call, temp_clazz):
        if is_safetynet(method_call['to_class']):
            if method_call['to_class'] in self.safetynet_calls:
                self.safetynet_calls[method_call['to_class']].append(temp_clazz)
            else:
                self.safetynet_calls[method_call['to_class']] = [temp_clazz]

    def get_classes(self):
        return self.classes

    def get_crypto(self):
        return self.crypto_calls

    def get_urls(self):
        return self.urls

    def get_dynamic(self):
        return self.dynamic_load_calls

    def get_safetynet(self):
        return self.safetynet_calls


class AndroidManifestParser:

    def __init__(self, manifest_xml_file):

        if manifest_xml_file is None:
            raise TypeError

        self.manifest = manifest_xml_file
        self.permissions = []

    def start(self):
        ap = AXMLPrinter(open(self.manifest, 'rb').read())
        buff = minidom.parseString(ap.getBuff()).toxml()
        xml_code = xml.dom.minidom.parseString(buff.rstrip())  # or xml.dom.minidom.parseString(xml_string)
        pretty_xml_as_string = xml_code.toprettyxml()
        for line in pretty_xml_as_string.split("\n"):
            if not line.find("<uses-permission") == -1:
                self.permissions.append(line.split("\"")[1])

    def get_xml(self):
        ap = AXMLPrinter(open(self.manifest, 'rb').read())
        buff = minidom.parseString(ap.getBuff()).toxml()
        xml_code = xml.dom.minidom.parseString(buff.rstrip())  # or xml.dom.minidom.parseString(xml_string)
        return xml_code.toprettyxml()

    def get_permissions(self):
        return self.permissions


class FileParser():

    def __init__(self, files_path):
        self.files_path = files_path
        self.signature_files = []
        self.xml_files = []

    def start(self):
        for subdir, dirs, files in os.walk(self.files_path):
            for file in files:
                full_path = os.path.join(subdir, file)
                if file.endswith("RSA"):
                    self.signature_files.append(full_path)
                if file.endswith("xml"):
                    self.xml_files.append(full_path)

    def get_signature_files(self):
        return self.signature_files

    def get_xml_files(self):
        return self.xml_files

    def get_xml(self, name):
        for xml_file in self.xml_files:
            if xml_file.endswith(name):
                return xml_file
