import React from 'react';
import axios from 'axios';
import {baseUrl} from './apiStore';


/**
 * User login logic, those functions are static
 */


const userContext = React.createContext({user: {}});

export const getJWT = (googleResponse) => {
	let tokenId = googleResponse.tokenId;

	return axios.post(`${baseUrl}/api/token/`, { token: tokenId })
		.then(response => response.data)
		.then(token => {
            return getUser(token.access).then(
                result => {
                    var user = result.user;

                    user.access = token.access;
                    user.refresh = token.refresh;

                    return user;
                }
            )
        }).catch(error => {
            console.log("Error: User do not match!", error);
            return {};
        })
};

export const refreshJWT = (refreshToken) => {
	return axios.post(`${baseUrl}/api/token/refresh/`, { refresh: refreshToken })
		.then(response => response.data)
		.then(token => {
            return getUser(token.access).then(
                result => {
                    var user = result.user;

                    user.access = token.access;
                    user.refresh = refreshToken;

                    return user;
                }
            )
        }).catch(error => {
            return {};
        })
};

export const getUser = (token) => {
	let headers = {
		'Authorization': 'Bearer ' + token
	}
	return axios.get(`${baseUrl}/api/token/user/get/`, {headers: headers})
		.then(response => response.data);
};


export { userContext };