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
import threading, subprocess
import queue, os


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
        self._logcat_reader = None

    def get_package_list(self, full_info=False):
        if not full_info:
            return self.device.list_packages()
        else:
            pkgs = []
            for p in self.device.list_packages():
                pkgs.append(self.device.package_info(p))
            return pkgs

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

    def start_logcat_interface(self):
        if not self._logcat_reader:
            self._logcat_reader = LogCatInterface(device_serial=self.serial)
            self._logcat_reader.init()

    # with app.app_context():
    #  while self._logcat_reader.hasNext():
    #      line = self._logcat_reader.next()
    #   logging.debug('[%s] - [WS] %s'.format(websocket.LOGCAT_MSG, line))
    # emit(websocket.LOGCAT_MSG, {'data', line})
    # eventlet.sleep(1)

    def get_next_line(self):
        if self._logcat_reader.hasNext():
            return self._logcat_reader.next()
        else:
            return None

    def tear_down_logcat_interface(self):
        self._logcat_reader.stop()
        self._logcat_reader = None

    def download_package(self, packagename, dst):
        full_path = self.device.shell("pm path {}".format(packagename)).split("package:")[1].rstrip("\n")
        self.device.shell("cp {} /sdcard/temp.apk".format(full_path))
        if os.path.exists(dst):
            os.remove(dst)
        self.device.sync.pull("/sdcard/temp.apk", dst)
        return dst


class LogCatInterface:

    def __init__(self, device_serial=None, pkg_name=None):
        self.pkg_name = pkg_name
        self.device_serial = device_serial
        self._proces = None
        self._queue = None
        self._reader = None

    def init(self):
        base_cmd = ['adb']
        if self.device_serial:
            base_cmd.extend(['-s', self.device_serial])

        base_cmd.append('logcat')

        self._process = subprocess.Popen(base_cmd, stdout=subprocess.PIPE)

        # Launch the asynchronous readers of the process' stdout.
        self._queue = queue.Queue()
        self._reader = AsynchronousAdbReader(self._process.stdout, self._queue)
        self._reader.start()

    def next(self):
        return self._queue.get()

    def stop(self):
        self._process.kill()
        self._process = None

    def hasNext(self):
        return self._process and not self._reader.eof()


class AsynchronousAdbReader(threading.Thread):

    def __init__(self, fd, queue):
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

if __name__ == "__main__":
    device = ConnectedDevice(serial="RF8M4050H3A")
    device.download_package("cake.app", "temp.apk")