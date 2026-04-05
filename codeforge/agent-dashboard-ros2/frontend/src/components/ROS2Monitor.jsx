import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AgentStatus from './AgentStatus';
import SystemHealth from './SystemHealth';
import OperationalMetrics from './OperationalMetrics';
import DashboardLayout from './DashboardLayout';

const ROS2Monitor = ({ rosData }) => {
  const [systemHealth, setSystemHealth] = useState(null);
  const [agentData, setAgentData] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSystemData = async () => {
      try {
        const systemResponse = await axios.get('/api/system/health');
        setSystemHealth(systemResponse.data);
        
        const agentsResponse = await axios.get('/api/agents');
        setAgentData(agentsResponse.data);
        
        const metricsResponse = await axios.get('/api/metrics');
        setMetrics(metricsResponse.data);
        
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch system data');
        setLoading(false);
      }
    };

    fetchSystemData();
    
    // Set up polling for real-time updates
    const interval = setInterval(() => {
      fetchSystemData();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div>Loading ROS2 system status...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <DashboardLayout>
      <div className="ros2-monitor">
        <h1>ROS2 System Monitor</h1>
        
        {systemHealth && (
          <SystemHealth healthData={systemHealth} />
        )}
        
        <div className="agent-metrics">
          <h2>Agent Status</h2>
          {agentData.map(agent => (
            <AgentStatus 
              key={agent.id} 
              agentData={agent} 
            />
          ))}
        </div>
        
        <div className="operational-metrics">
          <h2>Operational Metrics</h2>
          <OperationalMetrics metricsData={metrics} />
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ROS2Monitor;