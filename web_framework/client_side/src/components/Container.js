import React from 'react';
import ComponentSelector from "./ComponentSelector";
import {COLORS} from "../constants";

const Container = ({width, height, padding, margin, orientation, alignItems, justifyContent, children}) => {
    const containerStyle = {
        width: width,
        height: height,
        padding: padding,
        margin: margin,
        display: 'flex',
        flexDirection: orientation,
        alignItems: alignItems,
        justifyContent: justifyContent
    }

    return <div className={'Container'} style={containerStyle}>
        {children && children.map(child => {
                    if (!child || !child.component)
                        return;
                    console.log(margin)
                    const {component: componentData} = child;
                    return ComponentSelector(componentData);
                }
            )
        }
    </div>
}

export default Container;

