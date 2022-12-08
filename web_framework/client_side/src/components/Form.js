import React, {useState} from 'react';

import {Row, Col, Form as F, Container} from "react-bootstrap";
import HebrewLabel from "./HebrewLabel";
import SubmitButton from "./SubmitButton";
import FormInput from "./FormInput";

// turn properties to an object: key = property name, value = initial value
const initialValues = (properties) => {
    if (!properties)
        return {};
    return properties.reduce((obj, property) => {
        return property.initial_value ? {
            ...obj,
            [property.name]: property.is_placeholder ? null : property.initial_value
        } : obj;
    }, {})
};


const Form = ({props, children, onSubmit}) => {
    const { properties } = props;
    const [data, setData] = useState(initialValues(properties));

    const onChange = (name, value) => {
        data[name] = value;
        setData(data);
    }; // updates the data when change happens

    const submitForm = () => {
        onSubmit({data: {properties: data}});
    }; // submits data

    const groups = properties && properties.map((props) => {
        // groups of form input with its label
        const formControl = FormInput({...props, onChange})

        if (!formControl)
            return;

        return <F.Group as={Row} controlId={props.name}>
            <Col md="3"><F.Label>{props.display_name}</F.Label></Col>
            <Col>{formControl}</Col>
            {props.text && <F.Text className="text-muted">{props.text}</F.Text>}
        </F.Group>
    });

    //the Form return html
    return <Container>
        <HebrewLabel>{children}</HebrewLabel>
        {properties &&
            // right to left form
            <F dir="rtl">
                {groups}
                <SubmitButton onSubmit={submitForm} />
            </F>
        }
    </Container>;
};

export default Form;