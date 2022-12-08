import React from 'react';
import {COLORS, FONTS, SIZES} from "../constants";
import HebrewLabel from "./HebrewLabel";

const HyperLink = ({children, url = '.', ...props}) => {

    console.log(children);
    return <HebrewLabel {...props}>
        <a href={url} target='_blank'>
            {children}
        </a>
    </HebrewLabel>
};

export default HyperLink;