import React from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import {Container} from "react-bootstrap";
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import {darcula} from 'react-syntax-highlighter/dist/esm/styles/prism';
import gfm from "remark-gfm";

export default ({text}) => {
    return <Container style={{width: "200vh"}}>
        <ReactMarkdown
            rehypePlugins={[rehypeRaw]}
            children={text}
            style={{text: {fontSize: 18}}}
            remarkPlugins={[gfm]}
            components={{
                code({node, inline, className, children, ...props}) {
                    const match = /language-(\w+)/.exec(className || '')
                    return !inline && match ? (
                        <SyntaxHighlighter
                            dir="ltr"
                            children={String(children).replace(/\n$/, '')}
                            style={darcula}
                            language={match[1]}
                            PreTag="div"
                            {...props}
                        />
                    ) : (
                        <code className={className} {...props}>
                            {children}
                        </code>
                    )
                }
            }}/>
        <style type="text/css">{
            `table, tr, td, th {
              border: 1px solid #000;
            }`
        }</style>
    </Container>
}

