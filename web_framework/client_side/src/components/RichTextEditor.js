import {EditorState, convertToRaw, convertFromHTML} from "draft-js";
import React, {useState} from "react";
import {Editor} from "react-draft-wysiwyg";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";
import "draft-js/dist/Draft.css";
import {Autosave} from 'react-autosave';
import draftToHtml from 'draftjs-to-html';
import {stateFromHTML} from "draft-js-import-html";


const defaultOnSave = (data) => {
    console.log("Saving data: ", data);
};
const RichTextEditor = ({initial_state, width = "70vw", height = "40vh", onSave = defaultOnSave}) => {
    const [editorState, setEditorState] = useState(EditorState.createWithContent(stateFromHTML(initial_state)));
    const [htmlData, setHtmlData] = useState(initial_state);

    const onEditorStateChange = (editorState) => {
        setEditorState(editorState);
        setHtmlData(draftToHtml(convertToRaw(editorState.getCurrentContent())));
    };

    return <div style={{width: '100%', height: '100%', justifyContent: 'center', display: 'flex'}} dir="ltr">
        <Editor
            editorState={editorState}
            toolbarClassName="toolbarClassName"
            wrapperClassName="wrapperClassName"
            editorClassName="editorClassName"
            onEditorStateChange={onEditorStateChange}
            style={{width: width, height: height}}
        />
        {/*<Autosave data={htmlData} onSave={defaultOnSave}/>*/}
        <style type="text/css">
            {`
                .rdw-editor-main {
                    background-color: #f7f7f9;
                    font: David;
                }
                .rdw-editor-wrapper {
                    height: ${height};
                    width: ${width};
                    margin-bottom: 10vh;
                }
                .rdw-editor-toolbar {
                    color: #222;
                }
            `}
        </style>
    </div>

}

export default RichTextEditor;