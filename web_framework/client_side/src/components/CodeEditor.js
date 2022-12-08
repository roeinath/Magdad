import React, {useCallback, useState} from "react";
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/mode-text";
import "ace-builds/src-noconflict/theme-dracula";
import "ace-builds/src-noconflict/theme-cobalt";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/theme-tomorrow_night_bright";
import "ace-builds/src-noconflict/theme-terminal";
import "ace-builds/src-noconflict/ext-language_tools";


export default ({text, width = "70vw", height = "60vh", language, theme, editable, onSubmitCode, ...props}) => {
    const [editorCode, setEditorCode] = useState(text);
    const onChange = () => {
    };
    const updateContent = useCallback(
        code => {
            setEditorCode(code)
            onChange(code)
        }, [editorCode]
    );
    if (!editable && text !== editorCode) {
        updateContent(text);
    }
    const style = {boxShadow: '0 3px 7px 0 rgba(0, 0, 0, 0.2), 0 4px 12px 0 rgba(0, 0, 0, 0.19)'}
    const onSubmit = () => {
        onSubmitCode({data: editorCode})
    }
    const commands = [
        {
            name: "save",
            bindKey: {win: "Ctrl-S", mac: "Command-S"},
            exec: onSubmit
        }
    ];
    return (
        <AceEditor
            width={width}
            height={height}
            value={editorCode}
            onChange={updateContent}
            onBlur={onSubmit}
            commands={commands}
            style={style}
            name="ace-editor"
            mode={language}
            theme={theme}
            fontSize={14}
            showGutter
            highlightActiveLine
            enableLiveAutocompletion
            enableBasicAutocompletion
        />
    )
}