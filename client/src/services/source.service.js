import axios from 'axios';
import { apiConstants } from '../constants';

export const sourceService = {
    getSourceTree,
};


function getSourceTree()
{
    return axios.get(apiConstants.SOURCE_TREE);
}
