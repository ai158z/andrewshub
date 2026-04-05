import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Agent {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'unknown';
  last_heartbeat: string;
  task_score: number;
  index: number;
}

const AgentStatus: React.FC<{ agents: Agent[] }> = ({ agents = [] }) => {
  const [agentStatus, setAgentStatus] = useState<Agent[]>(agents);

  useEffect(() => {
    const fetchAgentStatus = async () => {
      try {
        const response = await axios.get('/api/agents');
        setAgentStatus(response.data);
      } catch (error) {
        console.error('Error fetching agent data:', error);
      }
    };

    if (agents.length === 0) {
      fetchAgentStatus();
    }
  }, [agents]);

  return (
    <div>
      <h2>Agent Status</h2>
      <div className="agent-status">
        {agentStatus.map((agent) => (
          <div key={agent.id}>
            <h3>{agent.name}</h3>
            <p>Status: {agent.status}</p>
            <p>Last Heartbeat: {agent.last_heartbeat}</p>
            <p>Task Score: {agent.task_score}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentStatus;