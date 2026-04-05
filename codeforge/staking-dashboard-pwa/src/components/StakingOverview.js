import React, { useState, useEffect } from 'react';
import { fetchWithCache } from '../../utils';
import { isOnline } from '../../utils';

const StakingOverview = () => {
  const [totalStaked, setTotalStaked] = useState(0);
  const [totalRewards, setTotalRewards] = useState(0);
  const [stakerCount, setStakerCount] = useState(0);
  const [formattedStakerCount, setFormattedStakerCount] = useState('0');

  const fetchStakingData = async () => {
    try {
      if (!isOnline()) return;
      
      const response = await fetchWithCache('/api/staking-info');
      if (!response) return;
      
      setStakerCount(response.data.total_stakers);
      setTotalStaked(response.data.total_staked);
      setTotalRewards(response.data.total_rewards);
      setFormattedStakerCount(response.data.formatted_staker_count);
    } catch (error) {
      console.error('Error fetching staking data:', error);
    }
  };

  const formatStakerCount = (count) => {
    return new Intl.NumberFormat('en', {
      notation: 'compact',
      compactDisplay: 'short'
    }).format(count);
  };

  const formatTotalStaked = (amount) => {
    return new Intl.NumberFormat('en', {
      style: 'currency',
      currency: 'USD',
      currencyDisplay: 'narrowSymbol',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  };

  useEffect(() => {
    fetchStakingData();
  }, []);

  return (
    <div className="staking-overview">
      <div className="staking-summary">
        <h2>Staking Overview</h2>
        <div>Total Staked: {formatTotalStaked(totalStaked)}</div>
        <div>Total Rewards: {formatTotalStaked(totalRewards)}</div>
        <div>Staker Count: {formatStakerCount(stakerCount)}</div>
      </div>
    </div>
  );
};

export default StakingOverview;