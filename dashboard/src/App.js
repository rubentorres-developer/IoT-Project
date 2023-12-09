import './App.css';
import User from './User'; // Import the new User component
import React, { useEffect, useState } from 'react';


function App() {
  const [refreshCount, setRefreshCount] = useState(0);

  useEffect(() => {
    // Set up an interval to make requests every 1 second (1000 milliseconds)
    const intervalId = setInterval(() => {
      // Increment the refreshCount to trigger a re-render
      setRefreshCount(prevCount => prevCount + 1);
    }, 5000);

    // Clear the interval when the component unmounts to avoid memory leaks
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <div className="container mt-3">
        <User/>
      </div>
    </div>
  );
}

export default App;
