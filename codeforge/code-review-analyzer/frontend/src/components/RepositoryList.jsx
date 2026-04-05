import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, Button, TextField, List, ListItem, ListItemText, Typography, Box, CircularProgress } from '@mui/material';
import { Add as AddIcon, Sync as SyncIcon } from '@mui/icons-material';

const RepositoryList = () => {
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newRepoUrl, setNewRepoUrl] = useState('');

  useEffect(() => {
    fetchRepositories();
  }, []);

  const fetchRepositories = async () => {
    try {
      // Mock implementation since we don't have the actual API
      // In a real implementation, this would fetch from your API
      const mockRepos = [
        { id: 1, name: 'repo1', url: 'https://github.com/user/repo1' },
        { id: 2, name: 'repo2', url: 'https://github.com/user/repo2' }
      ];
      setRepositories(mockRepos);
      setError(null);
    } catch (err) {
      setError('Failed to fetch repositories');
    } finally {
      setLoading(false);
    }
  };

  const handleAddRepository = async () => {
    if (!newRepoUrl) return;
    
    try {
      // Mock implementation for adding repository
      const newRepo = {
        id: repositories.length + 1,
        name: `repo-${Date.now()}`,
        url: newRepoUrl
      };
      setRepositories([...repositories, newRepo]);
      setNewRepoUrl('');
    } catch (err) {
      setError('Failed to add repository');
    }
  };

  const handleSyncRepository = async (repoId) => {
    try {
      // Mock implementation for syncing
      console.log(`Syncing repository ${repoId}`);
      // In a real implementation, this would call the sync API
    } catch (err) {
      setError('Failed to sync repository');
    }
  };

  const handleAddRepoUrlChange = (e) => {
    setNewRepoUrl(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleAddRepository();
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Card>
      <CardHeader title="Repositories" />
      <CardContent>
        <Box mb={2}>
          <TextField
            label="Add Repository URL"
            value={newRepoUrl}
            onChange={handleAddRepoUrlChange}
            onKeyPress={handleKeyPress}
            fullWidth
            variant="outlined"
            helperText="Enter GitHub repository URL"
          />
          <Button
            startIcon={<AddIcon />}
            variant="contained"
            color="primary"
            onClick={handleAddRepository}
            fullWidth
            sx={{ mt: 1 }}
          >
            Add Repository
          </Button>
        </Box>
        
        {error && (
          <Typography color="error" variant="body2" align="center" gutterBottom>
            {error}
          </Typography>
        )}
        
        <List>
          {repositories.map((repo) => (
            <ListItem
              key={repo.id}
              secondaryAction={
                <Button
                  startIcon={<SyncIcon />}
                  onClick={() => handleSyncRepository(repo.id)}
                  variant="outlined"
                  size="small"
                >
                  Sync
                </Button>
              }
              sx={{ pr: 2 }}
            >
              <ListItemText 
                primary={repo.name} 
                secondary={repo.url} 
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default RepositoryList;