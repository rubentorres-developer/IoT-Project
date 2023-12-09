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

const ComboChart = ({ duration, distance }) => {
  useEffect(() => {
    if (!duration || !distance) {
      // Handle the case where any of the arrays is not available yet
      return;
    }

    const drawChart = () => {
      const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

      const dataTable = new google.visualization.DataTable();
      dataTable.addColumn('string', 'Day');
      dataTable.addColumn('number', 'Duration (seconds)');
      dataTable.addColumn('number', 'Distance (meters)');

      // Populate data rows
      daysOfWeek.forEach((day, index) => {
        const rowData = [day, duration[index], distance[index]];
        dataTable.addRow(rowData);
      });

      const options = {
        title: 'Activity Each Day Of The Week',
        seriesType: 'bars', // Use bars for duration, distance, and calories
        series: {
          0: { targetAxisIndex: 0 }, // Duration on the primary axis
          1: { targetAxisIndex: 1 }, // Distance on the secondary axis
        },
        vAxes: {
          0: { title: 'Duration (seconds)' },
          1: { title: 'Distance (meters)' },
        },
      };

      const chart = new google.visualization.ComboChart(document.getElementById('combo-chart'));
      chart.draw(dataTable, options);
    };

    loadGoogleCharts().then(() => {
      google.charts.load('current', { packages: ['corechart'] });
      google.charts.setOnLoadCallback(drawChart);
    });

    return () => {
      // Cleanup if needed
    };
  }, [duration, distance]);

  return <div id="combo-chart" style={{ width: '100%', height: '300px' }} />;
};

export default ComboChart;
