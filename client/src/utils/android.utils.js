const ANDROID_API_REF = "https://developer.android.com/reference/";

export function smaliClassToJava(smaliURL) {
    if(!smaliURL.startsWith("L") || !smaliURL.endsWith(";"))
    {
        console.error("Invalid Smali name: "+smaliURL)
        return smaliURL
    }

    return smaliURL.substring(1, smaliURL.length-1).replace(/\//g, ".")

}

export function isAndroidPackage(packageName)
{
    if (!packageName) return false;

    return (packageName.startsWith("android")
            || packageName.startsWith("java")
            || packageName.startsWith("javax")
            || packageName.startsWith("com/android")
            || packageName.startsWith("dalvik")
        );
}

export function javaPackageToAndroidAPIUrl(javaPkg)
{
    return isAndroidPackage(javaPkg) ? ANDROID_API_REF+javaPkg.replace(/\./g, "/") : javaPkg

}