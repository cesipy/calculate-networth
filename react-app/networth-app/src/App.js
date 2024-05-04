// src/App.js
import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [networth, setNetworth] = useState(null);

  useEffect(() => {
    fetch('http://localhost:11111/networth')
      .then(response => response.json())
      .then(data => setNetworth(data.networth));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {networth ? `Net Worth: ${networth}` : 'Loading...'}
      </header>
    </div>
  );
}

export default App;