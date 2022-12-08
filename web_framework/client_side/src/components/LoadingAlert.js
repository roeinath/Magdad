import React from "react";
import {Alert, Spinner} from "react-bootstrap";

const LoaderText = '...טוען';
export default (
    <Alert variant="primary" style={{margin: 0, padding: 0}}>
        <Alert.Heading>{LoaderText}</Alert.Heading>
        <hr/>
        {/*<Spinner animation="border" variant="dark"/>*/}
        <img src={process.env.PUBLIC_URL + "/talpiX-logo-new.png"} alt="logo" width="100vw"
             style={{marginBottom: '3vh', animation: '0.8s cubic-bezier(0.65, 0.05, 0.36, 1) infinite alternate spinner-grow'}}/>
    </Alert>
);


