import * as Scroll from 'react-scroll'
import {Link, Element, Events, animateScroll as scroll, scrollSpy, scroller} from 'react-scroll'
import React from "react";
import './Scroller.css';
import ComponentSelector from "./ComponentSelector";
import HebrewLabel from "./HebrewLabel";
import Image from "./Image";

const Scroller = ({children, time}) => {
    console.log("children",children);
    return <div id='header' style={{overflowY: "hidden", height: 'auto', marginTop: "2rem"}}>
        <div className='toScroll' style={{animationDuration: `${time}s`}}>
            {children && children.map(child => {
                if (!child || !child.component)
                    return;
                const component = ComponentSelector(child.component);
                return <div>{component}</div>
            }
            )}
        </div>
    </div>;
};

export default Scroller;
