import React from 'react';
import ComponentSelector from "./ComponentSelector";
import {OverlayTrigger, Table, Tooltip} from "react-bootstrap";
import {COLORS} from "../constants";

const GridView = ({width, height, padding, cols, rows, rowsGap, colsGap, children, maxWidth, maxHeight}) => {
    let style = {
        display: 'grid',
        width: width,
        height: height,
        padding: padding,
        gridTemplateColumns: `repeat(${cols}, 1fr)`,
        gridTemplateRows: `repeat(${rows}, 1fr)`,
        gridColumnGap: colsGap,
        gridRowGap: rowsGap,
        maxWidth: maxWidth,
        maxHeight: maxHeight
    }

    return <div style={style}>
        {children && children.map(child => {
                if (!child || !child.component)
                    return;
                const {component: componentData} = child;
                return ComponentSelector(componentData);
            }
        )}
    </div>
}

export default GridView;

