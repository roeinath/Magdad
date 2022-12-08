import 'bootstrap/dist/css/bootstrap.css';

import React from 'react';
import {BrowserRouter as Router, Redirect, Route} from "react-router-dom";
import ReactDOM from 'react-dom';

import './index.css';
import Main from './Main';
import {userContext, getJWT, refreshJWT} from './stores/userContext';
import {configureRefreshAuthLogic} from './stores/apiStore';
import Switch from "react-bootstrap/Switch";
import {LoginParseRedirectFromGoogle} from './components/LoginComponent';


const LOGGED_IN_USER_DATA_ITEM = 'loggedInUser';


/**
 * The manages top level routing, and user login.
 */

class App extends React.Component {
    constructor(props) {
        super(props);

        let saved = JSON.parse(localStorage.getItem(LOGGED_IN_USER_DATA_ITEM));

        this.state = {
            user: saved || {}
        };

        this.updateCurrentUser = this.updateCurrentUser.bind(this);
        this.validateLogin = this.validateLogin.bind(this);
        this.loginUser = this.loginUser.bind(this);
        this.logoutUser = this.logoutUser.bind(this);

        configureRefreshAuthLogic(this);
        this.validateLogin(saved);
    }

    validateLogin(savedUser) {
        if (savedUser == null) {
            return;
        }

        refreshJWT(savedUser.refresh).then(this.updateCurrentUser);
    }

    loginUser(googleResponse) {
        getJWT(googleResponse).then(this.updateCurrentUser);
    }

    updateCurrentUser(newUser) {
        this.setState({user: newUser});

        localStorage.setItem(LOGGED_IN_USER_DATA_ITEM, JSON.stringify(newUser));


    }

    logoutUser() {
        this.setState({
            user: {}
        });

        localStorage.removeItem(LOGGED_IN_USER_DATA_ITEM);
    }

    componentDidMount() {

    }

    render() {
        const value = {
            user: this.state.user,
            loginUser: this.loginUser,
            logoutUser: this.logoutUser
        };

        return (
            <div style={{height: '100%', width: '100%'}}>
                <userContext.Provider value={value}>
                    <Router>
                        <Switch style={{padding: '5rem 0', height: '100%', width: '100%'}}>
                            <Route exact path="/react">
                                <Redirect to="/react/page/front" />;
                            </Route>
                            <Route path="/react/login">
                                <LoginParseRedirectFromGoogle user={value.user} loginUser={value.loginUser} />
                            </Route>
                            <Route exact path="/react/page/:id" render={({ match }) => {
                                // Do whatever you want with the match...
                                if(match.params.id.includes('/')) {
                                    return null;
                                }
                                return <Main params={match.params} />
                            }}/>
                            <Route path="/react/page/:id/:params" render={({ match }) => {
                                // Do whatever you want with the match...
                                console.log(match.params);
                                return <Main params={match.params} />
                            }}/>
                        </Switch>
                    </Router>
                </userContext.Provider>
            </div>
        );
    }
}

export default App;
ReactDOM.render(
    <App/>
    , document.getElementById('root'));
