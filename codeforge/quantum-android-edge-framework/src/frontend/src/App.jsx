import React, { useState, useEffect } from 'react';
import NodeVisualizer from './components/NodeVisualization';
import SimulationDashboard from './components/SimulationDashboard';
import NodeMonitor from './components/NodeMonitor';
import { fetchNodeData } from './api/client';
import useQuantumEncryption from './hooks/useQuantumEncryption';
import useIITModels from './hooks/useIITModels';

const QuantumFrameworkApp = () => {
  const [nodes, setNodes] = useState([]);
  const [connections, setConnections] = useState([]);
  const [scenario, setScenario] = useState('');
  const [isSimulationActive, setIsSimulationActive] = useState(false);
  const [nodeData, setNodeData] = useState(null);
  const [encryptedState, setEncryptedState] = useQuantumEncryption();
  const [modelState, setModelState] = useIITModels();

  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Fetch initial node data
        const data = await fetchNodeData('main');
        setNodeData(data);
        
        // Initialize with default quantum nodes and connections
        setNodes(data.nodes || []);
        setConnections(data.connections || []);
        
        // Set initial scenario
        setScenario(data.scenario || 'default');
      } catch (error) {
        console.error('Failed to initialize application:', error);
      }
    };

    initializeApp();
  }, []);

  const handleNodeUpdate = (nodeId, config) => {
    setNodes(prevNodes => 
      prevNodes.map(node => 
        node.id === nodeId ? { ...node, ...config } : node
      )
    );
  };

  const handleSimulationToggle = () => {
    setIsSimulationActive(!isSimulationActive);
  };

  const handleScenarioChange = (newScenario) => {
    setScenario(newScenario);
  };

  return (
    <div className="quantum-framework-app">
      <header>
        <h1>Quantum Android Edge Framework</h1>
      </header>
      
      <main>
        <section className="visualization-section">
          <h2>Node Visualization</h2>
          <NodeVisualizer 
            nodes={nodes} 
            connections={connections} 
          />
        </section>

        <section className="simulation-section">
          <SimulationDashboard 
            scenario={scenario}
            isActive={isSimulationActive}
            onToggle={handleSimulationToggle}
            onScenarioChange={handleScenarioChange}
          />
        </section>

        <section className="monitoring-section">
          <h2>Node Status</h2>
          <NodeMonitor nodeData={nodeData} />
        </section>

        <section className="encryption-section">
          <h2>Quantum Encryption</h2>
          <div>State: {encryptedState ? 'Encrypted' : 'Not Encrypted'}</div>
        </section>

        <section className="iit-section">
          <h2>IIT Models</h2>
          <div>Model State: {modelState?.status || 'Inactive'}</div>
        </section>
      </main>
    </div>
  );
};

export default QuantumFrameworkApp;