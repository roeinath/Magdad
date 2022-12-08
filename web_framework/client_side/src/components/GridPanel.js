import React from 'react';
import ComponentSelector from "./ComponentSelector";
import {OverlayTrigger, Table, Tooltip} from "react-bootstrap";
import {COLORS} from "../constants";


const GridPanel = ({row_count, column_count, row_headers, background_color, bordered = true, overlay, children}) => {
    const cellStyle = {padding: 0.2, border: bordered ? 'auto' : 'none', overflow: overlay ? 'hidden': 'unset'}

    const rows = []; // create a rowCount by colCount matrix
    for (let i = 0; i < row_count; i++) {
        let col = [];
        for (let j = 0; j < column_count; j++) {
            col.push(null);
        }
        rows.push(col);
    }
    // foreach child
    children && children.forEach(({row, column, background_color: childBgColor, component, row_span, column_span}) => {
        const color = childBgColor !== COLORS.TRANSPARENT ? childBgColor : background_color;
        // if row and column are in the ranges and the component is not null
        if (component && row >= 0 && row < row_count && column >= 0 && column < column_count) {
            const tableCell = (
                <td
                    style={cellStyle}
                    bgcolor={COLORS.findColor(color) || color}
                    rowSpan={row_span}
                    colSpan={column_span}
                    id={`${row}-${column}`}
                >
                    {/*turn to a component using ComponentSelector*/}
                    {ComponentSelector(component)}
                </td>
            );

            rows[row][column] = overlay ? (
                <OverlayTrigger overlay={<Tooltip>{component.text}</Tooltip>}>
                    {tableCell}
                </OverlayTrigger>
            ) : tableCell;
        }
    })

    const headers = row_headers ? rows.shift() : null;

    return <Table bordered={bordered} id="GridPanel" style={{width: '100%', tableLayout: "fixed"}}>
        <thead>
        <tr style={{borderBottom: bordered ? 'auto' : 'none'}}>{headers}</tr>
        </thead>
        <tbody>
        {rows.map(row => <tr>{row}</tr>)}
        </tbody>
    </Table>
}

export default GridPanel;

