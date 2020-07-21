import axios from 'axios';
import { apiConstants } from '../constants';

export const deviceService = {
    getCurrentDevice,
    getDevices,
    connectDevice,
    startLogcat,
    getPackages,
    dumpAnalyze,
};


function getCurrentDevice()
{
    return axios.get(apiConstants.CURRENT_DEVICE);
}

function getDevices()
{
    return axios.get(apiConstants.LIST_DEVICE);
}

function connectDevice(serial)
{
    return axios.post(apiConstants.CONNECT_DEVICE, {'serial': serial});
}

function startLogcat()
{
    return axios.get(apiConstants.START_LOGCAT);
}

function getPackages()
{
    return axios.get(apiConstants.PACKAGES_LIST)
}

function dumpAnalyze(pckgName)
{
    return axios.post(apiConstants.DUMP_APPLICATION, {'package_name': pckgName})
}