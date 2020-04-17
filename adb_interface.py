# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

from adbutils import adb


def get_devices():
    return adb.device_list()


def get_device(serial):
    return adb.device(serial)


class ConnectedDevice:

    def __init__(self, serial):
        if serial is None:
            raise RuntimeError("No connected device configured.")
        self.device = get_device(serial)
        self.serial = self.device.serial

    def get_packages(self):
        return self.device.list_packages()

    def download_package(self):
        pass

    def get_serial(self):
        return self.serial

    def get_prop(self, propstr):
        return str(self.device.shell(["getprop", propstr]))

    def get_info_dict(self):

        return {
            "serial": self.device.serial,
            "name": self.get_prop("ro.product.name"),
            "manufacturer": self.get_prop("ro.product.manufacturer"),
            "model": self.get_prop("ro.product.model"),
            "android_version": self.get_prop("ro.build.version.release"),
            "api_level": self.get_prop("ro.build.version.sdk"),
            "cpu_arch": self.get_prop("ro.arch"),
            "cpu_abi": self.get_prop("ro.product.cpu.abi"),
            "crypto_state": self.get_prop("ro.crypto.state"),
            "fde_algorithm": self.get_prop("ro.crypto.fde_algorithm"),
            "latest_security_patch": self.get_prop("ro.build.version.security_patch")
        }
