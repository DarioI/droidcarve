# This file is part of DroidCarve.
#
# Copyright (C) 2019, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

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

    def get_serial(self):
        return self.serial

    def get_prop(self, propstr):
        return str(self.device.shell(["getprop", propstr]))

    def get_info_dict(self):

        return {
            "Serial": self.device.serial,
            "Name": self.get_prop("ro.product.name"),
            "Manufacturer": self.get_prop("ro.product.manufacturer"),
            "Model": self.get_prop("ro.product.model"),
            "Android Version": self.get_prop("ro.build.version.release"),
            "API Level": self.get_prop("ro.build.version.sdk"),
            "CPU Architecture": self.get_prop("ro.arch"),
            "CPU ABI": self.get_prop("ro.product.cpu.abi"),
            "Crypto State": self.get_prop("ro.crypto.state"),
            "FDE Algorithm": self.get_prop("ro.crypto.fde_algorithm"),
            "Latest Security Patch": self.get_prop("ro.build.version.security_patch")
        }
