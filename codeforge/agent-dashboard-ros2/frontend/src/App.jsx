import React, { useState, useEffect } from 'react';
import DashboardLayout from './components/DashboardLayout';
import AgentStatus from './components/AgentStatus';
import SystemHealth from './components/SystemHealth';
import OperationalMetrics from './components/OperationalMetrics';
import ROS2Monitor from './components/ROS2Monitor';
import { api } from './services/api';

function App() {
  const [agents, setAgents] = useState([]);
  const [health, setHealth] = useState({});
  const [metrics, setMetrics] = useState([]);
  const [rosData, setRosData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [agentsResponse, healthResponse, metricsResponse, rosResponse] = await Promise.all([
          api.get('/api/agents'),
          api.get('/api/system/health'),
          api.get('/api/metrics'),
          api.get('/api/system/status')
        ]);

        setAgents(agentsResponse.data);
        setHealth(healthResponse.data);
        setMetrics(metricsResponse.data);
        setRosData(rosResponse.data);

        setLoading(false);
      } catch (err) {
        setError('Failed to load data');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <DashboardLayout>
      <div className="dashboard-grid">
        <div className="dashboard-section">
          <AgentStatus agentData={agents} />
        </div>
        <div className="dashboard-section">
          <SystemHealth healthData={health} />
        </div>
        <div className="dashboard-section">
          <OperationalMetrics metricsData={metrics} />
        </div>
        <div className="dashboard-section">
          <ROS2Monitor rosData={rosData} />
        </div>
      </div>
    </DashboardLayout>
  );
}

export default App;