import { useState, useEffect } from 'react';
import Link from 'next/link';
import axios from 'axios';
import AgentStatus from '../components/AgentStatus';
import SystemHealth from '../components/SystemHealth';
import { Agent } from '../types/agent';
import { Metric } from '../types/metric';

interface HomePageProps {
  agents: Agent[];
  metrics: Metric[];
}

export default function Home({ agents, metrics }: HomePageProps) {
  const [agentData, setAgentData] = useState<Agent[]>(agents || []);
  const [metricData, setMetricData] = useState<Metric[]>(metrics || []);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!agents || !metrics) {
        setLoading(true);
        try {
          const agentsResponse = await axios.get('/api/agents');
          const metricsResponse = await axios.get('/api/metrics');
          setAgentData(agentsResponse.data);
          setMetricData(metricsResponse.data);
        } catch (err) {
          setError('Failed to fetch dashboard data');
          console.error('Error fetching dashboard data:', err);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchData();
  }, [agents, metrics]);

  if (error) {
    return (
      <div className="container mx-auto p-4 py-16">
        <h1 className="text-2xl font-bold text-red-600">{error}</h1>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container mx-auto p-4 py-16">
        <div className="text-center">
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Agent Operations Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Monitor and manage your agent infrastructure
          </p>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">System Status</h2>
            <SystemHealth metrics={metricData} />
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Agent Status</h2>
            <AgentStatus agents={agentData} />
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-4">
              <Link href="/agents/dashboard" className="block">
                <button className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-150">
                  Agent Management
                </button>
              </Link>
              <Link href="/ops/dashboard" className="block">
                <button className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded transition duration-150">
                  Operations Dashboard
                </button>
              </Link>
              <Link href="/system/dashboard" className="block">
                <button className="w-full bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded transition duration-150">
                  System Metrics
                </button>
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export async function getServerSideProps() {
  try {
    const agentsResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/agents`);
    const metricsResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/metrics`);
    
    return {
      props: {
        agents: agentsResponse.data,
        metrics: metricsResponse.data,
      },
    };
  } catch (error) {
    console.error('Failed to fetch server-side data:', error);
    return {
      props: {
        agents: [],
        metrics: [],
      },
    };
  }
}