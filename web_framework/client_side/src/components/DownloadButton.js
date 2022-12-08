import React from 'react';
import Button from "./Button";
import {fetchApi} from "../stores/apiStore";
import {userContext} from "../stores/userContext";
import axios from "axios";


export default ({text, actionUrl, name: filename, filepath, ...props}) => {
    const onClick = (user) => {
        fetchApi(actionUrl, user,null, axios.CancelToken.source()).then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', filename); //or any other extension
                document.body.appendChild(link);
                link.click();
            }
        );
    }
    return <userContext.Consumer>
        {({user}) => <Button text={text} onClick={() => { onClick(user); }} {...props}></Button>}
    </userContext.Consumer>;
};
