import React from 'react';
import {COLORS, FONTS, SIZES} from "../constants";

const HebrewLabel = ({children, font = FONTS.RUBIK, size = 'md', bold = false, italic = false,
                         background_color = COLORS.NONE, color = COLORS.BLACK, width = '100%'}) => {
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
        whiteSpace: 'pre-line'
    }


    return <label style={styledLabel} dir="rtl">
        <link rel="stylesheet" href={`https://fonts.googleapis.com/css2?family=${encodeURIComponent(font)}`} />
        {children}
    </label>;
};

export default HebrewLabel;
