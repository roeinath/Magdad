import React, {useContext} from "react";
import {Redirect} from "react-router-dom";
import {Container, Button} from "react-bootstrap";
import {userContext} from "../stores/userContext";
import GoogleLogin from "react-google-login";
import {reactUrl} from "../stores/apiStore";
import {COLORS} from "../constants";
import {isMobileOnly as isMobile} from "react-device-detect";
import LoadingAlert from "./LoadingAlert";
import HebrewLabel from "./HebrewLabel";

const getFirstLetterNames = (full_name)=> {
    return full_name.split(' ').map((word)=>word?word[0]+' ':'').join('')
}

const LoginComponent = () => {
    const {user, loginUser, logoutUser} = useContext(userContext);
    const isLoggedOut = Object.keys(user).length === 0;
    const loginMessage = isMobile? (isLoggedOut ? '':getFirstLetterNames(`${user.name}`))
                                    :(isLoggedOut ? 'התחבר/י' : 'התנתק/י')

    // console.log("login", reactUrl + '/login')

    if (!isLoggedOut)
    {  
        return (<Container style={{width: 'fit-content', paddingRight: '0'}}>
            <Button onClick={logoutUser} variant="outline-light" style={{backgroundColor: COLORS.TALPIOT_CYAN}}>{loginMessage}</Button>
        </Container>);
    } else {
        return (<Container style={{paddingRight: '0'}} dir="ltr">
            <GoogleLogin
                clientId="330244991572-iimj6mtoao2motr1c05oklic54oo50vb.apps.googleusercontent.com"
                buttonText={loginMessage}
                uxMode='redirect'
                redirectUri={reactUrl + '/login'}
                cookiePolicy={'single_host_origin'}
                style={{width: 'fit-content'}}
            />
        </Container>);
    }
};

const LoginParseRedirectFromGoogle = (props) => {
    if (Object.keys(props.user).length === 0) {
        let afterhash = window.location.hash.substr(1);
        let key = afterhash.split("id_token=")[1].split("&login_hint=")[0];

        props.loginUser({tokenId: key});

        return <Container>
            <h1>מתחבר לשרת</h1>
            <Container style={{width: '50%'}}>
                {LoadingAlert}
            </Container>
            <HebrewLabel color="#888">לא אמור לקחת יותר מ5 שניות</HebrewLabel>
        </Container>;

    } else {
        return <Redirect to="/react" />;
    } 
};

export {LoginParseRedirectFromGoogle};

export default LoginComponent;