import './App.css';
import User from './User'; // Import the new User component
import React, { useEffect, useState } from 'react';


function App() {
  return (
    <div>
      <div className="container mt-3">
        <User/>
      </div>
    </div>
  );
}

export default App;
