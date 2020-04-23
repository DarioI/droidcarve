# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

import hashlib
import logging
import os
import utils
from subprocess import call

from parsers import FileParser, CodeParser, APKParser, ManifestParser

BAKSMALI_PATH = os.getcwd() + "/bin/baksmali.jar"
APK_FILE = ""
CACHE_PATH_SUFFIX = "/cache/"
UNZIPPED_PATH_SUFFIX = "/unzipped/"


class AndroidAnalyzer:

    def __init__(self, apk_file):
        (self.cache_path, self.unzip_path, self.from_cache, self.app_id) = self.generate_cache(apk_file=apk_file)
        self.apk_file = str(apk_file)
        self.file_parser = FileParser(self.unzip_path)
        self.code_parser = CodeParser(self.cache_path)
        self.analysis = False
        self.excludes = []

    def generate_cache(self, apk_file):
        hash = hashlib.sha1(open(apk_file, 'rb').read()).hexdigest()[0:10]
        logging.info("[*] Hash of APK file = " + hash)
        CACHE_PATH = os.getcwd() + "/" + hash + CACHE_PATH_SUFFIX
        UNZIPPED_PATH = os.getcwd() + "/" + hash + UNZIPPED_PATH_SUFFIX

        if os.path.exists(CACHE_PATH) or os.path.exists(UNZIPPED_PATH):
            return CACHE_PATH, UNZIPPED_PATH, True, hash

        if not os.path.exists(CACHE_PATH):
            os.makedirs(CACHE_PATH)

        if not os.path.exists(UNZIPPED_PATH):
            os.makedirs(UNZIPPED_PATH)

        return CACHE_PATH, UNZIPPED_PATH, False, hash

    def get_app_id(self):

        info = self.apk_parser.info
        info["application"] = self.app_id
        return info

    def unzip_apk(self, destination=None):
        if destination is None or destination == "":
            logging.info("[*] Unzipping APK ...")
            call(["unzip", self.apk_file, "-d", self.unzip_path])
        else:
            logging.info("[*] Unzipping APK to %s ... " % destination)
            call(["unzip", self.apk_file, "-d", destination])

    def get_source_tree(self):
        return utils.path_to_dict(self.cache_path)

    def get_source_file(self, key):
        return self.code_parser.get_file_for_hash(key)

    def pre_analyze(self):
        """
        analyze

        Analyze the Android application. Unzip and parse the files, disassemble and process Smali bytecode.
        This step is mandatory before using almost any of the other processing steps.
        """
        if not self.from_cache:
            self.unzip_apk()
            self.disassemble_apk()
        else:
            logging.info("[*] Start analysis from cache ...")

        logging.info("[*] Analyzing disassembled code ...")
        self.code_parser.start()
        logging.info("[*] Analyzing unzipped files ...")
        self.file_parser.start()

        logging.info("[*] Analyzing APK ...")
        self.apk_parser = APKParser(self.file_parser.get_xml("AndroidManifest.xml"), self.apk_file)
        logging.info("[*] Analyzing AndroidManifest_unobfuscated.xml ...")
        self.manifest_parser = ManifestParser(self.apk_parser.get_xml())
        logging.info("[*] Analyzing ... Done")
        self.analysis = True

    def get_manifest_source(self):
        return self.manifest_parser.get_manifest_xml()

    def get_manifest_parsed(self):
        return self.manifest_parser.get_manifest()

    def get_stats(self) -> dict:
        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        return {
            'classes': self.code_parser.get_classes(),
            'permissions': self.apk_parser.get_permissions(),
            'crypto': self.code_parser.get_crypto(),
            'dynamic': self.code_parser.get_dynamic(),
            'safetynet': self.code_parser.get_safetynet(),
            'urls': self.code_parser.get_urls(),
        }

    def find_safetyNet(self):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        return self.code_parser.get_safetynet()

    def print_signature(self):

        files = self.file_parser.get_signature_files()

        if len(files) == 0:
            return None

        for f in files:
            print("Found signature file : " + f)
            call(["keytool", "-printcert", "-file", f])

    def find_urls(self):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        return self.code_parser.get_urls()

    def find_crypto_usage(self):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        return self.code_parser.get_crypto()


    def find_dynamic_loading(self):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        return self.code_parser.get_dynamic()


    def disassemble_apk(self):
        logging.info("[*] Disassembling APK ...")
        call(["java", "-jar", BAKSMALI_PATH, "d", self.apk_file, "-o", self.cache_path])