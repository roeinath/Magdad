import React, {useState} from "react";
import {Button, Spinner} from "react-bootstrap";

const SubmitButton = ({onSubmit}) => {
    const [isLoading, setLoading] = useState(false);
    const onClick = async () => {
        setLoading(true);
        onSubmit();
        setTimeout(() => setLoading(false), 1000);
    };

    return <Button variant="primary" onClick={onClick}>
        {isLoading ? <Spinner animation="border" size="sm"/> : 'שלח'}
    </Button>
};

export default SubmitButton;
