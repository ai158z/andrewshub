import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import api from '../services/api';

const SystemHealth = ({ healthData }) => {
  const [systemMetrics, setSystemMetrics] = useState([]);
  const [agentMetrics, setAgentMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSystemHealth = async () => {
      try {
        setLoading(true);
        const [systemResponse, agentResponse] = await Promise.all([
          api.get('/api/system/health'),
          api.get('/api/metrics/system')
        ]);
        
        setSystemMetrics(Array.isArray(systemResponse.data.metrics) ? systemResponse.data.metrics : []);
        setAgentMetrics(Array.isArray(agentResponse.data.metrics) ? agentResponse.data.metrics : []);
        setError(null);
      } catch (err) {
        setError('Failed to fetch system health data');
        console.error('Error fetching system health:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSystemHealth();
    
    // Set up polling for real-time updates
    const interval = setInterval(fetchSystemHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="system-health">Loading system health data...</div>;
  }

  if (error) {
    return <div className="system-health error">Error: {error}</div>;
  }

  const renderSystemMetrics = () => (
    <div className="metrics-chart">
      <h3>System Metrics</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={systemMetrics}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="cpu_usage" 
            stroke="#8884d8" 
            activeDot={{ r: 8 }} 
            name="CPU Usage %" 
          />
          <Line 
            type="monotone" 
            dataKey="memory_usage" 
            stroke="#82ca9d" 
            name="Memory Usage %" 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );

  const renderAgentStatus = () => (
    <div className="agent-status">
      <h3>Agent Status</h3>
      <div className="status-grid">
        {agentMetrics.map((agent, index) => (
          <div key={agent.id || index} className="agent-card">
            <div className="agent-header">
              <h4>{agent.name}</h4>
              <span className={`status-badge ${agent.status}`}>{agent.status}</span>
            </div>
            <div className="agent-details">
              <p>CPU: {agent.metrics?.cpu?.toFixed(1) || 'N/A'}%</p>
              <p>Memory: {agent.metrics?.memory?.toFixed(1) || 'N/A'}%</p>
              <p>Uptime: {agent.uptime || 'N/A'}s</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const calculateHealthScore = () => {
    if (!systemMetrics || systemMetrics.length === 0) return 100;
    const avgCpu = systemMetrics.reduce((sum, m) => sum + (m.cpu_usage || 0), 0) / systemMetrics.length;
    const avgMemory = systemMetrics.reduce((sum, m) => sum + (m.memory_usage || 0), 0) / systemMetrics.length;
    const healthScore = Math.round(100 - (avgCpu + avgMemory) / 2);
    return Math.max(healthScore, 0);
  };

  return (
    <div className="system-health">
      <div className="health-summary">
        <div className="health-score">
          <h2>System Health: {systemMetrics.length > 0 ? calculateHealthScore() : 100}%</h2>
        </div>
        {renderSystemMetrics()}
        {agentMetrics.length > 0 && renderAgentStatus()}
      </div>
    </div>
  );
};

export default SystemHealth;