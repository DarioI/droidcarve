const BASE_URL = 'http://localhost:1337';

export const apiConstants = {

    SERVER_STATUS: BASE_URL+'/',
    GENERAL_STATUS: BASE_URL+'/status',

    // APP API
    CURRENT_APPLICATION: BASE_URL+'/app/',
    SET_CURRENT_APPLICTION: BASE_URL+'/app/upload',
    DUMP_APPLICATION: BASE_URL+'/app/dump',
    APP_STATISTICS: BASE_URL+'/app/stats',

    // SOURCE API
    SOURCE_TREE: BASE_URL+'/source/tree',

    // FILE API
    GET_FILE: BASE_URL+'/file/download',

    // DEVICE API
    CURRENT_DEVICE: BASE_URL+'/device/',
    LIST_DEVICE: BASE_URL+'/device/list',
    CONNECT_DEVICE: BASE_URL+'/device/connect',
    PACKAGES_LIST: BASE_URL+'/device/packages',

    // LOGCAT API
    START_LOGCAT: BASE_URL+'/logcat/start',
    STOP_LOGCAT: BASE_URL+'/logcat/stop',

    // MANIFEST API
    GET_MANIFEST: BASE_URL+'/manifest/view',
    GET_MANIFEST_OVERVIEW: BASE_URL+'/manifest/overview'
}
