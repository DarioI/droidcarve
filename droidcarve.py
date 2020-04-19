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

import os
from analyzer import AndroidAnalyzer
import adb_interface


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
        print("Checking {}".format(filepath))
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

    def get_device(self):
        if not self.connected_device:
            return {
                'device': None
            }

        return {
            'device': self.connected_device.get_info_dict()
        }

    def get_device_list(self):

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

    def connect_device(self, serial):

        if not serial:
            return None

        else:
            self.connected_device = adb_interface.ConnectedDevice(serial=serial)
            return self.connected_device.get_info_dict()
