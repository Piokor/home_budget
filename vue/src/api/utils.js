import axios from 'axios';
import store from '@/store';
import router from '@/router';

const API_URL = "http://localhost:5000/api";

async function postRequest(enpoint, data) {
    return axios({
        method: 'post',
        url: `${API_URL}${enpoint}`,
        data: data,
        headers: {
            "x-access-tokens": store.state.currentUser.token
        }
    }).catch(function (error) {
        if (error.response) {
            if(error.response.status == 440) {            
                //assuming the session was terminated    
                store.commit('signOff');
                router.push('/login?expired=1');
            }
            return {
                data: error.response.data,
                status: error.response.status
            }
        }
    });
}

async function getRequest(enpoint, data) {
    return axios({
        method: "get",
        url: `${API_URL}${enpoint}`,
        params: data,
        headers: {
            "x-access-tokens": store.state.currentUser.token
        }
    }).catch(function (error) {
        if (error.response) {
            if(error.response.status == 440) {            
                //assuming the session was terminated    
                store.commit('signOff');
                router.push('/login?expired=1');
            }
            return {
                data: error.response.data,
                status: error.response.status
            }
        }
    });
}

export {API_URL, getRequest, postRequest}