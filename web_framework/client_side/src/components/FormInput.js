import React, {useState} from "react";
import * as moment from "moment";
import {FormControl as FC, Col, Row, Tooltip, OverlayTrigger} from "react-bootstrap";
import {COLORS, TIME_FORMATS} from "../constants";

const FormControl = ({name, type, display_name, editable = true, placeholder, value,
                         onChange, isForm = true, color, background_color}) => {
    const [isFocused, setFocus] = useState(isForm);

    const onBlur = (event) => {
        setFocus(isForm);
        onChange(name, event.target.value);
    }; // on outside click

    const notFocusedStyled = {
        'background-color': background_color || COLORS.TRANSPARENT,
        'border': 'none',
        'color': color || COLORS.BLACK,
    } // style when input is not clicked
    const formControlStyled = {

        'width': '100%',
        'padding': '10px',
        'margin': '0px',
        'box-sizing': 'border-box',
        'text-align': 'center',
        'font-size': '1vw',
        ...((!isFocused || !editable) && notFocusedStyled)
    }; // css style of the input

    return <FC
        type={type}
        readOnly={!editable || !isFocused}
        defaultValue={value}
        placeholder={placeholder}
        onFocus={() => { setFocus(true); }}
        onBlur={onBlur}
        onKeyDown={(event) => { if (event.key === 'Enter') onBlur(event);}}
        style={formControlStyled}
    />;
};


const DatetimeFormControl = ({type, display_name, initial_value, onChange, ...props }) => {
    // a datetime input. made out of 2 inputs - date and time
    const initialDate = moment(initial_value);
    const [date, setDate] = useState(initialDate.format(TIME_FORMATS.BOOTSTRAP.date));
    const [time, setTime] = useState(initialDate.format(TIME_FORMATS.BOOTSTRAP.time));

    const fullDatetime = (d, t) => moment(`${d} ${t}`).format(TIME_FORMATS.JSON)

    const onChangeDatetime = {
        time: (name, newTime) => {
            setTime(newTime);
            onChange(name, fullDatetime(date, newTime));
        },
        date: (name, newDate) => {
            setDate(newDate);
            onChange(name, fullDatetime(newDate, time));
        }
    };
    const datetimeFromControl = (fromControlType) => FormControl({
        ...props, type: fromControlType, onChange: onChangeDatetime[fromControlType],
        initial_value: initialDate.format(TIME_FORMATS.BOOTSTRAP[fromControlType])
    })

    const styledFormControl = {
        time: (!props.isForm && {'margin': '0 0 0 1.5rem'}),
        date: (!props.isForm && {'margin': '0 0 0.5rem 3rem'})
    }

    return <Row>
        {type !== 'time' && <Col style={styledFormControl.date}>{datetimeFromControl('date')}</Col>}
        {type !== 'date' && <Col style={styledFormControl.time}>{datetimeFromControl('time')}</Col>}
    </Row>
};

const FormInput = ({...props}) => {
    if (!props.visible)
        return;
    if (props.type === 'str')
        return FormControl({...props, type: 'text'});
    if (['datetime', 'date', 'time'].includes(props.type))
        return DatetimeFormControl(props);
    /*if (props.type == 'combo')
        return ComboBoxControl(props)*/

    return FormControl({...props});
};


export default FormInput;