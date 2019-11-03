# This file is part of DroidCarve.
#
# Copyright (C) 2019, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

import lief
import zipfile
import shutil
import subprocess
import tempfile
import os
import pathlib
import requests
import re

gadget_architecture = {
    "arm64": "android-arm64.so",
    "arm64-v8a": "android-arm64.so",
    "armeabi": "android-arm.so",
    "armeabi-v7a": "android-arm.so",
    "x86": "android-x86.so",
    "x86_64": "android-x86_64.so"
}


class Injector:

    def __init__(self, unzipped_path, adb_device):
        self.unzip_path = unzipped_path
        self.adb_device

    def inject(self, libdir, arch, selected_library):
        # Get latests frida-gadgets
        latest = requests.get(url="https://github.com/frida/frida/releases/latest")

        # Get stable frida-gadgets
        # latest = requests.get(url = "https://github.com/frida/frida/releases/tag/12.5.4")

        response = latest.content.decode('utf-8')
        latestArch = re.findall(r'\/frida\/frida\/releases\/download\/.*\/frida-gadget.*\-android\-.*xz', response)
        url_gadget = ""
        for i in latestArch:
            if gadget_architecture[arch] in i:
                url_gadget = i

        print("[+] Downloading and extracting frida gadget for: " + arch)
        url = 'https://github.com' + str(url_gadget)
        r = requests.get(url)
        filename = "frida-gadget" + str(arch) + ".so.xz"
        with open(libdir / arch / filename, 'wb') as f:
            f.write(r.content)
        #xtract(str(libdir / arch / filename))
        gadget_name = "libgdgt.so"
        os.rename(libdir / arch / filename[:-3], libdir / arch / gadget_name)
        os.remove(libdir / arch / filename)
        print(f"[+] Injecting {gadget_name} into {arch}/{selected_library} \n")
        libcheck_path = libdir / arch / selected_library
        libcheck = lief.parse(libcheck_path.as_posix())
        libcheck.add_library(gadget_name)
        libcheck.write(libcheck_path.as_posix())

    def get_system_architecture(self):
        pass

