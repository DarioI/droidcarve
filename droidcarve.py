# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#
from adbutils import AdbError

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

import os, argparse, json
import utils
from cmd import Cmd
from analyzer import AndroidAnalyzer
import adb_interface

BAKSMALI_PATH = os.getcwd() + "/bin/baksmali.jar"


class DroidCarve(Cmd):

    def __init__(self, apk_file=None):
        Cmd.__init__(self)
        self.prompt = "DC $> "
        self.connected_device = None
        self.androidAnalyzer = None
        if apk_file:
            self.androidAnalyzer = AndroidAnalyzer(apk_file)
            self.androidAnalyzer.pre_analyze()
        else:
            utils.print_blue("Start by connecting a device over ADB or load an APK. See 'help device' or 'help apk' "
                             "for a complete list of commands 'help'. Happy hacking!")

    def do_quit(self, arg):
        print('Exiting, cheers!')
        exit(0)

    def do_exit(self, arg):
        self.do_quit(arg)

    def do_unzip(self, destination):
        """
        unzip

        Unzip the Android application in the working cache.

        unzip [destination]

        Unzip the Android application to a given destination.
        """
        self.androidAnalyzer.unzip_apk(destination)

    def do_crypto(self, arg):

        """
        crypto

        Print classes where cryptographic calls have been found.
        """

        self.androidAnalyzer.find_crypto_usage()

    def do_dynamic(self, arg):
        """
        dynamic

        Print classes where dynamic code loading calls have been found.
        """

        self.androidAnalyzer.find_dynamic_loading()

    def do_urls(self, arg):
        """
        urls

        Print urls that have been found have been found.
        """

        self.androidAnalyzer.find_urls()

    def do_safetynet(self, arg):
        """
        safetynet

        Print classes where SafetyNet calls have been found.
        """

        if not self.androidAnalyzer:
            utils.print_red("[!!!] Currently no APK has been set for analysis.")
            return

        self.androidAnalyzer.find_safetyNet()

    def do_exclude(self, arg):

        """
        exclude

        List the current list of exclusion filters.

        exclude [regex]

        Add a given regex to the exclusion list. All the classes or methods that match this regex will be excluded from
        results that are printed to the command line.

        exclude clear

        Clear the current list of regexes.
        """

        self.androidAnalyzer.exclude_regex(arg)

    def do_signature(self, arg):
        """
        signature

        Print the application certificate in a human readable format.
        This requires that the Java keytool binary is installed and in PATH.

        In case no signature is found, make sure the application is signed and the 'analyze' is executed.
        """

        if not self.androidAnalyzer:
            utils.print_red("[!!!] Currently no APK has been set for analysis.")
            return

        self.androidAnalyzer.print_signature()

    def do_statistics(self, arg):

        """
        statistics

        Print some statistics about the Android application.
        """

        if not self.androidAnalyzer:
            utils.print_red("[!!!] Currently no APK has been set for analysis.")
            return

        self.androidAnalyzer.print_statistics()

    def do_about(self, arg):

        """
        about

        About DroidCarver
        """
        utils.print_blue(
            "DroidCarver is a hobby project of Dario Incalza (@h4oxer) <dario.incalza@gmail.com>. A mobile security "
            "and hardware security enthousiast.")

    def do_device(self, arg):

        """
        device

        Check the current connected device.

        device info

        Get information about the currently connected ADB device.

        device connect

        Connect with a device over ADB.

        device disconnect

        Disconnect with the current connected device over ADB.

        device dump-apk

        Dump an APK that is currently installed on the device.
        """

        args = arg.split(" ")

        if not arg:
            if self.connected_device:
                utils.print_blue(
                    "Currently connected device with serial number: {}".format(self.connected_device.get_serial()))
                return
            else:
                utils.print_red("No device has been connected to DroidCarver. Use 'device connect' to start "
                                "connecting a device.")
                return

        if args[0] == "disconnect":
            if self.connected_device:
                utils.print_blue("Disconnecting device {} ...".format(self.connected_device.get_serial()))
                self.connected_device = None
                utils.print_blue("Disconnecting done.")
                return
            else:
                utils.print_purple("Nothing to disconnect here.")
                return

        if args[0] == "info":
            try:
                if self.connected_device:
                    utils.print_blue(json.dumps(self.connected_device.get_info_dict(), indent=2))
                else:
                    utils.print_red("No device has been connected to DroidCarver. Use 'device connect' to start "
                                    "connecting a device.")
                    return
            except AdbError:
                self.connected_device = None
                utils.print_red("[!!!] Connection error. Did you disconnect the device?")

        if args[0] == "connect":
            return self._connect_to_device()

        if args[0] == "dump-apk":
            if self.connected_device:
                pkg_name = utils.ask_question("What package do you want to dump?", self.connected_device.get_packages())
                utils.print_blue("[*] selected package {} for analysis".format(pkg_name))
                return
            else:
                utils.print_red("No device has been connected to DroidCarver. Use 'device connect' to start "
                                "connecting a device.")
                return

    def _connect_to_device(self):
        if self.connected_device:
            utils.print_purple("Already connected to device {}, please first disconnect.".format(
                self.connected_device.get_serial()))
            return
        else:
            device_list = [d.serial for d in adb_interface.get_devices()]

            if len(device_list) == 0:
                utils.print_purple(
                    "No connected devices were found, make sure to check the USB connection and whether ADB is turned "
                    "on.")
                return
            choice = utils.ask_question("Which device would you like to connect to DroidCarver?", device_list)
            try:
                self.connected_device = adb_interface.ConnectedDevice(serial=choice)
                utils.print_blue("Connected to device {}".format(choice))
                return
            except RuntimeError as e:
                print(e)
                utils.print_red("Could not connect to device {}".format(choice))
                return

    def do_apk(self, arg):
        """
        apk

        Print the APK in the current working context.

        apk set [path to apk]

        Change APK in the current working context.

        apk m
        Print a readable AndroidManifest.xml

        apk p
        List of extracted permissions.

        apk s
        List of extracted services.

        apk a
        List of extracted activities.

        """

        args = arg.split(" ")

        if not arg:
            if not self.androidAnalyzer:
                utils.print_red("[!!!] Currently no APK has been set for analysis.")
            else:
                utils.print_blue(self.androidAnalyzer)

        elif args[0] == "set":
            if len(args) > 1 and os.path.exists(args[1]):
                self.androidAnalyzer = AndroidAnalyzer(apk_file=args[1])
                self.androidAnalyzer.pre_analyze()
            else:
                utils.print_purple("[!!!] Please give a valid APK filepath.")
        elif args[0] == "id":
            if not self.androidAnalyzer:
                utils.print_red("[!!!] Currently no APK has been set for analysis.")
            else:
                self.androidAnalyzer.analyze_obfuscation()

        elif args[0]:
            if not self.androidAnalyzer:
                utils.print_red("[!!!] Currently no APK has been set for analysis.")
                return
            self.androidAnalyzer.print_manifest_info(arg)

    def do_classes(self, arg):

        """
        classes

        Print how much classes are disassembled.

        classes find [regex]

        Print the disassembled classes that match the regex.
        """
        if not self.androidAnalyzer:
            utils.print_red("[!!!] Currently no APK has been set for analysis.")
            return

        self.androidAnalyzer.print_classes(arg)


'''
Parse the arguments and assign global variables that we will be using throughout the tool.
'''


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='DroidCarve is capable of analyzing an Android APK file and automate certain reverse engineering '
                    'tasks. For a full list of features, please see the help function.')
    parser.add_argument('-a', '--apk', type=str, help='APK file to analyze',
                        required=False)

    args = parser.parse_args()

    global APK_FILE
    APK_FILE = args.apk

    if APK_FILE:
        check_apk_file()
        return APK_FILE
    else:
        return None


'''
Sanity check to see if a valid APK file is specified.

TODO: implement more specific check to see if it is a valid APK file
'''


def check_apk_file():
    if APK_FILE == "" or not os.path.isfile(APK_FILE):
        print("No APK file specified, exiting.")
        exit(3)


'''
Check if there is a baksmali tool.
'''


def has_baksmali():
    return os.path.isfile(BAKSMALI_PATH)


def main():
    set_logging()
    apk_file = parse_arguments()
    droidcarve = DroidCarve(apk_file)
    droidcarve.cmdloop()


def set_logging():
    import logging
    logging.basicConfig(level=logging.ERROR)


if __name__ == "__main__":

    utils.print_welcome()
    if not has_baksmali():
        print("No baksmali.jar found in " + BAKSMALI_PATH)
        exit(2)

    if not utils.adb_available():
        utils.print_red("[!!!] ADB not found. Features that need a connected Android device won't work. Please "
                        "install ADB before using DroidCarve.")
    main()
