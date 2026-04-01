import React, { useState, useEffect } from 'react';
import { useQuantumEncryption } from '../hooks/useQuantumEncryption';
import { useIITModels } from '../hooks/useIITModels';
import NodeVisualizer from './NodeVisualization';
import NodeMonitor from './NodeMonitor';
import { fetchNodeData, updateNodeConfiguration } from '../api/client';

const SimulationDashboard = ({ scenario, isActive }) => {
  const [modelState, setModelState] = useIITModels();
  const [encryptedState, setEncryptedState] = useQuantumEncryption();
  const [simulationData, setSimulationData] = useState(null);
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [nodeData, setNodeData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadSimulationData = async () => {
      if (!isActive) return;
      
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/api/simulations/${scenario}`);
        const data = await response.json();
        
        if (response.ok) {
          setSimulationData(data);
          if (data.nodes) {
            setNodes(data.nodes);
          }
          if (data.connections) {
            setConnections(data.connections);
          }
        } else {
          throw new Error(data.detail || 'Failed to load simulation data');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadSimulationData();
  }, [scenario, isActive]);

  useEffect(() => {
    const updateNodeStatus = async () => {
      if (!isActive || !nodes.length) return;
      
      try {
        const updatedNodeData = {};
        for (const node of nodes) {
          const data = await fetchNodeData(node.id);
          updatedNodeData[node.id] = data;
        }
        setNodeData(updatedNodeData);
      } catch (err) {
        setError(err.message);
      }
    };

    const interval = setInterval(updateNodeStatus, 5000);
    return () => clearInterval(interval);
  }, [isActive, nodes]);

  const handleNodeConfigUpdate = async (nodeId, config) => {
    try {
      const result = await updateNodeConfiguration(nodeId, config);
      if (result.success) {
        setNodeData(prev => ({
          ...prev,
          [nodeId]: { ...prev[nodeId], ...config }
        }));
      }
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading simulation data...</div>;
  }

  if (error) {
    return <div className="dashboard-error">Error: {error}</div>
  }

  return (
    <div className="simulation-dashboard">
      <h2>Simulation Dashboard: {scenario}</h2>
      <div className="dashboard-content">
        <div className="visualization-section">
          <NodeVisualizer 
            nodes={nodes} 
            connections={connections} 
          />
        </div>
        <div className="monitoring-section">
          <NodeMonitor 
            nodeData={nodeData} 
            onNodeConfigUpdate={handleNodeConfigUpdate}
          />
        </div>
        <div className="controls-section">
          <button 
            onClick={() => {
              setModelState(modelState);
              setEncryptedState(encryptedState);
            }}
            disabled={!isActive}
          >
            Update Simulation
          </button>
        </div>
      </div>
    </div>
  );
};

export default SimulationDashboard;