# This file is part of DroidCarve.
#
# Copyright (C) 2020, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#

__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

CALLING_OPCODES = [
    'invoke-virtual',
    'invoke-super',
    'invoke-direct',
    'invoke-static',
    'invoke-interface',
    'invoke-custom'
]

CRYPTO_CLASSES = [
    'Ljavax/crypto/Cipher;',
    'Ljavax/crypto/SecretKey;',
    'Ljavax/crypto/Mac;',
    'Ljavax/crypto/KeyGenerator;',
    'Ljavax/crypto/KeyAgreement;',
    'Ljavax/crypto/spec/SecretKeySpec;',
    'Ljavax/crypto/spec/PBEKeySpec;',
    'Lorg/spongycastle/jce/provider/BouncyCastleProvider;',
    'Lcom/android/security/KeyChain;',
    'Landroidx/security/crypto/EncryptedFile;',
    'Landroidx/security/crypto/MasterKey',
]

DYNAMIC_LOADING_CLASSES = [
    'Ldalvik/system/PathClassLoader',
    'Ldalvik/system/BaseDexClassLoader',
    'Ldalvik/system/InMemoryDexClassLoader',
    'Ljava/net/URLClassLoader',
    'Ljava/security/SecureClassLoader'
]

SAFETYNET_CLASSES = [
    'Lcom/google/android/gms/safetynet/SafetyNetClient',
    'Lcom/google/android/gms/safetynet/SafetyNetApi'
]

CLASS_ANNOTATION = '.class'
INTERFACE_ANNOTATION = '.implements'
ANNOTATION = ".annotation"
END = ".end"
SOURCE_ANNOTATION = '.source'
SUPER_ANNOTATION = ".super"
