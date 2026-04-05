import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const OperationalMetrics = ({ metricsData }) => {
  const [metrics, setMetrics] = useState([]);
  const [labels, setLabels] = useState([]);
  const [cpuData, setCpuData] = useState([]);
  const [memoryData, setMemoryData] = useState([]);
  const [networkData, setNetworkData] = useState([]);

  useEffect(() => {
    if (metricsData && Array.isArray(metricsData) && metricsData.length > 0) {
      const newLabels = metricsData.map((_, index) => `Point ${index + 1}`);
      const newCpuData = metricsData.map(metric => metric.cpu_usage || 0);
      const newMemoryData = metricsData.map(metric => metric.memory_usage || 0);
      const newNetworkData = metricsData.map(metric => metric.network_usage || 0);

      setLabels(newLabels);
      setCpuData(newCpuData);
      setMemoryData(newMemoryData);
      setNetworkData(newNetworkData);
      setMetrics(metricsData);
    }
  }, [metricsData]);

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'CPU Usage (%)',
        data: cpuData,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        tension: 0.1,
      },
      {
        label: 'Memory Usage (MB)',
        data: memoryData,
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        tension: 0.1,
      },
      {
        label: 'Network Usage (KB/s)',
        data: networkData,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Operational Metrics Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      }
    }
  };

  return (
    <div className="metrics-container">
      <Line data={data} options={options} />
    </div>
  );
};

export default OperationalMetrics;