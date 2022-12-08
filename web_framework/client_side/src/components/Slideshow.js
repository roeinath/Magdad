import React from 'react'
import Carousel from 'react-bootstrap/Carousel'
import HebrewLabel from "./HebrewLabel";
import {Container} from "react-bootstrap";
import ComponentSelector from "./ComponentSelector";

const Slideshow = ({interval, children}) => {
    const style = {flex: true, justifyContent: 'center', width: '50vw'}
    const size = Array.isArray(children) ? children.length: 1;
    const car_items = size > 1 && children.map((child) => {
        if (!child || !child.component)
            return;
        const component = ComponentSelector(child.component);
        return <Carousel.Item> {component} </Carousel.Item>
    });

    if (size > 1) {
        return (
            <Container style={style}>
                <Carousel interval={interval}>
                    {car_items}
                </Carousel>
            </Container>);
    }
    else if (size === 1)
        return <Container style={style}> {children} </Container>
    else
        return <Container style={style}> <HebrewLabel>Slideshow: אין מספיק שקופיות להציג 😖</HebrewLabel> </Container>
}

export default Slideshow;
