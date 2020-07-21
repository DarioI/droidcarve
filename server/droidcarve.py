# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

import os
from analyzer import AndroidAnalyzer
import adb_interface
from adb_interface import ConnectedDevice


class AnalysisController:

    def __init__(self):
        self.apk_analyzer = None

    def get_application(self):

        if not self.apk_analyzer:
            return {
                "application": None
            }

        return self.apk_analyzer.get_app_id()

    def set_application(self, filepath):
        print("[*] Checking {}".format(filepath))
        if os.path.exists(filepath):
            self.apk_analyzer = AndroidAnalyzer(apk_file=filepath)
            self.apk_analyzer.pre_analyze()
        else:
            raise AttributeError("Non valid APK supplied.")

    def get_statistics(self):

        if not self.apk_analyzer:
            raise AttributeError("No application has been selected.")

        return self.apk_analyzer.get_stats()

    def get_source_tree(self):
        if not self.apk_analyzer:
            raise AttributeError("No application has been selected.")

        return self.apk_analyzer.get_source_tree()

    def get_source_file_path(self, key):
        if not self.apk_analyzer:
            raise AttributeError("No application has been selected.")

        return self.apk_analyzer.get_source_file(key)

    def get_manifest_source(self):
        if not self.apk_analyzer:
            raise AttributeError("No application has been selected.")

        return self.apk_analyzer.get_manifest_source()

    def get_manifest_overview(self):
        if not self.apk_analyzer:
            raise AttributeError("No application has been selected.")

        return self.apk_analyzer.get_manifest_parsed()


class DeviceController:

    def __init__(self):
        self.connected_device = None

    def get_device(self) -> dict:
        if not self.connected_device:
            return {
                'device': None
            }

        return {
            'device': self.connected_device.get_info_dict()
        }

    def get_device_list(self) -> dict:

        device_list = [{'serial': d.serial, 'name': d.shell(["getprop", "ro.product.model"])} for d in
                       adb_interface.get_devices()]

        if len(device_list) == 0:
            return {
                'devices': None
            }
        else:
            return {
                'devices': device_list
            }

    def get_package_list(self):
        if not self.connected_device:
            raise AttributeError("No connected device")

        return self.connected_device.get_package_list()

    def connect_device(self, serial: str):

        if not serial:
            return None

        else:
            self.connected_device = ConnectedDevice(serial=serial)
            return self.connected_device.get_info_dict()

    def start_logcat(self):

        if not self.connected_device:
            raise AttributeError("No connected device")

        self.connected_device.start_logcat_interface()

    def next_logcat_line(self):
        if not self.connected_device:
            raise AttributeError("No connected device")

        return self.connected_device.get_next_line()

    def stop_logcat(self):
        if not self.connected_device:
            raise AttributeError("No connected device")

        self.connected_device.tear_down_logcat_interface()

    def download_package(self, packagename, dst):
        if not self.connected_device:
            raise AttributeError("No connected device")

        self.connected_device.download_package(packagename, dst)

