import React, {useState} from 'react';

import {withTheme} from '@rjsf/core';
import {Theme as AntDTheme} from '@rjsf/antd';
import 'antd/dist/antd.css';

import SelectWidget from './form/SelectWidget';
import Button from "react-bootstrap/Button";

// Make modifications to the theme with your own fields and widgets

const Form = withTheme(AntDTheme);


const JsonSchemaForm = ({json_schema, ui_schema, onSubmit, children = "שליחה"}) => {
    const [data, setData] = useState({});

    const onChange = (data) => {
        setData(data);
    }; // updates the data when change happens

    const submitForm = () => {
        onSubmit({data: {properties: data}});
    }; // submits data

    const customWidgets = {SelectWidget: SelectWidget};

    return <div>
        <Form
            style={{width: '100%'}}
            schema={json_schema}
            uiSchema={ui_schema}
            widgets={customWidgets}
            value={data}
            onChange={(x) => console.log("changed", x)}
            onSubmit={(x) => onSubmit({data: {properties: x.formData}})}
            onError={(x) => console.log("errors", x)}
        >
            <Button type="submit" variant="info">{children}</Button>
        </Form>
        <style type="text/css">
            {`
                .ant-form-item-label {
                    text-align: right !important;
                }
                .ant-select-selector {
                    text-align: right !important;
                }
                .ant-select-item-option-content {
                    text-align: right !important;
                }
                .ant-picker-header {
                    direction: ltr !important;
                }
            `}
        </style>
    </div>;
};

export default JsonSchemaForm;