import React, {useState} from 'react';
import HebrewLabel from "./HebrewLabel";


const CountDown = ({time: countDownTime}) => {
    const [countString, setCount] = useState('');
    const updateCount = () => {
        setTimeout(() => {
            const distance = new Date(countDownTime).getTime() - new Date().getTime();
            const days = Math.floor(distance / (1000 * 60 * 60 * 24)).toString();
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString().padStart(2, '0');
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, '0');
            const seconds = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, '0');
            setCount(`${days} ימים ו-${hours}:${minutes}:${seconds}`);
            updateCount();
        }, 1000);
    }

    updateCount();
    return <HebrewLabel size={30}>{countString}</HebrewLabel>
};

export default CountDown;
