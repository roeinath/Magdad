import React from 'react';


const GoogleDocsDisplay = ({url, width, height}) => {
    return <iframe src={url} width={width} height={height} style={{maxWidth: '100%'}}/>;
};

export default GoogleDocsDisplay;