import React from "react";
import {Modal} from "react-bootstrap";
import ComponentSelector from "./ComponentSelector";
import StackPanel from "./StackPanel";
import Image from "./Image";
import Button from "react-bootstrap/Button";


const PopUp = ({props, onEvent}) => {
    const handleClose = () => {
        onEvent && onEvent();
    };
    const closeImg = "https://freesvg.org/img/close-button.png"

    return <Modal show={props.is_shown} onHide={handleClose} dir="rtl">
		<Modal.Header dir="rtl">
			<Modal.Title id="example-modal-sizes-title-sm">
				{props.title}
			</Modal.Title>
			{
				props.is_cancelable && <Button variant="link" onClick={handleClose}>
					<Image url={closeImg} scale={0.05}/>
				</Button>
			}
		</Modal.Header>
		<Modal.Body>
			<StackPanel children={props.children} orientation={1}/>
		</Modal.Body>
    </Modal>
};

export default PopUp;
