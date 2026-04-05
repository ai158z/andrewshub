import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  const [calculationResult, setCalculationResult] = useState(null);
  const [networkStats, setNetworkStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Staking Reward Calculator</h1>
      </header>
      <main>
        <div>
          <h2>Network Statistics</h2>
          {networkStats && (
            <div>
              <p>Total Validators: {networkStats.totalValidators}</p>
              <p>Active Validators: {networkStats.activeValidators}</p>
              <p>Network Status: {networkStats.status}</p>
            </div>
          )}
        </div>
        
        <div>
          <h2>Reward Calculation</h2>
          {loading && <p>Loading...</p>}
          {error && <p>Error: {error}</p>}
          {calculationResult && (
            <div>
              <p>Estimated Annual Reward: {calculationResult.annualReward} tokens</p>
              <p>Estimated Monthly Reward: {calculationResult.monthlyReward} tokens</p>
              <p>Estimated Daily Reward: {calculationResult.dailyReward} tokens</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;