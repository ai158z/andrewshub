import React, { Component } from 'react';
import axios from 'axios';
import ChartComponent from './ChartComponent';

class ResultsDisplay extends Component {
  constructor(props) {
    super(props);
    this.state = {
      results: null,
      chartData: null,
      loading: false,
      error: null
    };
  }

  componentDidMount() {
    this.fetchResults();
  }

  fetchResults = async () => {
    this.setState({ loading: true, error: null });
    
    try {
      const response = await axios.get('/api/results');
      const { results, chartData } = response.data;
      
      this.setState({
        results,
        chartData,
        loading: false
      });
    } catch (error) {
      this.setState({
        loading: false,
        error: 'Failed to fetch results'
      });
    }
  };

  renderResults = () => {
    const { results } = this.state;
    if (!results) return null;

    return (
      <div className="results-container">
        <h3>Calculation Results</h3>
        <div className="result-item">
          <span className="result-label">Total Rewards:</span>
          <span className="result-value">{results.totalRewards} tokens</span>
        </div>
        <div className="result-item">
          <span className="result-label">APR:</span>
          <span className="result-value">{results.apr}%</span>
        </div>
        <div className="result-item">
          <span className="result-label">Duration:</span>
          <span className="result-value">{results.duration} days</span>
        </div>
      </div>
    );
  };

  renderChart = () => {
    const { chartData } = this.state;
    if (!chartData) return null;

    return <ChartComponent data={chartData} />;
  };

  render() {
    const { loading, error } = this.state;
    
    if (loading) {
      return <div className="loading">Loading...</div>;
    }
    
    if (error) {
      return <div className="error">{error}</div>;
    }

    return (
      <div className="results-display">
        {this.renderResults()}
        {this.renderChart()}
      </div>
    );
  }
}

export default ResultsDisplay;