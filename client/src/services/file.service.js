import axios from 'axios';
import { apiConstants } from '../constants';

export const fileService = {
    getFile,
    getFileTree
};


function getFile(key)
{
    return axios.get(apiConstants.GET_FILE+'/'+key);
}

function getFileTree()
{
    return axios.get(apiConstants.GET_FILE_TREE);
}