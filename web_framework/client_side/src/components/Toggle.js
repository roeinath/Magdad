import React from "react";
// import BootstrapSwitchButton from 'bootstrap-switch-button-react'
import {COLORS, SIZES} from "../constants";

const Toggle = ({onChange, initial_state, on_label, off_label, size}) => {
    const toggleStyle = {
        backgroundColor: COLORS.TALPIOT_CYAN,
        padding: '0.35rem',
        fontSize: SIZES[size] || size
    };

    // return <BootstrapSwitchButton
    //     checked={initial_state}
    //     onlabel={on_label}
    //     offlabel={off_label}
    //     onChange={(checked) => {
    //         onChange({checked: checked});
    //     }}
    //     onstyle="outline-primary"
    //     offstyle="outline-dark"
    // />
}

export default Toggle;
