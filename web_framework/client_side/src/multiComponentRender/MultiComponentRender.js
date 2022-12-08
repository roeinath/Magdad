import React from 'react';
import axios from 'axios';
import {withRouter} from 'react-router-dom'

import {fetchApi, fetchPage} from "../stores/apiStore";
import {Container, Modal} from "react-bootstrap";
import {container, item} from "./MultiComponentRender.css";
import {pageContext} from "../stores/pageContext";
import Loader from "../components/LoadingAlert";
import ComponentSelector from "../components/ComponentSelector";
import HebrewLabel from "../components/HebrewLabel";
import {ACTIONS, COLORS, FONTS, HTTP_RESPONSE} from "../constants";

/**
 * Singleton that handles drawing TalpiX components.
 */


class MultiComponentRender extends React.Component {
    //sets state.data to props, if props is null sets an empty list
    //PARAM props = (login, pagename)
    constructor(props) {
        super(props);
        // set data to initialData or []
        const {initialData} = props;
        this.state = {
            data: initialData || [],
            parentsDict: {}, //For every component, his parent
            user: props.login,
            serverResponse: {responseStatus: 0, responseMessage: ''},
            isLoading: false
        };
        this.cancelTokenSource = axios.CancelToken.source();

        this.doAction = this.doAction.bind(this);
    }

    componentDidMount() {
        // when the page first reloads, call the refreshPage function
        this.cancelTokenSource = axios.CancelToken.source();
        this.refreshPage()
    }

    componentDidUpdate(prevProps) {
        //Called when any component changes
        if (JSON.stringify(prevProps) !== JSON.stringify(this.props)) {
            if (this.props.login.access !== prevProps.login.access)
                return
            //If the props are changed
            this.setState({
                data: []
            });
            this.cancelTokenSource.cancel();
            this.cancelTokenSource = axios.CancelToken.source();
            console.log("props", prevProps, this.props);
            this.refreshPage();
        }
    }

    //if there is an error print it
    defaultOnError = (error) => {
        const {serverResponse} = this.state;
        serverResponse.responseStatus = error.response && error.response.status
        if (error.response && error.response.data) {
            const errorData = error.response.data;
            serverResponse.responseMessage = typeof errorData === 'object' ? errorData.error : errorData
        } else if (error.isAxiosError) {
            serverResponse.responseStatus = HTTP_RESPONSE.CONNECTION_ERROR
        }
        this.setState({serverResponse, isLoading: false});
        console.error("Got an error", error)
        console.log(Object.entries(error), error.response)
    }

    //Find the data of the child component with the given id, inside the given data
    //Gets data parameter, so this function can find children of a child and not just the whole page.
    findIndex(data, id) {
        return data.findIndex(i => i.id === id); // find index where value's id === id
    }

    /**
     * Perform an action on a given component
     * @param {*} data the data of the component's parent
     * @param {*} index the id of the component to edit
     * @param {*} action the action to perform (change, add_child, etc')
     * @param {*} value the value for the action (for example, the child to add)
     */
    findAndEditByIndex(data, index, action, value) {
        if (index >= 0 && index < data.length && value) { // check that the value is not undefined and data has that index
            if (action === ACTIONS.add_component && value.child) {
                const prevChildren = data[index].children || []; // change the value for the specific index
                data[index].children = [...prevChildren, value.child];
            } else if (action === ACTIONS.REMOVE_CHILD && value.component) {
                const prevChildren = data[index].children || []; // change the value for the specific index
                const childIndex = prevChildren.findIndex(child => child.id === value.component.id)
                prevChildren.splice(childIndex, 1);
                data[index] = {...data[index], children: prevChildren};
            } else if (action === ACTIONS.CHANGE) {
                Object.entries(value).forEach(([name, attr]) => {
                    data[index][name] = attr;
                }); // change the value for the specific index
            } else { //any other action is passed to the component to decide what to do

            }
        }
    }

    findParentOf(data, id) {
        const {parentsDict} = this.state;
        const parentIdList = [id, ...parentsDict[id]]; // get the id of the parent
        let currentParentData = data;
        for (let i = parentIdList.length - 1; i > 0; i--) {

            // console.log("parentData", currentParentData)
            let parentId = parentIdList[i]

            const index = this.findIndex(currentParentData, parentId);
            if (index >= 0) {
                if (!currentParentData[index].children) {
                    currentParentData[index].children = []
                }
                currentParentData = currentParentData[index].children && currentParentData[index].children
                    .map(child => child.component);
            } else {
                console.log("Child not Found", parentId, data)
            }
        }
        return currentParentData;
    }

    /**
     *
     * @param {*} data
     * @param {*} value
     * @param {*} id
     * @param {*} action
     */
    doActionOnComponent(data, id, action, value) {
        const currentParentData = this.findParentOf(data, id);

        const index = this.findIndex(currentParentData, id);
        this.findAndEditByIndex(currentParentData, index, action, value);
        // console.log("data", data)
    }

    async refreshPage() {
        //get fetch function from props
        console.log(this.props)
        let pageName = this.props.pageName;
        let params = this.props.params;
        const user = this.props.login;

        console.log("refresh page " + pageName)

        if (!pageName) //if null
            return;

        await this.updateData(fetchPage(pageName, user, params, this.cancelTokenSource), true)
    }

    async doAction(actionUrl, actionData) {
        console.log("Doing action!", actionUrl, actionData)
        // when action happens, sent the action data to the server with post request
        if (!actionUrl)
            return

        const user = this.props.login;

        //fetch the json from the server and store it in result
        const fetchFunction = fetchApi(actionUrl, user, actionData, this.cancelTokenSource);
        await this.updateData(fetchFunction, false);
    }

    async updateData(fetchFunction, enforceNewData) {
        // when action happens, sent the action data to the server with post request
        if (!fetchFunction)
            return

        const {onError = this.defaultOnError} = this.props;
        const {parentsDict, isLoading} = this.state; //the data we fetched with {refreshPage}
        var {data} = this.state;

        if (enforceNewData) {
            data = [];
        }

        this.setState({isLoading: enforceNewData ? isLoading : null});
        setTimeout(() => {
            if (this.state.isLoading === null) {
                this.setState({isLoading: true});
            }
        }, 1500)

        //fetch the jason from the server and store it in result
        fetchFunction.then(
            (result) => {
                const {serverResponse} = this.state;
                serverResponse.responseStatus = result.status; // update status from server
                this.setState({serverResponse})

                result = result.data;
                if (result.detail != null)
                    return;

                //run on each pair {action, value} in result's items and processes it
                Object.values(result).forEach((pack) => { // run on all items sent
                    pack.forEach(({action, value}) => {   //for each item ({action, value}) in the package
                        if (!value || !value.id)
                            return;

                        //Redirect to url
                        if (action === ACTIONS.REDIRECT) {
                            if (value.override) {
                                this.props.history.push(value.url);
                            }
                            else if (!this.props.history.location.pathname.endsWith(value.url)) {
                                const url = `${this.props.history.location.pathname}${value.url}`
                                this.props.history.push(url.replace('//', '/'));
                            }
                        }

                        //Add a component to root
                        if (action === ACTIONS.ADD) {
                            data.push({...value});
                            parentsDict[value.id] = [] // declare that this component does not have a parent
                        }

                        //All the other actions
                        if ([ACTIONS.CHANGE, ACTIONS.add_component, ACTIONS.REMOVE_CHILD].includes(action)) {
                            if (value && value.child && value.child.component) {
                                //If the value is a children of something, update its parent in the parent dict
                                const grandParents = parentsDict[value.id]
                                if (!grandParents) {
                                    console.error(`Trying to add a ${value.child.component.type} to not existing component with id ${value.id}`);
                                    return;
                                }
                                parentsDict[value.child.component.id] = [value.id, ...grandParents] // save the parent id of the child
                            }
                            //Update the component
                            this.doActionOnComponent(data, value.id, action, value);
                        }
                    })
                })
                // sets the data in the state to our changed data
                this.setState({data, parentsDict, isLoading: false});
            },
            onError // do something if an error happens
        )
    }

    render() {
        const {data, serverResponse: {responseStatus, responseMessage}, isLoading} = this.state; // get the data from the state

        const value = {
            onEvent: this.doAction
        };

        const BAD_REQUEST_MESSAGE = `נסו לטעון מחדש את העמוד או להתחבר לחשבון של תלפיות`;
        const SERVER_ERROR_MESSAGE = 'השרת נתקל בשגיאה';
        const CONNECTION_ERROR_MESSAGE = `בעיית חיבור לשרת` + ' ' + (responseMessage || '');

        return (
            <pageContext.Provider value={value}>
                <Container className={container}>
                    {data && data.length > 0 // if the data is not an empty list
                        ? data.map((item) => { // foreach item in the data
                            const itemChild = ComponentSelector({
                                ...item, // all the data on the item
                            });
                            // return the item's component
                            return <div className="item">
                                <span className="sr-only">{item.id}</span>
                                {itemChild}
                            </div>
                        }) :  // if data is empty
                        <div className={item}>
                            {HTTP_RESPONSE.equal(responseStatus, HTTP_RESPONSE.BAD_REQUEST) ?
                                <HebrewLabel font={FONTS.RUBIK} color={COLORS.ALERT} size="2rem">
                                    {responseMessage || BAD_REQUEST_MESSAGE}
                                </HebrewLabel>
                                : HTTP_RESPONSE.equal(responseStatus, HTTP_RESPONSE.SERVER_ERROR) ?
                                    <HebrewLabel font={FONTS.RUBIK} color={COLORS.ALERT} size="2rem">
                                        {SERVER_ERROR_MESSAGE}
                                    </HebrewLabel>
                                    : HTTP_RESPONSE.equal(responseStatus, HTTP_RESPONSE.CONNECTION_ERROR) ?
                                        <HebrewLabel font={FONTS.RUBIK} color={COLORS.ALERT} size="2rem">
                                            {CONNECTION_ERROR_MESSAGE}
                                        </HebrewLabel>
                                        : Loader}
                        </div> // if the data is empty display a loader

                    }
                    <Modal size="xs" show={isLoading} centered onHide={() => {
                        this.setState({isLoading: false});
                    }}>
                        <Container style={{padding: 0}}>
                            {Loader}
                        </Container>
                    </Modal>
                </Container>
            </pageContext.Provider>
        );
    }
}

export default withRouter(MultiComponentRender);