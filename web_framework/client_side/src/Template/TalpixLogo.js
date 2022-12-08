import logo from "./talpiot-logo.png"
import React from "react";

// const logo = process.env.PUBLIC_URL + "/talpiX-logo-new.png";

const TalpixLogo = ({size_type})=>{

    const picSize = size_type === "page"?window.innerWidth *0.25:(size_type === "symbol"?'50px':'10vw')
    const styleImage = {
        width: picSize, alignSelf: 'center', padding: '5px'} //, top: window.innerHeight*0.1
    return <img src={logo} alt="Talpiot" style={styleImage}/>

}
export default TalpixLogo;