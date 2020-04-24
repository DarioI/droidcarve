#!/bin/bash

function program_installed {
  local return_=1
  type $1 >/dev/null 2>&1 || { local return_=0; }
  echo "$return_"
}


echo "[*] Installing DroidCarve"
if [ $(program_installed yarn) == 1 ]; then
    echo "[*] Yarn detected"
else
    echo "[*] Installing yarn ... "
    curl -o- -L https://yarnpkg.com/install.sh | bash
fi

echo "[*] Installing node modules"
yarn --cwd client/ install
echo "[*] Building frontend"
yarn --cwd client/ build

if [ $(program_installed adb) == 1 ]; then
    echo "[*] ADB detected"
else
    echo "[*] Installing ADB ... "
    brew cask install android-platform-tools > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[*] Installing ADB ... Done."
    else
        echo "[!!!] Failed to install ADB. Exiting."
        exit 1
    fi
fi

if [ $(program_installed python) == 1 ]; then
    echo "[*] Python detected"
else
    echo "[*] Python 3.4 or older needs to be installed or set as default. Exiting."
    exit 1
fi

source server/venv/bin/activate
pip install --upgrade pip
echo '[*] Installing Python Requirements'
pip install --no-cache-dir -r server/requirements.txt






