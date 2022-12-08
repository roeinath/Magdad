import MultiComponentRender from "../multiComponentRender/MultiComponentRender";
import React from "react";
import {COLORS} from "../constants";
import Navbar from "react-bootstrap/Navbar";
import {Link} from "react-router-dom";
import TalpixLogo from "./TalpixLogo";
import Nav from "react-bootstrap/Nav";
import Clock from 'react-live-clock';
import 'moment-timezone';
import 'react-moment'

const TvPage =  ({login, pageName}) => {
    console.log("Here")
    return <>
            <Navbar expand="lg" variant="dark" fixed={"top"} className="menu"
                    style={{
                        width: '100%',
                        justifyItems: 'end',
                        backgroundColor: COLORS.TALPIOT_BLUE,
                        transform: 'translateZ(100%)',
                        }}>
                <Navbar.Brand as={Link} to="/react/page/front">
                    TalpiWeb
                    {/*{isMobile ? null : 'TalpiWeb'}*/}
                    <TalpixLogo size_type = "symbol"/>
                    {/*{<img src={logo} alt="Talpiot" style={{width: picSize, height: picSize, paddingLeft: '6px'}}/>}*/}
                </Navbar.Brand>
                <Nav className="ml-auto" style={{justifyItems: 'end', right: '10px'} }>
                    <Clock format={'HH:mm:ss DD/MM/YYYY'}
                           ticking={true}
                           timezone={'Asia/Jerusalem'}
                           style={{fontSize: '1.5em', color: 'white'}}
                           locale='he-IL'
                    />
                </Nav>
            </Navbar>
            <MultiComponentRender login={login} pageName={pageName}/>
        </>
}

export default TvPage;