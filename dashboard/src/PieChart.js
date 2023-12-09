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

const PieChart = ({ runDistance, walkDistance, id, activity }) => {
  useEffect(() => {
    const drawChart = () => {
      const data = google.visualization.arrayToDataTable([
        ['Activity', 'Distance'],
        ['Run Distance', runDistance],
        ['Walk Distance', walkDistance],
      ]);

      const options = {
        title: `${activity}`,
        pieHole: 0.4,
        legend: { position: 'bottom' },
      };

      const chart = new google.visualization.PieChart(document.getElementById(id));
      chart.draw(data, options);
    };

    loadGoogleCharts().then(() => {
      google.charts.load('current', { packages: ['corechart'] });
      google.charts.setOnLoadCallback(drawChart);
    });

    return () => {
      // Cleanup if needed
    };
  }, [runDistance, walkDistance, id]); // Include id in the dependency array

  return <div id={id} style={{ height: '300px'}} />;
};

export default PieChart;

