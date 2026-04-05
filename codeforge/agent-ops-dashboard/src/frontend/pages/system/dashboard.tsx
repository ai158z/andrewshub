import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

interface MetricData {
  timestamp: string;
  network_in: number;
  network_out: number;
  storage_used: number;
  storage_total: number;
}

interface SystemMetrics {
  networkIn: number[];
  networkOut: number[];
  storageUsed: number[];
  storageTotal: number[];
  timestamps: string[];
}

export default function SystemDashboard() {
  const [metrics, setMetrics] = useState<SystemMetrics>({
    networkIn: [],
    networkOut: [],
    storageUsed: [],
    storageTotal: [],
    timestamps: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get('/api/system/metrics');
        const data: MetricData[] = response.data;
        
        const networkIn: number[] = [];
        const networkOut: number[] = [];
        const storageUsed: number[] = [];
        const storageTotal: number[] = [];
        const timestamps: string[] = [];
        
        data.forEach((item: MetricData) => {
          networkIn.push(item.network_in);
          networkOut.push(item.network_out);
          storageUsed.push(item.storage_used);
          storageTotal.push(item.storage_total);
          timestamps.push(item.timestamp);
        });
        
        setMetrics({
          networkIn,
          networkOut,
          storageUsed,
          storageTotal,
          timestamps
        });
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching metrics:', err);
        setError('Failed to load system metrics');
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  if (loading) {
    return <div className="text-center py-8">Loading system metrics...</div>;
  }

  if (error) {
    return <div className="text-center py-8 text-red-500">{error}</div>;
  }

  const chartData = metrics.timestamps.map((timestamp, index) => ({
    timestamp,
    networkIn: metrics.networkIn[index] || 0,
    networkOut: metrics.networkOut[index] || 0,
    storageUsed: metrics.storageUsed[index] || 0,
    storageTotal: metrics.storageTotal[index] || 0
  }));

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">System Infrastructure Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Network Traffic</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="networkIn" 
                  stroke="#8884d8" 
                  name="Network In (MB/s)" 
                  strokeWidth={2}
                />
                <Line 
                  type="monotone" 
                  dataKey="networkOut" 
                  stroke="#82ca9d" 
                  name="Network Out (MB/s)" 
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Storage Utilization</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="storageUsed" 
                  stroke="#ff7300" 
                  name="Storage Used (GB)" 
                  strokeWidth={2}
                />
                <Line 
                  type="monotone" 
                  dataKey="storageTotal" 
                  stroke="#d00000" 
                  name="Storage Total (GB)" 
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium">Current Status</h3>
          <p className="mt-2">System is operating normally</p>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium">Network Health</h3>
          <p className="mt-2">All systems operational</p>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium">Storage Health</h3>
          <p className="mt-2">35% capacity used</p>
        </div>
      </div>
    </div>
  );
}