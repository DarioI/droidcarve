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

import os, argparse, fnmatch
from cmd import Cmd
from subprocess import call

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

BAKSMALI_PATH = os.getcwd() + "/bin/baksmali.jar"
APK_FILE = ""
CACHE_PATH = os.getcwd() + "/cache/"
UNZIPPED_PATH = os.getcwd() + "/unzipped/"


class DroidCarve(Cmd):

    def __init__(self, apk_file):
        Cmd.__init__(self)
        self.prompt = "DC $> "
        self.apk_file = str(apk_file)

    def do_help(self, arg):
        print "help yoo"

    def do_quit(self, arg):
        print 'Exiting, cheers!'
        exit(0)

    def do_exit(self, arg):
        self.do_quit(arg)

    def do_analyze(self, arg):
        print "Analyzing ..."
        self.unzip_apk()
        self.disassemble_apk()
        print "Analyzing ... Done"

    def do_statistics(self, arg):
        onlyfiles = len(fnmatch.filter(os.listdir(CACHE_PATH), '*.smali'))
        print 'Disassembled classes = '+str(onlyfiles)

    '''
    Use baksmali to disassemble the APK.
    '''
    def disassemble_apk(self):
        print "Disassembling APK ..."
        call(["java", "-jar", BAKSMALI_PATH, "d", self.apk_file, "-o", CACHE_PATH])

    def unzip_apk(self):
        print "Unzipping APK ..."
        call(["unzip", self.apk_file,"-d", UNZIPPED_PATH])

    def extract_strings(self):
        return

'''
Parse the arguments and assign global variables that we will be using throughout the tool.
'''
def parse_arguments():
    parser = argparse.ArgumentParser(description='DroidCarve is capable of analyzing an Android APK file and automate certain reverse engineering tasks. For a full list of features, please see the help function.')
    parser.add_argument('-a', '--apk', type=str, help='APK file to analyze',
                        required=True)

    args = parser.parse_args()

    global APK_FILE
    APK_FILE = args.apk


'''
Sanity check to see if a valid APK file is specified.

TODO: implement more specific check to see if it is a valid APK file
'''
def check_apk_file():
    if APK_FILE == "" or not os.path.isfile(APK_FILE):
        print "No APK file specified, exiting."
        exit(3)


'''
Check if there is a baksmali tool.
'''


def has_baksmali():
    return os.path.isfile(BAKSMALI_PATH)


def main():
    parse_arguments()
    droidcarve = DroidCarve(APK_FILE)
    droidcarve.cmdloop()


if __name__ == "__main__":

    if not has_baksmali():
        print "No baksmali.jar found in " + BAKSMALI_PATH
        exit(2)

    main()
