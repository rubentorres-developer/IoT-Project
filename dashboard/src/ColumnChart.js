/* eslint-disable */
import React, { useEffect } from 'react';

const loadGoogleCharts = () => {
  const script = document.createElement('script');
  script.src = 'https://www.gstatic.com/charts/loader.js';
  script.async = true;
  document.head.appendChild(script);

  return new Promise((resolve) => {
    script.onload = () => {
      resolve();
    };
  });
};

const ColumnChart = ({ calories }) => {
  useEffect(() => {
    if (!calories) {
      // Handle the case where calories data is not available yet
      return;
    }

    const drawChart = () => {
        const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      
        const data = google.visualization.arrayToDataTable([
          ['Day', 'Calories'],
          ...calories.map((calories, index) => [daysOfWeek[index], calories]),
        ]);
      
        const options = {
          title: 'Calories Burned Each Day Of The Week',
          legend: { position: 'none' },
        };
      
        const chart = new google.visualization.ColumnChart(document.getElementById('column-chart'));
        chart.draw(data, options);
    };
      

    loadGoogleCharts().then(() => {
      google.charts.load('current', { packages: ['corechart'] });
      google.charts.setOnLoadCallback(drawChart);
    });

    return () => {
      // Cleanup if needed
    };
  }, [calories]);

  return <div id="column-chart" style={{ width: '100%', height: '300px' }} />;
};

export default ColumnChart;