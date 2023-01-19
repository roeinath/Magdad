import React from 'react';
import Plot from 'react-plotly.js'
import {COLORS, FONTS, SIZES} from "../constants";

const plotData = [
  {
    x: [1, 2, 3],
    y: [1, 2, 3],
    type: 'scatter'
  }
];


const PlotlyFigure = ({
                       plotly_params
                     }) => {
  return (
    <Plot
      data={plotly_params.data}
      layout={plotly_params.layout}
    />
  );
};

export default PlotlyFigure;
