# This file is part of DroidCarve.
#
# Copyright (C) 2015, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, constants, re, utils

from xml.dom import minidom
from axmlparserpy.axmlprinter import AXMLPrinter
import xml.dom.minidom

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'


class CodeParser():

    def __init__(self, code_path):
        self.code_path = code_path
        self.classes = []
        self.strings = []

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
                        if self.is_class(line):
                            temp_clazz = self.extract_class(line, full_path)
                            self.classes.append(temp_clazz)

                        if self.is_const_string(line):
                            string = self.extract_const_string(line)['value']
                            self.strings.append(string)
                            if temp_clazz:
                                temp_clazz["const-strings"].append(string)

                        elif '.method' in line: #class methods
                            if self.is_class_method(line):
                                class_method = self.extract_class_method(line)
                                #utils.print_blue("Class %s method: %s" % (temp_clazz['name'], class_method['name']))
                            pass

                        elif 'invoke' in line:
                            if self.is_method_call(line):
                                method_call = self.extract_method_call(line)
                                #utils.print_red("Method %s in class %s" % (method_call['to_method'], method_call['to_class']))
                            pass

                        #self.detect_crypto(line)

                        # if line.lstrip().startswith("const-string"):
                        # print line

                    if not continue_loop:
                        continue

        print "Found %s classes" % str(len(self.classes))
        print "Found %s strings" % str(len(self.strings))

    def is_method_call(self, line):
        match = re.search("invoke-\w+(?P<invoke>.*)", line)
        if match:
            return True
        else:
            return False

    def extract_method_call(self, data):
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

    def is_class(self, line):
        match = re.search("\.class\s+(?P<class>.*);", line)
        if match:
            return True
        else:
            return False

    def is_const_string(self, line):
        match = re.search("const-string\s+(?P<const>.*)", line)
        if match:
            return True
        else:
            return False

    def extract_const_string(self, data):

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

    def extract_class(self, data, file_path):

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

    def detect_crypto(self,code_line):
        if not self._is_smali_code(code_line):
            return
        code_line = code_line.lstrip()
        opcode = self._get_opcode(code_line)
        print opcode

    def is_method_call(self, line):
        match = re.search("invoke-\w+(?P<invoke>.*)", line)
        if match:
            return True
        else:
            return False

    def _is_smali_code(self, code_line):
        code_line = code_line.lstrip().replace("\n","")

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

    def _get_opcode(self, code_line):
        return code_line.split(" ")[0]

    def get_classes(self):
        return self.classes

    def is_class_method(self, line):
        match = re.search("\.method\s+(?P<method>.*)$", line)
        if match:
            return True
        else:
            return False

    def extract_class_method(self, data):

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


class AndroidManifestParser:

    def __init__(self, manifest_xml_file):
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
