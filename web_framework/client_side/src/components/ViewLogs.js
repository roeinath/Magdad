import React, {useEffect, useState} from 'react';
// import {LazyLog, ScrollFollow} from 'react-lazylog';
import AceEditor from "react-ace";
import {Container, Button} from "react-bootstrap";

export default ({children, onUpdate}) => {
    // const [didUpdate, setUpdate] = useState(false);
    const text = children ? children.reverse().map(child => child.text).join('\n') : '';
    // const text = children ? children[children.length - 1].text : ''
    const position = (children && children.length) ? children[children.length - 1].position : 0;
    // console.log(children)
    useEffect(() => {
        onUpdate({current_position: position});
    }, [position])

    return <Container>
        <AceEditor
            value={text}
            width="90vw"
            style={{boxShadow: '0 3px 7px 0 rgba(0, 0, 0, 0.2), 0 4px 12px 0 rgba(0, 0, 0, 0.19)'}}
            name="logs"
            theme="terminal"
            fontSize={14}
            showGutter={false}
            readOnly={true}
        />
        <Button size="lg" variant="dark" onClick={() => { onUpdate({current_position: position}); }}>
            🔄
        </Button>
    </Container>
};