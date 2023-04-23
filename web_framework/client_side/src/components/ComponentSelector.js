import React from "react";

import Button from "./Button";
import HebrewLabel from "./HebrewLabel";
import Form from "./Form";
import JsonSchemaForm from "./JsonSchemaForm";
import Table from "./Table";
import PopUp from "./PopUp";
import GridPanel from "./GridPanel";
import ComboBox from "./ComboBox";
import {pageContext} from "../stores/pageContext";
import StackPanel from "./StackPanel";
import ChartJsComponent from './ChartJsComponent';
import {FONTS} from "../constants";
import YnetComponent from "./YnetComponent";
import Image from "./Image";
import Toggle from "./Toggle";
import Slideshow from "./Slideshow";
import FileUpload from "./FileUpload";
import FileDisplay from "./FileDisplay";
import Scroller from "./Scroller";
import HyperLink from "./HyperLink";
import Accordion from "./Accordion";
import CodeBlock from "./CodeBlock";
import CodeEditor from "./CodeEditor";
import FileTree from "./FileTree";
import ViewLogs from "./ViewLogs";
import CountDown from "./CountDown";
import Markdown from "./Markdown";
import GoogleDocsDisplay from "./GoogleDocsDisplay";
import DownloadButton from "./DownloadButton";
import Card from './Card'
import GridView from "./GridView";
import Container from './Container'
import RichTextEditor from './RichTextEditor'
import TextInput from './TextInput'
// import PureHTML from "./PureHTML";


// return the component by its type
const ComponentSelector = ({type, text, action, ...props}) => {
    return (<pageContext.Consumer>
        {
            ({onEvent}) => {
                if (type === 'Label')
                    return <HebrewLabel font={FONTS.RUBIK} color={props.text_color} {...props}>{text}</HebrewLabel>
                if (type === 'Button')
                    // onClick checks if action is a function and passing data into it
                    return <Button text={text} color={props.text_color} onClick={() => onEvent(action, {}) } {...props}/>
                if (type === 'Toggle')
                    // onChange checks if action is a function and passing data into it
                    return <Toggle onChange={(data) => onEvent(action, data)} {...props}/>
                if (type === 'Form')
                    return <Form onSubmit={(data) => onEvent(action, data)} props={props}>{text}</Form>
                if (type === 'JsonSchemaForm')
                    return <JsonSchemaForm onSubmit={(data) => onEvent(action, data)} {...props}>{text}</JsonSchemaForm>
                if (type === 'DataGrid')
                    return <Table onSubmit={onEvent} props={props}>{text}</Table>
                if (type === 'PopUp')
                    // turns the com
                    return <PopUp onEvent={() => onEvent(action, {}) } props={props}/>
                if (type === 'GridPanel')
                    return (<GridPanel {...props}/>);
                if (type === 'ComboBox')
                    return <ComboBox placeHolder={text} onChoose={(body) => onEvent(action, body) } {...props} />
                if (type === 'StackPanel')
                    return <StackPanel {...props} />
                if (type === 'ChartJsComponent')
                    return <ChartJsComponent {...props} />
                if (type === 'image')
                    return <Image {...props} />
                if (type === 'scroller') {
                    return <Scroller text={text} children={props.children} {...props}/>
                }
                if (type === 'YnetComponent')
                    return <YnetComponent />
                if (type === 'Slideshow')
                    return <Slideshow {...props}/>
                if (type === 'UploadFile')
                    return <FileUpload uploadFiles={(data) => onEvent(action, data)} {...props} />
                if (type === 'DisplayFile')
                    return <FileDisplay {...props} onClick={() => onEvent(action, {})} />
                if (type === 'HyperLink')
                    return <HyperLink {...props} >{text}</HyperLink>
                if (type === 'Accordion')
                    return <Accordion {...props} />
                if (type === 'CodeBlock')
                    return <CodeBlock text={text} {...props} />
                if (type === 'CodeEditor')
                    return <CodeEditor text={text} onSubmitCode={(data) => onEvent(action, data)} {...props} />
                if (type === 'FileTree')
                    return <FileTree onFileClick={(data) => onEvent(action, data)} {...props} />
                if (type === 'LogViewer')
                    return <ViewLogs onUpdate={(data) => onEvent(action, data)} {...props} />
                if (type === 'DownloadButton')
                    return <DownloadButton text={text} actionUrl={action} {...props} />
                if (type === 'CountDown')
                    return <CountDown {...props} />
                if (type === 'Markdown')
                    return <Markdown text={text} {...props} />
                if (type === 'Divider')
                    return <div style={{margin: '7px 0', width: '32vw',borderTop: '1px solid rgba(0, 0, 0, 0.15)'}}/>
                if (type === 'GoogleDocsDisplay')
                    return <GoogleDocsDisplay {...props}/>
                if (type === 'Card')
                    return <Card {...props}/>
                if (type === 'GridView')
                    return <GridView {...props}/>
                if (type === 'Container')
                    return <Container {...props}/>
                if (type === 'RichTextEditor')
                    return <RichTextEditor onSave={(data) => onEvent(action, data)} {...props} />
                if (type === 'TextInput')
                    return <TextInput placeholder={text} font={FONTS.RUBIK} color={props.text_color} onChange={(data) => onEvent(action, data)} {...props}></TextInput>
            }
        }
    </pageContext.Consumer>);
};

export default ComponentSelector;