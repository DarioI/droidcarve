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

import os

from xml.dom import minidom
from axmlparserpy.axmlprinter import AXMLPrinter
import xml.dom.minidom

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'


class CodeParser():

    def __init__(self, code_path):
        self.code_path = code_path

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
                    continue_loop = True;
                    for line in f:
                        if line.startswith(".class"):
                            class_line = line.strip("\n")  # extract the class line; always first line
                            class_name = self.extract_class_name(class_line)  # extract the class descriptor
                            # print class_name

                        # if line.lstrip().startswith("const-string"):
                        # print line

                    if not continue_loop:
                        continue


class AndroidManifestParser():

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
