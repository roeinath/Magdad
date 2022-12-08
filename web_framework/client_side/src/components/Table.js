import React, {useEffect, useState} from 'react';

import {Container, Col, Table as T, FormControl} from "react-bootstrap";
import HebrewLabel from "./HebrewLabel";
import ComponentSelector from "./ComponentSelector";
import FormInput from "./FormInput";
import SubmitButton from "./SubmitButton";

const TableCell = (cell) => <td style={{'font-size': '1vw'}}>{cell}</td>;

const Table = ({props, children, onSubmit}) => {
    const {objects, headers, action} = props;
    const [data, setData] = useState({...objects});
    const [filteredObjects, setFilteredObjects] = useState(objects);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        if (searchTerm) {
            const reqData = objects.filter(({name}, index) => {
                const lowerCaseName = name && name.toLowerCase();
                if (lowerCaseName.includes(searchTerm.toLowerCase()))
                    return objects[index];
                return null;
            });
            setFilteredObjects(reqData.filter(user => !!user));
        } else setFilteredObjects(objects);
    }, [searchTerm, setFilteredObjects]
    );

    const fieldIndex = (field) => { return headers.findIndex(h => h.name === field) };
    // function that return the index in the headers list of a field

    const tableHeaders = headers.map(h => TableCell(h.display_name));
    // the labels of the headers

    const onChange = (name, value, index) => {
        data[index] = {...data[index], [name]: value}
        setData(data);
    };
    // what to do if a value changes

    const submitTable = () => {
        onSubmit(action, {data: {objects: data}});
    };
    // send table data to the server

    const tableRow = (fields, rowIndex) => {
        // foreach field, extract the cell
        return fields.map((field, fieldIndex) => {
            let cell = field;
            if (field === null)
                cell = '';
            else if (typeof field === 'object')
                cell = ComponentSelector(field);
            // returns a form input
            return TableCell(FormInput({
                ...headers[fieldIndex], initial_value: cell, isForm: false,
                onChange: (name, value) => { onChange(name, value, rowIndex); }
            }) || '---')
        })
    };

    // for each object call tableRow
    const tableBody = filteredObjects.map((row, rowIndex) => {
        // turns object to a list of its values sorted like the headers
        const fieldsIndexes = Object.entries(row).reduce((obj, [field, value]) => {
            return {...obj, [fieldIndex(field)]: value};
        }, {});

        const sortedFields = headers.map((_, index) => fieldsIndexes[index]);
        console.log(sortedFields);
        return <tr>{tableRow(sortedFields, rowIndex)}</tr>
    })

    return <Container styled={{
                // 'max-width': '100rem',
                'overflow': 'hidden',
                    'white-space': 'nowrap',
                    'position': 'absolute',
                    'width': '100%',
            }}>
        <Col>
            <HebrewLabel>{children}</HebrewLabel>
            <FormControl style={{'margin': '1rem', 'max-width': '50%', 'float': 'right'}}
                         onChange={(event) => {
                            setSearchTerm(event.target.value)
                        }}
                         type="text" placeholder="חפש..."  dir="rtl"
            />
        </Col>
        {objects &&
            <T bordered hover dir="rtl" style={{'table-layout': 'fixed', 'font-size': 'inherit'}}>
                <thead><tr>{tableHeaders}</tr></thead>
                <tbody>{tableBody}</tbody>
            </T>
        }
        {(!tableBody || tableBody.length === 0) && <HebrewLabel>ממש ריק פה! איפה כולם?</HebrewLabel>}
        {onSubmit && <SubmitButton onSubmit={submitTable} />}
    </Container>;


};

export default Table;