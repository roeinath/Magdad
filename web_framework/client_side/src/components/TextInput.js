import React, {useState} from "react";
import {COLORS, FONTS, SIZES} from "../constants";
import draftToHtml from 'draftjs-to-html';
import {stateFromHTML} from "draft-js-import-html";

const TextInput = ({children, onChange, font = FONTS.RUBIK, size = 'md', bold = false, italic = false, placeholder="",
                         background_color = COLORS.NONE, color = COLORS.BLACK, width = '100%'}) => {


    const onSubmit = async (inp) => {
        var val = inp.target.value;
        if(val == ""){
            val = " ";
        }
        onChange({data: val});
    };

    const styledLabel = {
        fontSize: SIZES[size] || size,
        fontFamily: `${font}, serif`,
        fontWeight: bold ? 'bold': 'normal',
        fontStyle: italic ? 'italic': 'normal',
        color: color,
        background: background_color,
        margin: 0,
        padding: 0,
        width: width,
        whiteSpace: 'pre-line',
    }

    return <input type="text" placeholder={placeholder} onMouseOut={onSubmit} style={styledLabel} dir="rtl"/>;
};
export default TextInput;
