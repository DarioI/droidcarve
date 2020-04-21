# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

import io, os, re, utils, logging

from pyaxmlparser import APK
from pyaxmlparser.axmlprinter import AXMLPrinter
import xml.etree.ElementTree as ET

import constants

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


def extract_method_call(data, line_number=-1):
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
        'to_class': c_dst_class + ';',

        # Destination method
        'to_method': c_dst_method,

        # Local arguments
        'local_args': c_local_args,

        # Destination arguments
        'dst_args': c_dst_args,

        # Return value
        'return': c_ret,

        'line_number': line_number
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


def extract_class(data, file_path, file_key):
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
        'methods': [],

        'key': file_key
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
        self.crypto_calls = None
        self.dynamic_load_calls = None
        self.safetynet_calls = None
        self.file_hash_table = {}

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
                with io.open(full_path, 'r', encoding="utf-8") as f:
                    file_key = utils.get_path_hash(full_path)
                    self.file_hash_table[file_key] = full_path
                    continue_loop = True
                    line_number = 1
                    temp_clazz = {}
                    for line in f:
                        if is_class(line):
                            temp_clazz = extract_class(line, full_path, file_key)
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
                                method_call = extract_method_call(line, line_number)
                                self.process_crypto(method_call, temp_clazz, line_number)
                                self.proces_dynamic(method_call, temp_clazz)
                                self.proces_safetynet(method_call, temp_clazz)

                        line_number += 1

                    if not continue_loop:
                        continue

        logging.info("Found %s classes" % str(len(self.classes)))
        logging.info("Found %s strings" % str(len(self.strings)))

    def get_file_for_hash(self, key):
        try:
            return self.file_hash_table[key]
        except KeyError:
            return None

    def process_crypto(self, method_call, temp_clazz, line_number=-1):

        if not self.crypto_calls:
            self.crypto_calls = {}
        if is_crypto(method_call['to_class']):
            temp_clazz['line_number'] = line_number
            if method_call['to_class'] in self.crypto_calls:
                self.crypto_calls[method_call['to_class']].append(temp_clazz)
            else:
                self.crypto_calls[method_call['to_class']] = [temp_clazz]

    def proces_dynamic(self, method_call, temp_clazz):

        if not self.dynamic_load_calls:
            self.dynamic_load_calls = {}

        if is_dynamic(method_call['to_class']):
            if method_call['to_class'] in self.dynamic_load_calls:
                self.dynamic_load_calls[method_call['to_class']].append(temp_clazz)
            else:
                self.dynamic_load_calls[method_call['to_class']] = [temp_clazz]

    def proces_safetynet(self, method_call, temp_clazz):
        if not self.safetynet_calls:
            self.safetynet_calls = {}

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


class APKParser:

    def __init__(self, manifest_xml_file, apk_file):
        if manifest_xml_file is None:
            raise TypeError

        self.manifest = manifest_xml_file
        self.apk_file = apk_file
        self.apk = APK(apk_file)
        self.permissions = []
        self.info = {}
        self._parse_apk()

    def _parse_apk(self):
        self.info["package"] = self.apk.package
        self.info["name"] = self.apk.get_app_name()
        self.info["version_name"] = self.apk.version_name
        self.info["version_code"] = self.apk.version_code
        self.info["valid_apk"] = self.apk.valid_apk
        self.info["min_sdk_version"] = self.apk.get_min_sdk_version()
        self.info["max_sdk_version"] = self.apk.get_max_sdk_version()
        self.info["target_sdk_version"] = self.apk.get_target_sdk_version()

    def get_xml(self):
        raw = bytearray(utils.read_file(self.manifest))
        ap = AXMLPrinter(raw)
        return ap.get_xml(pretty=True)

    def get_permissions(self):
        return self.apk.get_permissions()

    def get_services(self):

        services = []

        for svc in self.apk.get_services():
            print(svc)
            services.append({
                'name': svc,
                'intent': self.apk.get_intent_filters("service", svc)
            })

        return self.apk.get_services()

    def get_activities(self):
        activities = []

        for act in self.apk.get_activities():
            print(act)
            activities.append({
                'name': act,
                'intent': self.apk.get_intent_filters("activity", act)
            })

        return activities

    def get_features(self):
        return self.apk.get_features()

    def get_libraries(self):
        return self.apk.get_libraries()


class FileParser:

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


class ManifestParser:

    def __init__(self, xml):
        self.xml = xml
        self.manifest = {
            "activities": [],
            "permissions": [],
            "services": [],
            "features": [],
            "providers": [],
            "receivers": [],
            "meta_data": []
        }
        root = ET.fromstring(xml.decode('utf-8'))
        self._is_namespaced = self._has_android_ns(root)
        self._parse_element(root)

    def get_manifest(self):
        return self.manifest

    def get_manifest_xml(self):
        return self.xml

    def is_obfuscated(self):
        return self._is_namespaced

    def _get_android_NS(self, attrib):
        if self._is_namespaced:
            return attrib

        return "{%s}" % ("http://schemas.android.com/apk/res/android") + attrib

    def _has_android_ns(self, element):
        for child in element:
            ns_name = "{%s}" % ("http://schemas.android.com/apk/res/android") + 'name'
            if ns_name in child.attrib.keys():
                return False
            if 'name' in child.attrib.keys():
                return True

    def _parse_element(self, element):
        try:
            self._parse_activity(element)
            self._parse_permission(element)
            self._parse_service(element)
            self._parse_feature(element)
            self._parse_provider(element)
            self._parse_receiver(element)
            self._parse_meta_data(element)
        except TypeError as e:
            logging.error(e)

        for child in element:
            self._parse_element(child)

    def _parse_activity(self, element):
        if element.tag == "activity":
            ns_name = self._get_android_NS('name')
            self.manifest["activities"].append(
                {
                    'name': element.attrib[ns_name],
                    'intent': self._filter_intent(element, 'activity', element.attrib[ns_name])
                }
            )

    def _parse_permission(self, element):
        ns_name = self._get_android_NS('name')
        if (element.tag == "uses-permission" or element.tag == "permission") and ns_name in element.attrib.keys():
            self.manifest["permissions"].append(element.attrib[ns_name])

    def _parse_service(self, element):
        ns_name = self._get_android_NS('name')
        ns_exported = self._get_android_NS('exported')

        if element.tag == "service":
            self.manifest["services"].append(
                {
                    'name': element.attrib[ns_name],
                    'exported': element.attrib[ns_exported] if ns_exported in element.attrib.keys() else None,
                    'intent': self._filter_intent(element, 'service', element.attrib[ns_name])
                }
            )

    def _parse_feature(self, element):
        ns_name = self._get_android_NS('name')
        if element.tag == "uses-feature" and ns_name in element.attrib.keys():
            self.manifest["features"].append(element.attrib[ns_name])

    def _parse_provider(self, element):
        ns_name = self._get_android_NS('name')
        ns_exported = self._get_android_NS('exported')
        ns_authorities = self._get_android_NS('authorities')

        if element.tag == "provider":
            self.manifest["providers"].append({
                'name': element.attrib[ns_name],
                'exported': element.attrib[ns_exported] if ns_exported in element.attrib.keys() else False,
                'authorities': element.attrib[ns_authorities],
            })

    def _parse_receiver(self, element):

        if element.tag == "receiver":
            ns_name = self._get_android_NS('name')
            ns_exported = self._get_android_NS('exported')
            ns_permission = self._get_android_NS('permission')

            item = {'name': element.attrib[ns_name],
                    'intent': self._filter_intent(element, 'receiver', element.attrib[ns_name])}

            if 'permission' in element.attrib.keys():
                item['permission'] = element.attrib[ns_permission]

            if ns_exported in element.attrib.keys():

                if element.attrib[ns_exported] == 'true':
                    item['exported'] = True
                else:
                    item['exported'] = False

            self.manifest['receivers'].append(item)

    def _parse_meta_data(self, element):
        ns_name = self._get_android_NS('name')
        if element.tag == "meta-data" and ns_name in element.attrib.keys():
            item = {'name': element.attrib[ns_name]}
            for key in element.attrib.keys():
                item[key] = element.attrib[key]
            self.manifest['meta_data'].append(item)

    def _filter_intent(self, element, tagType, name):
        result = {
            'action': [],
            'category': []
        }
        ns_name = self._get_android_NS('name')
        if element.tag == tagType and element.attrib[ns_name] == name:
            for child in element:
                if child.tag == 'intent-filter':
                    intent_filter = child
                    for item in intent_filter:
                        if item.tag == "action":
                            _, temp_action = item.attrib.popitem()
                            result['action'].append(temp_action)
                        if item.tag == "category":
                            _, temp_category = item.attrib.popitem()
                            if temp_category not in result['category']:
                                result['category'].append(temp_category)

        return None if len(result['category']) == 0 and len(result['action']) == 0 else result
