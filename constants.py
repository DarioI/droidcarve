CALLING_OPCODES = [
    'invoke-virtual',
    'invoke-super',
    'invoke-direct',
    'invoke-static',
    'invoke-interface',
    'invoke-custom'
]

CRYPTO_CLASSES = [
    'Ljavax/crypto/Cipher',
    'Ljavax/crypto/SecretKey',
    'Ljavax/crypto/spec/SecretKeySpec',
    'Ljavax/crypto/spec/PBEKeySpec',
    'Lorg/spongycastle/jce/provider/BouncyCastleProvider'
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
