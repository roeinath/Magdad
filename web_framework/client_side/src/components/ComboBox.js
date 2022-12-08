import React, {useState} from 'react';

import {Container, InputGroup} from "react-bootstrap";
import { Typeahead } from 'react-bootstrap-typeahead'
import {COLORS} from "../constants";
import NavDropdown from "react-bootstrap/NavDropdown";

const ComboBox = ({placeHolder, options, multiple, onChoose, default_value}) => {
    const initialState = options[default_value] ? [{id: default_value, label: options[default_value]}] : []
    const [selection, setSelection] = useState(initialState);
    const firstOption = options && Object.values(options) && Object.values(options)[0]
    const isHebrew = typeof firstOption !== "string" || !firstOption.charAt(0).match(/[a-z]/i)
    const optionsList = Object.keys(options).map(id => ({id, label: options[id]})) // map dictionary to a list of id and label

    const filterBy = (option, search) => {
        if (search.selected.length) {
            return true;
        }
        return option.label.toLowerCase().indexOf(search.text.toLowerCase()) > -1;
    }

    const onChange = (selected) => {
        setSelection(selected);
        onChoose({chosen: selected && selected[0] && selected[0].id }); // return chosen id
    }

    return <Container>
        <InputGroup
            style={{float: 'right', left: isHebrew ? 0 : '10%', textAlign: 'right', marginBottom: '4px',
                color: COLORS.WHITE}}
            dir={isHebrew ? "rtl" : "ltr"}
        >
            <Typeahead
                id="combo-box"
                filterBy={filterBy}
                options={optionsList}
                placeholder={placeHolder}
                emptyLabel="🙁 לא נמצאה התאמה"
                style={{width: '90%', height: '50%'}}
                multiple={multiple}
                onChange={onChange}
                selected={selection}
                size="sm"
            >
                <style type="text/css">
                    {`
                    .dropdown-item, .dropdown-menu {
                        background-color: ${COLORS.TALPIOT_DARK_BLUE};
                        color: white;
                        text-align: right;
                    }
                    .dropdown-item:hover {
                        background: ${COLORS.TALPIOT_BLUE} !important;
                        color: ${COLORS.WHITE} !important;
                    }
                `}
                </style>
            </Typeahead>
        </InputGroup>
    </Container>
};

export default ComboBox;