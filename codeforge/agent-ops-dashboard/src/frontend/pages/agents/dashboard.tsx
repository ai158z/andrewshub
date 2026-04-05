import { useState, useEffect } from 'react';
import axios from 'axios';
import AgentStatus from '../../components/AgentStatus';
import SystemHealth from '../../components/SystemHealth';

interface Agent {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'warning';
  last_heartbeat: string;
  performance: number;
}

interface Metric {
  id: string;
  agent_id: string;
  metric_type: string;
  value: number;
  timestamp: string;
}

export default function AgentDashboard() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await axios.get<Agent[]>('/api/agents');
        setAgents(response.data);
      } catch (err) {
        setError('Failed to fetch agents');
        console.error(err);
      }
    };

    const fetchMetrics = async () => {
      try {
        const response = await axios.get<Metric[]>('/api/metrics');
        setMetrics(response.data);
      } catch (err) {
        setError('Failed to fetch metrics');
        console.error(err);
      }
    };

    const fetchData = async () => {
      try {
        await Promise.all([fetchAgents(), fetchMetrics()]);
      } catch (err) {
        setError('Failed to fetch dashboard data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="p-6">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Agent Operations Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">System Health</h2>
          <SystemHealth metrics={metrics} />
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Agent Status</h2>
          <AgentStatus agents={agents} />
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">Agent Performance Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map((agent) => (
            <div key={agent.id} className="border p-4 rounded">
              <h3 className="font-bold text-lg">{agent.name}</h3>
              <div className="mt-2">
                <span className={`inline-block w-3 h-3 rounded-full mr-2 ${agent.status === 'online' ? 'bg-green-500' : agent.status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'}`}></span>
                <span className="capitalize">{agent.status}</span>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Last heartbeat: {new Date(agent.last_heartbeat).toLocaleString()}
              </p>
              <div className="mt-2">
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className="bg-blue-600 h-2.5 rounded-full" 
                    style={{ width: `${agent.performance}%` }}
                  ></div>
                </div>
                <p className="text-xs mt-1">Performance: {agent.performance}%</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}