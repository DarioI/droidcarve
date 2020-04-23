import axios from 'axios';
import { apiConstants } from '../constants';

export const manifestService = {
    getManifestXML,
    getOverview
};


function getManifestXML()
{
    return axios.get(apiConstants.GET_MANIFEST);
}

function getOverview()
{
    return axios.get(apiConstants.GET_MANIFEST_OVERVIEW);
}