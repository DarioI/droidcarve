# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

from parsers import FileParser, CodeParser, APKParser
import hashlib, os, utils, re
from subprocess import call
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.terminal256 import Terminal256Formatter
from apkid.apkid import Scanner, Options
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
        print("Hash of APK file = " + hash)
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
            print("Unzipping APK ...")
            call(["unzip", self.apk_file, "-d", self.unzip_path])
        else:
            print("Unzipping APK to %s ... " % destination)
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
            print("Start analysis from cache ...")

        print("Analyzing disassembled code ...")
        self.code_parser.start()
        print("Analyzing unzipped files ...")
        self.file_parser.start()

        print("Analyzing AndroidManifest.xml ...")
        self.apk_parser = APKParser(self.file_parser.get_xml("/AndroidManifest.xml"), self.apk_file)
        self.apk_parser.start()
        self.analysis = True
        print("Analyzing ... Done")

    def print_apk_info(self):
        pass

    def print_manifest_info(self, option):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        xml_file = self.file_parser.get_xml("/AndroidManifest.xml")

        if xml_file is None:
            print("AndroidManifest.xml was not found.")
            return

        elif option == "m":
            xml_source = self.apk_parser.get_xml()
            lexer = get_lexer_by_name("xml", stripall=True)
            formatter = Terminal256Formatter()
            print(highlight(xml_source.rstrip(), lexer, formatter))

        elif option == "p":
            for perm in self.apk_parser.get_permissions():
                if not perm.startswith("android."):
                    utils.print_purple("\t" + perm)
                else:
                    print("\t" + perm)
        elif option == "a":
            for activity in self.apk_parser.get_activities():
                print("\t"+activity)
        elif option == "s":
            for service in self.apk_parser.get_services():
                print("\t"+service)
        elif option == "f":
            for feature in self.apk_parser.get_features():
                print("\t"+feature)

    def get_stats(self, shouldPrint=True):
        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        if shouldPrint:
            print('Disassembled classes     = %i' % len(self.code_parser.get_classes()))
            print('Permissions              = %i' % len(self.apk_parser.get_permissions()))
            print('Crypto Operations        = %i' % len(self.code_parser.get_crypto()))
            print('Dynamic Code Loading     = %i' % len(self.code_parser.get_dynamic()))
            print('SafetyNet Calls          = %i' % len(self.code_parser.get_safetynet()))
            print('Hardcoded URLS           = %i' % len(self.code_parser.get_urls()))

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

        safetynet_clazz = self.code_parser.get_safetynet()

        if len(safetynet_clazz) == 0:
            utils.print_blue("No SafetyNet calls found. Maybe they are obfuscated using reflection calls "
                             "or the app simply does not use the SafetyNet API.")
            return

        else:
            utils.prettyprintdict(safetynet_clazz)

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

        urls = self.code_parser.get_urls()

        if len(urls) == 0:
            utils.print_blue("Nu URLs were found.")
            return

        else:
            print(urls)

    def find_crypto_usage(self):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        crypto_classes = self.code_parser.get_crypto()

        if len(crypto_classes) == 0:
            utils.print_blue("No cryptographic calls found. Maybe they are obfuscated using reflection calls, "
                             "an unkown third party has been used or the app simply does not use any crypto.")
            return

        else:
            utils.prettyprintdict(crypto_classes)

    def find_dynamic_loading(self):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        dynamic_classes = self.code_parser.get_dynamic()

        if len(dynamic_classes) == 0:
            utils.print_blue("No dynamic code loading calls found. Maybe they are obfuscated using reflection calls "
                             "or the app simply does not use any dynamic code loading.")
            return

        else:
            utils.prettyprintdict(dynamic_classes)

    def is_excluded(self, candidate):
        for regex in self.excludes:
            pattern = re.compile(regex)
            if pattern.match(candidate):
                return True

        return False

    def print_classes(self, option):

        if not self.analysis:
            print("Please analyze the APK before running this command.")
            return

        args = option.split(" ")
        classes = self.code_parser.get_classes()

        if not option:
            utils.print_blue("Found %s classes" % str(len(classes)))

        if args[0] == "find":
            if len(args) == 1:
                utils.print_red("Please specify a regex to match a class name.")
            else:
                regex = args[1]
                if utils.is_valid_regex(regex):
                    pattern = re.compile(regex)
                    for clazz in classes:
                        if pattern.match(clazz["name"]) and not self.is_excluded(clazz["name"]):
                            print(clazz["name"])
                else:
                    utils.print_red("Invalid regex.")

        elif args[0] == "open":

            clazz_name = args[1]

            for clazz in classes:

                if not clazz_name.endswith(';'):
                    clazz_name = clazz_name + ';'

                if clazz["name"].rstrip("\n") == clazz_name:
                    # print("Opening file: %s " % clazz["file-path"])
                    # scWin = SourceCodeWindow(clazz["file-path"], clazz["name"])
                    # scWin.run()
                    pass

    def disassemble_apk(self):
        print("Disassembling APK ...")
        call(["java", "-jar", BAKSMALI_PATH, "d", self.apk_file, "-o", self.cache_path])

    def analyze_obfuscation(self):
        options = Options(
                        json=True
                    )

        rules = options.rules_manager.load()
        scanner = Scanner(rules, options)
        scanner.scan(self.apk_file)

    def exclude_regex(self, arg):
        if not arg:
            print("Exclusion list:")
            print(self.excludes)
            return

        args = arg.split(" ")

        if args[0] == "clear":
            self.excludes = []
            utils.print_blue("Exclusion list cleared.")
        elif utils.is_valid_regex(args[0]):
            self.excludes.append(args[0])
        else:
            utils.print_red("No valid exclusion regex provided.")