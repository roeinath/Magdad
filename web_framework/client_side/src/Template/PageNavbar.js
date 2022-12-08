import React, {useState} from 'react';

import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import NavDropdown from 'react-bootstrap/NavDropdown'
import {Link} from 'react-router-dom';

import LoginComponent from "../components/LoginComponent";
import {COLORS} from "../constants";
import TalpixLogo from "./TalpixLogo";
import {isMobileOnly as isMobile} from "react-device-detect";


class DropDownPageSelector extends React.Component {
    constructor(props) {
        super(props);
        this.state = {click: false, hover: false};
    }

    componentDidMount() {
        // when the page first reloads, call the refreshPage function
        this.refresh()
    }

    defaultOnError = (error) => {
        console.error(error)
    }

    async refresh() {
        const {fetchFunction, onError = this.defaultOnError} = this.props;
        if (!fetchFunction)
            return;

        // fetch the request and then set the data to the request data
        fetchFunction().then(
            (result) => {
                this.setState({data: result.data});
            },
            onError // do something if an error happens
        )
    }

    render() {
        const {pages, title, closeNavBar} = this.props; // get the data from the state
        const {click, hover} = this.state; // get the data from the state

        return <NavDropdown title={`${title}  `} id="collasible-nav-dropdown"
                            onMouseEnter={() => {this.setState({hover: true})}}
                            onMouseLeave={() => {this.setState({hover: false})}}
                            onClick={() => {this.setState({click: !click})}}
                            style={{fontSize: '20px'}}
        >
            <style type="text/css">
                {`
                .dropdown-menu.show {
                    background-color: ${COLORS.TALPIOT_DARK_BLUE};
                    color: white;
                    top: 115%;
                }
                .dropdown-menu {
                    transition: all 0.3s ease-in-out 0s, visibility 0s linear 0.3s, z-index 0s linear 0.01s;
                }
                .dropdown-item:hover {
                    background: ${COLORS.TALPIOT_BLUE} !important;
                }
            `}
            </style>
            {pages && pages.length > 0 // if the data is not an empty list
                ? pages.map((item) => { // foreach item in the data
                    const page_address = item.url;
                    const link_title = item.name;

                    // return the item's component
                    return <NavDropdown.Item
                        as={Link}
                        to={page_address}
                        onClick={closeNavBar}
                        style={{textAlign: 'right', color: COLORS.WHITE, background: COLORS.TRANSPARENT}}
                    >
                        {link_title}
                    </NavDropdown.Item>
                }) : "No pages"}
        </NavDropdown>;
    }
}

const Categories = ({categories}) => {
    // categories = categories.categories;
    // const current_page = props.current_page
    const numberOfCategories = categories?.length || 0;

    console.log("Given categories", categories);

    return <Navbar>
        <Navbar.Collapse id="navbarScroll">
            {numberOfCategories > 0 && categories.map(category =>
                <Navbar variant="dark" id="responsive-navbar-nav">
                    <Nav className="mr-auto">
                        <DropDownPageSelector title={category.name} pages={category.pages}/>

                    </Nav>
                </Navbar>)
            }

        </Navbar.Collapse>

        <Navbar.Toggle aria-controls="navbarScroll"/>
    </Navbar>
}


const PageNavbar = ({categories}) => {
        const [isOpen, setOpen] = useState(false);
        categories = categories.categories;
        // const current_page = props.current_page
        const numberOfCategories = categories?.length || 0;
        const side = "top"

        const login = <Nav className="ml-auto" style={{justifyItems: 'end', right: '5px'}}><LoginComponent/></Nav>

        return <Navbar
            expand="lg" variant="dark" fixed={side} className="menu" expanded={isOpen} dir="rtl"
            style={{
                width: '100%',
                justifyItems: 'end',
                backgroundColor: COLORS.TALPIOT_BLUE,
                transform: 'translateZ(100%)'
            }}
        >
            <Navbar.Brand as={Link} to="/react/page/front">
                TalpiWeb
                <TalpixLogo size_type="symbol"/>
            </Navbar.Brand>
            {isMobile && login}
            <Navbar.Collapse style={{marginLeft: '5%', textAlign: 'right'}}>
                {
                    numberOfCategories > 0 && categories.map(category =>
                        <Nav className="mr-auto">
                            <DropDownPageSelector
                                title={category.name}
                                pages={category.pages}
                                closeNavBar={() => setOpen(false)}
                            />
                        </Nav>
                    )
                }
            </Navbar.Collapse>
            {!isMobile && login}
            <Navbar.Toggle onClick={() => {
                setOpen(!isOpen)
            }} style={{position: 'fixed', left: '1rem', top: '0.7rem'}}/>

        </Navbar>
    }
;

export default PageNavbar
