import React from "react";
import FolderTree from "react-folder-tree";
import {SIZES, COLORS} from "../constants";


const treeState = {
    name: 'root',
    isOpen: true,   // this folder is opened, we can see it's children
    url: 'root',
    children: [
        {
            name: 'children 1',
            url: 'root/child1',
        },
        {
            name: 'children 2',
            url: 'root/child2',
            isOpen: false,
            children: [
                {name: 'children 2-1', url: 'root/child2/children2-1',},
                {name: 'children 2-2', url: 'root/child2/children2-2',},
            ],
        },
    ],
};


export default ({files = treeState, size, onFileClick}) => (
    <div style={{width: '20vw', overflowX: 'scroll'}}>
        <FolderTree
            data={files}
            showCheckbox={false}
            initOpenStatus="closed"
            indentPixels={20}
            onNameClick={({defaultOnClick, nodeData}) => {
                defaultOnClick();
                onFileClick(nodeData);
            }}
            readOnly
        />
        <style type="text/css">
            {`
            .TreeNode {
                direction: ltr; 
                font-size: ${SIZES[size]};
                display: flex;
            }
            .TreeNode:hover {
                color: ${COLORS.TALPIOT_CYAN};
                cursor: pointer;
            }
            ::-webkit-scrollbar {
              width: 5px;
            }
            ::-webkit-scrollbar-track {
              box-shadow: inset 0 0 5px grey; 
              border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb {
              background: ${COLORS.TALPIOT_BLUE}; 
              border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover {
              background: ${COLORS.TALPIOT_DARK_BLUE}; 
            }
            `}
        </style>
    </div>
);