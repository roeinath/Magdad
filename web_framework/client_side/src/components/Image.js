import React from 'react';


const Image = ({url, scale}) => {
    return <img src={url} alt={'could not get image'} width={`${scale*500}vh`} height="auto" style={{maxWidth: '100%'}}/>;
};

export default Image;