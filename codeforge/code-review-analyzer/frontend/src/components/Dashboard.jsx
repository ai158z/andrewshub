import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer, 
  PieChart, 
  Cell
} from 'recharts';
import { getRepositories, getAnalysis, getAnalysisResults } from '../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RepositoryList } from './RepositoryList';
import { AnalysisResult } from './AnalysisResult';
import { CodeViewer } from './CodeViewer';
import { VulnerabilityList } from './VulnerabilityList';
import { Repository } from './Repository';

export const Dashboard = () => {
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRepo, setSelectedRepo] = useState(null);

  useEffect(() => {
    const fetchRepositories = async () => {
      try {
        const repos = await getRepositories();
        setRepositories(repos);
      } catch (error) {
        console.error('Failed to fetch repositories:', error);
      } finally {
        if (loading) {
          setLoading(false);
        }
      }
    };

    fetchRepositories();
  }, []);

  const handleRepoSelect = (repo) => {
    setSelectedRepo(repo);
  };

  return (
    <div className="dashboard">
      <h1>Code Analysis Dashboard</h1>
      <RepositoryList repositories={repositories} onRepo={handleRepoSelect} />
      {selectedRepo && (
        <Repository repo={selectedRepo} />
      )}
    </div>
  );
};