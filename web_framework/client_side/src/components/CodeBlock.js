import React from 'react';
import {CodeBlock as CodeBlockComponent, CopyBlock, dracula} from "react-code-blocks";
import Card from "react-bootstrap/Card";


const CodeBlock = ({text, language, highlight_lines, is_copyable, width, height}) => {
    const highlight = highlight_lines !== null ? highlight_lines.join(',') : ''
    const boxShadow = '0 3px 7px 0 rgba(0, 0, 0, 0.2), 0 4px 12px 0 rgba(0, 0, 0, 0.19)'
    is_copyable = is_copyable && text.split('\n').length > 1;
    return <Card dir="ltr" style={{textAlign: 'left', fontSize: '0.9vw', boxShadow: boxShadow,
        width: width, height: height, maxWidth: width, maxHeight: height}}>
        {is_copyable ? <CopyBlock
            text={text}
            language={language}
            theme={dracula}
            highlight={highlight}
            codeBlock
        /> : <CodeBlockComponent
            text={text}
            language={language}
            theme={dracula}
            showLineNumbers={false}
            highlight={highlight}
        />}
    </Card>
};

export default CodeBlock;