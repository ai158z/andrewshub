import { useState, useEffect } from 'react';
import axios from 'axios';
import AgentStatus from '../../components/AgentStatus';
import SystemHealth from '../../components/SystemHealth';
import { Agent } from '../../types/agent';
import { Metric } from '../../types/metric';

interface DashboardData {
  agents: Agent[];
  metrics: Metric[];
}

export default function OpsDashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [agentsRes, metricsRes] = await Promise.all([
          axios.get<Agent[]>('/api/agents'),
          axios.get<Metric[]>('/api/metrics')
        ]);
        
        setDashboardData({
          agents: agentsRes.data,
          metrics: metricsRes.data
        });
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch dashboard data');
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="text-center p-8">Loading dashboard...</div>;
  if (error) return <div className="text-red-500 text-center p-8">Error: {error}</div>;
  if (!dashboardData) return <div className="text-center p-8">No data available</div>;

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Operations Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">System Health</h2>
          <SystemHealth metrics={dashboardData.metrics} />
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Agent Status</h2>
          <AgentStatus agents={dashboardData.agents} />
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">System Metrics Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 p-4 rounded">
            <h3 className="font-medium text-blue-700">Active Agents</h3>
            <p className="text-2xl font-bold">
              {dashboardData.agents.filter(a => a.status === 'active').length}
            </p>
          </div>
          <div className="bg-green-50 p-4 rounded">
            <h3 className="font-medium text-green-700">Healthy Metrics</h3>
            <p className="text-2xl font-bold">
              {dashboardData.metrics.filter(m => m.status === 'healthy').length}
            </p>
          </div>
          <div className="bg-yellow-50 p-4 rounded">
            <h3 className="font-medium text-yellow-700">Warnings</h3>
            <p className="text-2xl font-bold">
              {dashboardData.metrics.filter(m => m.status === 'warning').length}
            </p>
          </div>
        </div>
      </div>
  );
}