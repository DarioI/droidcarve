# droidcarve

```
DroidCarve is capable of analyzing an Android APK file and automate certain
reverse engineering tasks. For a full list of features, please see the help
function.

optional arguments:
  -h, --help         show this help message and exit
  -a APK, --apk APK  APK file to analyze
```
## Installation and requirements
This tool is written for Python 2.7 and requires pip.

```shell
git clone https://github.com/DarioI/droidcarve
cd droidcarve
pip install -r requirements.txt
python droidcarve.py -a yourapplication.apk  
```

## Features
* Code disassembling into Smali bytecode
* APK signature extraction
* AndroidManifest parsing: permissions, services, intents, package information etc

## Roadmap
* Code parsing: strings, cryptography, dynamic code loading, native libraries etc.
* Java source code navigation
* ...

## Smali/Baksmali License

The majority of smali/baksmali is written and copyrighted by me (Ben Gruver)
and released under the following license:

*******************************************************************************
Copyright (c) 2010 Ben Gruver (JesusFreke)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*******************************************************************************
