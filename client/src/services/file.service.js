import axios from 'axios';
import { apiConstants } from '../constants';

export const fileService = {
    getFile,
};


function getFile(key)
{
    return axios.get(apiConstants.GET_FILE+'/'+key);
}