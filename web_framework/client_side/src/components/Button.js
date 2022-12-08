import React, {useRef, useState} from "react";
import {Button as BootstrapButton, Spinner} from "react-bootstrap";
import {COLORS, FONTS, SIZES} from "../constants";

const Button = ({onClick, text, size, font, background_color = COLORS.TALPIOT_CYAN, color = COLORS.WHITE}) => {
    const [isLoading, setLoading] = useState(false);
    const [width, setWidth] = useState(-1);
    const ref = useRef(null);
    const onSubmit = async () => {
        setLoading(true);
        onClick();
        setTimeout(() => setLoading(false), 1000);
        setWidth(Math.max(ref.current.offsetWidth, width));
    };

    const btnStyle = {
        fontSize: SIZES[size] || size,
        fontFamily: font || FONTS.RUBIK, //`${font}, serif`,
        color: color || COLORS.WHITE,
        backgroundColor: background_color || COLORS.TALPIOT_CYAN,
        padding: '0.35rem 0.8rem',
        width: width,
        minWidth: 'fit-content',
        height: 'fit-content',
        alignItems: 'center',
        alignText: 'center',
    }
//    const btnStyle = {backgroundColor: background_color?background_color:COLORS.TALPIOT_CYAN,
    return <BootstrapButton ref={ref} onClick={onSubmit} block variant="outline-light" style={btnStyle}>
        {isLoading ? <Spinner animation="border" size="sm"/> : text}
    </BootstrapButton>
}

export default Button;
