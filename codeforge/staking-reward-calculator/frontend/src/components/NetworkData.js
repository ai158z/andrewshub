import React, { Component } from 'react';
import { fetchNetworkStats } from '../api/client';
import './NetworkData.css';

class NetworkData extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stats: null,
      loading: true,
      error: null
    };
  }

  componentDidMount() {
    this.loadNetworkStats();
  }

  loadNetworkStats = async () => {
    try {
      const response = await fetchNetworkStats();
      this.setState({
        stats: response.data,
        loading: false
      });
    } catch (error) {
      this.setState({
        error: error.message,
        loading: false
      });
    }
  }

  render() {
    const { stats, loading, error } = this.state;

    if (loading) {
      return <div className="network-data">Loading network data...</div>;
    }

    if (error) {
      return <div className="network-data error">Error: {error}</div>;
    }

    return (
      <div className="network-data">
        <h2>Network Statistics</h2>
        {stats && (
          <div className="stats-container">
            <div className="stat-item">
              <span className="stat-label">Total Validators:</span>
              <span className="stat-value">{stats.validators_count}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Active Stake:</span>
              <span className="stat-value">{stats.active_stake} ATOM</span>
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default NetworkData;