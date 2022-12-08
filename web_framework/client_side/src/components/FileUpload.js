import React, {useState} from "react";
import {Row, Col, Spinner} from "react-bootstrap";
import HebrewLabel from "./HebrewLabel";
import {COLORS, FILE_TYPES, SIZES} from "../constants";
import Container from "react-bootstrap/Container";
import Image from "./Image";
import FileDisplay from "./FileDisplay";

const uploadIcon = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/OOjs_UI_icon_upload.svg/1024px-OOjs_UI_icon_upload.svg.png'

const FileUpload = ({uploadFiles, files = [], size = SIZES.lg}) => {
    const [isDragging, setDragging] = useState(false);
    const [isLoading, setLoading] = useState(false);

    const parseFileList = (fileList) => {
        const data = []
        let uploaded_count = 0; // counter for the number of uploaded files
        Array.from(fileList).map((file) => { // for each file, collect the file's content
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                data.push({
                    content: reader.result,
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    last_modified: file.lastModifiedDate,
                });
                uploaded_count++; // increase counter
            };
            reader.onerror = error => console.error(error);
        });
        const loopTillDoneCollecting = () => {
            if (uploaded_count === fileList.length) {
                uploadFiles({files: data}); // upload files
            }
            else
                setTimeout(loopTillDoneCollecting, 100);
        };
        loopTillDoneCollecting();
    }

    const onDragLeave = () => { // when the file dragging is finished
        setDragging(false);
    }
    const onDragStart = (event) => { // when the file dragging is starting
        event.preventDefault();
        setDragging(true);
    }
    const onDrop = (event) => { // when the user stop dropped the file
        event.preventDefault()
        setLoading(true);
        setDragging(false);
        const files = event && event.dataTransfer && event.dataTransfer.files // get the files to a fileList
        if (files && files.length > 0) { // if files is not null or undefined
            setLoading(true);
            parseFileList(files);
            setTimeout(() => {
                setLoading(false);
            }, 1000); //fake loading state
        }
    }

    const styleDiv = {
        margin: '0 auto',
        background: isDragging ? '#ccc' : '#bbb',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '2px dashed',
        borderColor: isDragging ? 'gold' : 'grey'
    }

    const filesImages = files.map((file) => {
        return <FileDisplay {...file} />;
    });

    return filesImages.length === 0
        ? <Container
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onDragOver={onDragStart}
            style={styleDiv}
        >
            <HebrewLabel color={COLORS.BLACK} size={size}>
                יש לגרור את הקובץ לכאן
                <div style={{height: '5vh'}}>
                    {isLoading ? <Spinner animation="border" size="sm"/>
                    : <Image url={uploadIcon} scale={0.03}/>}
                </div>
            </HebrewLabel>
        </Container>
        : <Container><Row>{filesImages}</Row></Container>

};

export default FileUpload;