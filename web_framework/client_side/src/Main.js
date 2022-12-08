import React from "react";

import Container from "react-bootstrap/Container";
import MultiComponentRender from "./multiComponentRender/MultiComponentRender";
import MainTemplatePage from "./Template/DefaultTemplate";

import {userContext} from './stores/userContext';
import FrontPage from "./Template/FrontPage";
import TvPage from "./Template/TvPage";

/**
 *
 */


class Main extends React.Component {
    //sets state.data to props, if props is null sets an empty list
    constructor(props) {
        super(props);
        // set data to initialData or []
        this.state = {};
    }

    //if there is an error print it
    defaultOnError = (error) => {
        console.error(error)
    }

    render() {
        let pageName = this.props.params.id;
        let params = this.props.params.params;
        if (pageName.includes('TV')){
            return (
                <userContext.Consumer>
                    {user =>
                        <TvPage login={user.user} pageName={pageName}/>
                    }
                </userContext.Consumer>);
        }

        return <userContext.Consumer>
            {user =>
                <>
                    <style type="text/css">{`::-webkit-scrollbar {display: none;}`}</style>
                    <MainTemplatePage user={user.user}/>
                    <Container className="p-3" >
                        {pageName.includes('front') ?
                            <FrontPage user={user.user}/> :
                                <MultiComponentRender login={user.user} pageName={pageName} params={params}/>}
                    </Container>
                </>
            }
        </userContext.Consumer>;
    }
}

export default Main;

