import React from 'react';
import ComponentSelector from "./ComponentSelector";

const Card = ({width, height, padding, shadow, background_color, radius, children, grid_start, grid_end, title}) => {
    const cardStyle = {
        width: width,
        height: height,
        padding: padding,
        boxShadow: shadow,
        backgroundColor: background_color,
        borderRadius: radius,
        display: 'flex',
        flexDirection: 'column',
        gridColumnStart: grid_start && grid_start.length === 2 ? grid_start[0] : null,
        gridRowStart: grid_start && grid_start.length === 2 ? grid_start[1] : null,
        gridColumnEnd: grid_end && grid_end.length === 2 ? grid_end[0] : null,
        gridRowEnd: grid_end && grid_end.length === 2 ? grid_end[1] : null,
        boxSizing: 'content-box',
        minWidth: '0px'
    }

    return <div style={cardStyle}>
        {children && children.map(child => {
                if (!child || !child.component)
                    return;
                const {component: componentData} = child;
                return ComponentSelector(componentData);
            }
        )}
    </div>
}

export default Card;

