import axios from 'axios';

export const API_URL = "http://localhost:5000/api";
export {register, login}


async function register(username, password) {
    return axios({
        method: 'post',
        url: `${API_URL}/register`,
        data: {
            name: username,
            password: password
        }
    }).catch(function (error) {
        if (error.response) {
            return {
                data: error.response.data,
                status:error.response.status
            }
        }
    });
}

async function login(username, password) {
    return axios({
        method: 'post',
        url: `${API_URL}/login`,
        data: {
            username: username,
            password: password
        }
    }).catch(function (error) {
        if (error.response) {
            return {
                data: error.response.data,
                status:error.response.status
            }
        }
    });
}