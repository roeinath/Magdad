import React from 'react';

import ChartComponent from 'react-chartjs-2';

const ChartJsComponent = ({chart, options, width, height}) => {

    return <ChartComponent
            type={chart.type}
            data={chart.data}
            options={options}
            width={width}
            height={height}
            // style={{minWidth: width, minHeight: height}}
        />
};

export default ChartJsComponent;