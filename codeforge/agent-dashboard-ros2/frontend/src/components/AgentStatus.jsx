import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

const AgentStatus = ({ agentData }) => {
  const [agent, setAgent] = useState(agentData);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({});

  useEffect(() => {
    setAgent(agentData);
    setEditData(agentData || {});
  }, [agentData]);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = async () => {
    try {
      const response = await api.put(`/agents/${agent.id}/status`, editData);
      setAgent(response.data);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating agent status:', error);
    }
  };

  const handleCancel = () => {
    setEditData(agent || {});
    setIsEditing(false);
  };

  const handleChange = (field, value) => {
    setEditData(prev => ({ ...prev, [field]: value }));
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-500';
      case 'inactive':
        return 'bg-gray-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-300';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active':
        return 'Active';
      case 'inactive':
        return 'Inactive';
      case 'error':
        return 'Error';
      default:
        return 'Unknown';
    }
  };

  if (!agent) {
    return <div>Loading...</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Agent Status</h2>
        <div className={`flex items-center px-3 py-1 rounded-full text-white ${getStatusColor(agent.status)}`}>
          <span>{getStatusText(agent.status)}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-700">Agent Information</h3>
          <p className="text-gray-600"><span className="font-medium">Name:</span> {agent.name}</p>
          <p className="text-gray-600"><span className="font-medium">ID:</span> {agent.id}</p>
          <p className="text-gray-600"><span className="font-medium">Type:</span> {agent.type}</p>
          <p className="text-gray-600"><span className="font-medium">Last Seen:</span> {agent.last_seen ? new Date(agent.last_seen).toLocaleString() : 'Never'}</p>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-700">Configuration</h3>
          {isEditing ? (
            <div>
              <div className="mb-2">
                <label className="block text-gray-700 text-sm font-bold mb-2">Name</label>
                <input
                  type="text"
                  value={editData.name || ''}
                  onChange={(e) => handleChange('name', e.target.value)}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
              </div>
              <div className="mb-2">
                <label className="block text-gray-700 text-sm font-bold mb-2">Status</label>
                <select
                  value={editData.status || 'active'}
                  onChange={(e) => handleChange('status', e.target.value)}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                >
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="error">Error</option>
                </select>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={handleSave}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                  Save
                </button>
                <button
                  onClick={handleCancel}
                  className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div>
              <p className="text-gray-600"><span className="font-medium">Name:</span> {agent.name}</p>
              <p className="text-gray-600"><span className="font-medium">Status:</span> {getStatusText(agent.status)}</p>
              <button
                onClick={handleEdit}
                className="mt-2 bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Edit
              </button>
            </div>
          )}
        </div>
      </div>
      {isEditing && (
        <div className="mt-4 text-sm text-gray-500">
          Editing mode: Make changes and click Save to update
        </div>
      )}
    </div>
  );
};

export default AgentStatus;