import React, { useState, useEffect } from 'react';
import { 
  AgentStatus, 
  SystemHealth, 
  OperationalMetrics, 
  ROS2Monitor 
} from './AgentComponents';
import { api } from '../services/api';

const DashboardLayout = ({ children }) => {
  const [agents, setAgents] = useState([]);
  const [systemHealth, setSystemHealth] = useState({});
  const [metrics, setMetrics] = useState([]);
  const [rosData, setRosData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [agentsRes, healthRes, metricsRes, rosRes] = await Promise.allSettled([
          api.get('/api/agents'),
          api.get('/api/system/health'),
          api.get('/api/metrics'),
          api.get('/api/system/ros2')
        ]);

        if (agentsRes.status === 'fulfilled') setAgents(agentsRes.value.data);
        if (healthRes.status === 'fulfilled') setSystemHealth(healthRes.value.data);
        if (metricsRes.status === 'fulfilled') setMetrics(metricsRes.value.data);
        if (rosRes.status === 'fulfilled') setRosData(rosRes.value.data);
        
        setError(null);
      } catch (err) {
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="dashboard-error">{error}</div>;
  }

  return (
    <div className="dashboard-layout">
      <header className="dashboard-header">
        <h1>Agent Dashboard</h1>
      </header>
      
      <div className="dashboard-content">
        <nav className="dashboard-sidebar">
          <div className="nav-item">
            <AgentStatus agentData={agents} />
          </div>
          <div className="nav-item">
            <SystemHealth healthData={systemHealth} />
          </div>
          <div className="nav-item">
            <OperationalMetrics metricsData={metrics} />
          </div>
          <div className="nav-item">
            <ROS2Monitor rosData={rosData} />
          </div>
        </nav>
        
        <main className="dashboard-main-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;