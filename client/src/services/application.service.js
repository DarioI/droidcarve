import axios from 'axios';
import { apiConstants } from '../constants';

export const appService = {
    getCurrentApplication,
    getAnalysisOverview,
};


function getCurrentApplication()
{
    return axios.get(apiConstants.CURRENT_APPLICATION);
}

function getAnalysisOverview()
{
    return axios.get(apiConstants.APP_STATISTICS);
}
