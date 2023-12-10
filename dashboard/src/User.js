import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PieChart from './PieChart';
import ComboChart from './ComboChart';
import ColumnChart from './ColumnChart';

const User = () => {
  const [userData, setUserData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to fetch data from the API
  const fetchData = async () => {
    try {
      const response = await axios.get('/api/data');
      setUserData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
      setError(error);
    }
  };

  // useEffect to initiate the interval and clean it up when the component unmounts
  useEffect(() => {
    // Fetch data initially
    fetchData();

    // Set up the interval to fetch data every 5 seconds
    const intervalId = setInterval(() => {
      fetchData();
    }, 1000);

    // Clean up the interval when the component is unmounted
    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error.message}</p>;
  }

  let week_distance_run = 0.0;
  let week_distance_walk = 0.0;
  userData.week.forEach(day => {
    week_distance_run += day.distances.run;
    week_distance_walk += day.distances.walk;
  });

  console.log(week_distance_run);
  console.log(week_distance_walk);


  let calories_by_day_week = [];
  let distance_by_day_week = [];
  let duration_by_day_week = [];
  userData.week.forEach(day => {
    calories_by_day_week.push(day.calories.run + day.calories.walk);
    distance_by_day_week.push(day.distances.run + day.distances.walk);
    duration_by_day_week.push(day.durations.run + day.durations.walk);
  })

  // Calculate total weekly values
  const totalWeekDurationsRun = userData.week.reduce((total, day) => total + day.durations.run, 0);
  const totalWeekDurationsWalk = userData.week.reduce((total, day) => total + day.durations.walk, 0);
  const totalWeekDistancesRun = userData.week.reduce((total, day) => total + day.distances.run, 0);
  const totalWeekDistancesWalk = userData.week.reduce((total, day) => total + day.distances.walk, 0);
  const totalWeekCaloriesRun = userData.week.reduce((total, day) => total + day.calories.run, 0);
  const totalWeekCaloriesWalk = userData.week.reduce((total, day) => total + day.calories.walk, 0);


  return (
    <div>
      <div>
        <h2>Today's Data</h2>
        <table class="table table-bordered" style={{ border: '1px solid black', width: '70%' }}>
          <thead class="thead-dark">
            <tr>
              <th>Activity</th>
              <th>Durations</th>
              <th>Distances</th>
              <th>Calories</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Run</td>
              <td>{userData.today.durations.run} seconds</td>
              <td>{userData.today.distances.run.toFixed(2)} m</td>
              <td>{userData.today.calories.run.toFixed(2)} kcal</td>
            </tr>
            <tr>
              <td>Walk</td>
              <td>{userData.today.durations.walk} seconds</td>
              <td>{userData.today.distances.walk.toFixed(2)} m</td>
              <td>{userData.today.calories.walk.toFixed(2)} kcal</td>
            </tr>
          </tbody>
        </table>
        {/* Display Weekly Data */}
        <h2>Weekly Data</h2>
        <table class="table table-bordered" style={{ border: '1px solid black', width: '70%' }}>
          <thead class="thead-dark">
            <tr>
              <th>Activity</th>
              <th>Durations</th>
              <th>Distances</th>
              <th>Calories</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Run</td>
              <td>{totalWeekDurationsRun} seconds</td>
              <td>{totalWeekDistancesRun.toFixed(2)} m</td>
              <td>{totalWeekCaloriesRun.toFixed(2)} kcal</td>
            </tr>
            <tr>
              <td>Walk</td>
              <td>{totalWeekDurationsWalk} seconds</td>
              <td>{totalWeekDistancesWalk.toFixed(2)} m</td>
              <td>{totalWeekCaloriesWalk.toFixed(2)} kcal</td>
            </tr>
          </tbody>
        </table>
        {/* Display Monthly Data */}
        <h2>Monthly Data</h2>
        <table class="table table-bordered" style={{ border: '1px solid black', width: '70%' }}>
          <thead class="thead-dark">
            <tr scope="row">
              <th >Activity</th>
              <th>Durations</th>
              <th>Distances</th>
              <th>Calories</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Run</td>
              <td>{userData.month.durations.run} seconds</td>
              <td>{userData.month.distances.run.toFixed(2)} m</td>
              <td>{userData.month.calories.run.toFixed(2)} kcal</td>
            </tr>
            <tr>
              <td>Walk</td>
              <td>{userData.month.durations.walk} seconds</td>
              <td>{userData.month.distances.walk.toFixed(2)} m</td>
              <td>{userData.month.calories.walk.toFixed(2)} kcal</td>
            </tr>
          </tbody>
        </table>
      </div>



      <h3 class="mt-4">Distance:</h3>
      <ul>
        <div class="row">
          <div class="col-md-4">
            <PieChart runDistance={userData.today.distances.run} walkDistance={userData.today.distances.walk} activity={"Today"} id="chart-2" />
          </div>
          <div class="col-md-4">
            <PieChart runDistance={week_distance_run} walkDistance={week_distance_walk} activity={"Week"} id="chart-3" />
          </div>
          <div class="col-md-4">
            <PieChart runDistance={userData.month.distances.run} walkDistance={userData.month.distances.walk} activity={"Month"} id="chart-1" />
          </div>
        </div>
        <h3 class="mt-4">Weekly Status</h3>
        <ComboChart duration={duration_by_day_week} distance={distance_by_day_week} />
        <ColumnChart calories={calories_by_day_week} />
      </ul>
    </div>
  );
};

export default User;
