import React, { Component } from 'react';
import axios from 'axios';

class CalculatorForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stake: '',
      duration: '',
      network: 'ethereum',
      results: null,
      networks: [],
      loading: false,
      error: null
    };
  }

  async componentDidMount() {
    try {
      const response = await axios.get('/api/networks');
      this.setState({ networks: response.data });
    } catch (error) {
      console.error('Failed to load networks:', error);
      this.setState({ error: 'Failed to load networks' });
    }
  }

  handleChange = (e) => {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  };

  handleSubmit = async (e) => {
    e.preventDefault();
    const { stake, duration, network } = this.state;
    
    if (!stake || !duration) {
      this.setState({ error: 'Please fill in all fields' });
      return;
    }

    if (parseFloat(stake) <= 0) {
      this.setState({ error: 'Stake must be greater than 0' });
      return;
    }

    if (parseInt(duration, 10) <= 0) {
      this.setState({ error: 'Duration must be greater than 0' });
      return;
    }

    this.setState({ loading: true, error: null });
    
    try {
      const response = await axios.post('/api/calculate', {
        stake: parseFloat(stake),
        duration: parseInt(duration, 10),
        network
      });
      
      this.setState({ results: response.data, loading: false });
      if (this.props.onCalculate) {
        this.props.onCalculate(response.data);
      }
    } catch (error) {
      console.error('Calculation error:', error);
      this.setState({ 
        error: 'Calculation failed', 
        loading: false 
      });
    }
  };

  render() {
    const { stake, duration, network, networks, loading, error } = this.state;
    
    return (
      <form onSubmit={this.handleSubmit} className="calculator-form">
        <div>
          <label>
            Stake Amount:
            <input 
              type="number" 
              name="stake" 
              value={stake} 
              onChange={this.handleChange} 
              step="any" 
              min="0"
              required 
            />
          </label>
        </div>
        
        <div>
          <label>
            Duration (days):
            <input 
              type="number" 
              name="duration" 
              value={duration} 
              onChange={this.handleChange} 
              min="1"
              max="3650"
              required 
            />
          </label>
        </div>
        
        <div>
          <label>
            Network:
            <select 
              name="network" 
              value={network} 
              onChange={this.handleChange}
            >
              <option value="ethereum">Ethereum</option>
              {networks.map(net => (
                <option key={net.value} value={net.value}>
                  {net.label}
                </option>
              ))}
            </select>
          </label>
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Calculating...' : 'Calculate Rewards'}
        </button>
        
        {error && <div className="error">{error}</div>}
      </form>
    );
  }
}

export default CalculatorForm;