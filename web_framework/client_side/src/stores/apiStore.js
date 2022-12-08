import {METHODS} from "../constants";
import axios from 'axios';
import createAuthRefreshInterceptor from 'axios-auth-refresh';
import {refreshJWT} from './userContext';

//const axiosInstance = axios.create({timeout: 200000});
const axiosInstance = axios.create();
// const axiosInstance = axios.create({timeout: 200000});


let _baseUrl = "";
let _reactUrl = "";

if (process.env.REACT_APP_IS_PRODUCTION === "0")
{
    _baseUrl = process.env.PUBLIC_URL.replace('/react', 'http://localhost:8000'); //'https://bot.talpiot.org'
    _reactUrl = process.env.PUBLIC_URL.replace('/react', 'http://localhost:3000/react'); 
} else {
    _baseUrl = process.env.PUBLIC_URL.replace('/react', '/new/server');
    _reactUrl = process.env.PUBLIC_URL;
}

export const baseUrl = _baseUrl;
export const reactUrl = _reactUrl;
// 'http://192.168.137.1:4243' // 'http://127.0.0.1:5000'; //

// console.log("BURL", baseUrl);
// console.log("BURL", process.env.REACT_APP_IS_PRODUCTION);

// Function that will be called to refresh authorization
export const configureRefreshAuthLogic = (app) => {
    const refreshAuthLogic = failedRequest => {
        let isLoggedOut = Object.keys(app.state.user).length === 0;

        if (isLoggedOut) {
            console.log("Logged out.");
            return Promise.resolve();
        }

        let refreshToken = app.state.user.refresh;

        return refreshJWT(refreshToken).then(
            user => {
                failedRequest.response.config.headers['Authorization'] = 'Bearer ' + user.access;

                app.updateCurrentUser(user);

                return Promise.resolve();
            }
        );
    }
    
    createAuthRefreshInterceptor(axiosInstance, refreshAuthLogic);
}

const getAllUrlParams = (url) => {

    // get query string from url (optional) or window
    var queryString = url ? url.split('?')[1] : window.location.search.slice(1);

    // we'll store the parameters here
    var obj = {};

    // if query string exists
    if (queryString) {

        // stuff after # is not part of query string, so get rid of it
        queryString = queryString.split('#')[0];

        // split our query string into its component parts
        var arr = queryString.split('&');

        for (var i = 0; i < arr.length; i++) {
            // separate the keys and the values
            var a = arr[i].split('=');

            // set parameter name and value (use 'true' if empty)
            var paramName = a[0];
            var paramValue = typeof (a[1]) === 'undefined' ? true : a[1];

            // (optional) keep case consistent
            paramName = paramName.toLowerCase();
            if (typeof paramValue === 'string') paramValue = paramValue.toLowerCase();

            // if the paramName ends with square brackets, e.g. colors[] or colors[2]
            if (paramName.match(/\[(\d+)?\]$/)) {

                // create key if it doesn't exist
                var key = paramName.replace(/\[(\d+)?\]/, '');
                if (!obj[key]) obj[key] = [];

                // if it's an indexed array e.g. colors[2]
                if (paramName.match(/\[\d+\]$/)) {
                    // get the index value and add the entry at the appropriate position
                    var index = /\[(\d+)\]/.exec(paramName)[1];
                    obj[key][index] = paramValue;
                } else {
                    // otherwise add the value to the end of the array
                    obj[key].push(paramValue);
                }
            } else {
                // we're dealing with a string
                if (!obj[paramName]) {
                    // if it doesn't exist, create property
                    obj[paramName] = paramValue;
                } else if (obj[paramName] && typeof obj[paramName] === 'string'){
                    // if property does exist and it's a string, convert it to an array
                    obj[paramName] = [obj[paramName]];
                    obj[paramName].push(paramValue);
                } else {
                    // otherwise add the property
                    obj[paramName].push(paramValue);
                }
            }
        }
    }

    return obj;
}

//export const fetchMainPage = async () => fetchApi('/get_page/?name=FIRST_MVP');
export const fetchPage = (name, login, params, cancelSource = null) => fetchApi('/get_page/?name='+name+'&params='+params, login, null, cancelSource);


//fetches the json data from the server side
export const fetchApi = async (apiUrl, login,  data = null, cancelSource = null) => {
    var options = {};

    if (cancelSource != null) {
        options['cancelToken'] = cancelSource.token;
    }

	if (login != null) {
		options['headers'] = {
            'Authorization': 'Bearer ' + login.access
        };
	}

    const url = `${baseUrl}${apiUrl}`;

    if (data != null)
    {
        // options.params = data;
        const urlParams = getAllUrlParams(url)
        return axiosInstance.post(url.split('?')[0], Object.assign(urlParams, data), options);
    }

    return axiosInstance.get(url, options);
};


