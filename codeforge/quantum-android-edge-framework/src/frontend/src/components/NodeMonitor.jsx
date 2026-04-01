import React, { useState, useEffect } from 'react';
import { fetchNodeData } from '../api/client';
import { useQuantumEncryption } from '../hooks/useQuantumEncryption';
import { useIITModels } from '../hooks/useIITModels';

const NodeMonitor = ({ nodeData }) => {
  const [nodeStatus, setNodeStatus] = useState(nodeData);
  const [encryptedState, setEncryptedState] = useQuantumEncryption();
  const [modelState, setModelState] = useIITModels();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await fetchNodeData(nodeStatus.id);
        setNodeStatus(data);
        setEncryptedState(data.encryptedState);
        setModelState(data.modelState);
      } catch (err) {
        setError('Failed to fetch node data');
      } finally {
        setLoading(false);
      }
    };

    const interval = setInterval(fetchData, 5000);
    fetchData();

    return () => clearInterval(interval);
  }, [nodeStatus.id, setEncryptedState, setModelState]);

  if (loading) {
    return <div className="node-monitor">Loading node data...</div>;
  }

  if (error) {
    return <div className="node-monitor">Error: {error}</div>;
  }

  return (
    <div className="node-monitor">
      <h2>Node Monitoring Dashboard</h2>
      <div className="node-info">
        <h3>Node: {nodeStatus.id}</h3>
        <div className="status-indicators">
          <div className="indicator">
            <span>Status: </span>
            <span className={nodeStatus.online ? 'online' : 'offline'}>
              {nodeStatus.online ? 'Online' : 'Offline'}
          </div>
          <div className="indicator">
            <span>Load: {nodeStatus.load}</span>
          </div>
          <div className="indicator">
            <span>Latency: {nodeStatus.latency}ms</span>
          </div>
        </div>
      </div>
      <div className="node-configuration">
        <h4>Configuration</h4>
        <div className="config-item">
          <span>Quantum Encryption State: {encryptedState}</span>
        </div>
        <div className="config-item">
          <span>IIT Model State: {modelState}</span>
        </div>
      </div>
    </div>
  );
};

export default NodeMonitor;