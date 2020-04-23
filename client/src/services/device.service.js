import axios from 'axios';
import { apiConstants } from '../constants';

export const deviceService = {
    getCurrentDevice,
    getDevices,
    connectDevice,
    startLogcat
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