import React, {useState} from 'react';
import HebrewLabel from "./HebrewLabel";
import {Container, Row, Col} from "react-bootstrap"

const HEBREW_TIMES = {
    seconds: 'שניות',
    minutes: 'דקות',
    hours: 'שעות',
    days: 'ימים',
}

const CountDown = ({time: countDownTime}) => {
    const [countSeconds, setCountSeconds] = useState(0);
    const [countMinutes, setCountMinutes] = useState(0);
    const [countHours, setCountHours] = useState(0);
    const [countDays, setCountDays] = useState(0);
    const updateCount = () => {
        setTimeout(() => {
            const distance = new Date(countDownTime).getTime() - new Date().getTime();
            const days = Math.floor(distance / (1000 * 60 * 60 * 24)).toString();
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString().padStart(2, '0');
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, '0');
            const seconds = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, '0');
            setCountSeconds(seconds);
            setCountMinutes(minutes);
            setCountHours(hours);
            setCountDays(days);
            updateCount();
        }, 1000);
    }

    updateCount();
    return <Row>
        {Object.entries({
            days: countDays,
            hours: countHours,
            minutes: countMinutes,
            seconds: countSeconds
        }).map(([key, value]) => {
            return <Col>
                <h1 style={{fontSize: '13vh', marginBottom: '0px', padding: '0 9vh'}}>{value}</h1>
                <HebrewLabel size={25}>{HEBREW_TIMES[key]}</HebrewLabel>
            </Col>
        })}
    </Row>

};

export default CountDown;
