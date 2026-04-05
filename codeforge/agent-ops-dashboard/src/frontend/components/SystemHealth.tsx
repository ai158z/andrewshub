import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

interface HealthMetric {
  name: string;
  value: number;
  timestamp: string;
}

const SystemHealth: React.FC<{ metrics?: HealthMetric[] }> = ({ metrics }) => {
  const [healthData, setHealthData] = useState<HealthMetric[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealthMetrics = async () => {
      try {
        const response = await axios.get('/api/metrics/system-health');
        setHealthData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load system health metrics');
        setLoading(false);
      }
    };

    if (metrics && metrics.length > 0) {
      setHealthData(metrics);
      setLoading(false);
    } else {
      fetchHealthMetrics();
    }
  }, [metrics]);

  if (loading) {
    return <div className="p-4">Loading system health data...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  // Create a stable key based on the metric data for the list items
  const getMetricKey = (metric: HealthMetric, index: number) => {
    return `${metric.name}-${index}`;
  };

  return (
    <div className="system-health-container p-6">
      <h2 className="text-xl font-bold mb-4">System Health Metrics</h2>
      
      <div className="health-chart-container">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={healthData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" name="Health Value" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="health-metrics-list mt-8">
        <h3 className="text-lg font-semibold mb-2">Current Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {healthData.map((metric, index) => (
            <div key={getMetricKey(metric, index)} className="bg-white p-4 rounded-lg shadow">
              <h4 className="font-medium">{metric.name}</h4>
              <p className="text-2xl font-bold">{metric.value}</p>
              <p className="text-sm text-gray-500">{new Date(metric.timestamp).toLocaleString()}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SystemHealth;