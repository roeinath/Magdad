import React, {useState} from "react";
import {Accordion as BootstrapAccordion, Card, Row, Col} from "react-bootstrap";
import ComponentSelector from "./ComponentSelector";
import HebrewLabel from "./HebrewLabel";
import Image from "./Image";
import {SIZES} from "../constants";

const DOWN = 1
const UP = -1

const Accordion = ({children, background_color = 'transparent', ...props}) => {
    const cardStyle = {
        border: 'none',
        borderBottom: '1px solid rgba(0, 0, 0, 0.125)',
        alignItems: 'center',
    }
    const headerStyle = {
        padding: '0',
        border: 'none',
        backgroundColor: background_color,
        overflow: 'hidden',
        width: '60vw'
    }

    const arrowsDict = {
        [DOWN]: <Image
            url="https://www.svgrepo.com/show/9249/down-chevron.svg"
            scale={0.03}
        />,
        [UP]: <Image
            url="https://www.svgrepo.com/show/93813/up-arrow.svg"
            scale={0.03}
        />
    }

    const [arrowStates, changeArrowStates] = useState(Array(children.length).fill(DOWN));

    const changeArrow = (index) => {
        const newStates = Array(children.length).fill(DOWN);
        newStates[index] = -1 * arrowStates[index];
        changeArrowStates(newStates);
    }

    return <BootstrapAccordion>
        {
            children && children.map((child, index) =>
                <Card style={cardStyle}>
                    <BootstrapAccordion.Toggle
                        as={Card.Header}
                        eventKey={index + 1}
                        style={headerStyle}
                        onClick={() => {
                            changeArrow(index);
                        }}
                    >
                        <Row>
                            <Col>{arrowsDict[arrowStates[index]]}</Col>
                            <Col><HebrewLabel bold={true} {...props}>{child.title || ""}</HebrewLabel></Col>
                            <Col>{arrowsDict[arrowStates[index]]}</Col>
                        </Row>
                    </BootstrapAccordion.Toggle>
                    <BootstrapAccordion.Collapse eventKey={index + 1}>
                        <Card.Body>
                            {child && child.component && ComponentSelector(child.component)}
                        </Card.Body>
                    </BootstrapAccordion.Collapse>
                </Card>
            )
        }
        <style type="text/css">
            {`
                .card-header:hover {
                    background-color: rgba(200, 200, 200, 0.3) !important;
                    cursor: pointer !important;
                }
            `}
        </style>
    </BootstrapAccordion>
}

export default Accordion;
