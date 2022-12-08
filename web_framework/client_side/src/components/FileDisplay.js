import React from "react";
import {Col} from "react-bootstrap";
import HebrewLabel from "./HebrewLabel";
import {FILE_TYPES, SIZES} from "../constants";
import Image from "./Image";

const defaultOnClick = () => {
};

const FileDisplay = ({name, file_type, file_size, last_modified, url, onClick = defaultOnClick}) => {
    let imgUrl = FILE_TYPES.FILE.icon;
    Object.values(FILE_TYPES).forEach((fileType) => {
        if (file_type && file_type.includes(fileType.type)) {
            imgUrl = fileType.icon;
        }
    })
    return <Col onClick={onClick}>
        <a href={url} target='_blank'>
            <Image url={imgUrl} scale={0.1}/>
        </a>
        <br/>
        <HebrewLabel size={SIZES.md}>{name}</HebrewLabel>
    </Col>
};

export default FileDisplay;