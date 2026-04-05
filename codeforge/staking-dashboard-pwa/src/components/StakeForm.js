import React, { useState, useEffect } from 'react';
import { useStake } from '../hooks/useStake';
import { useUnstake } from '../hooks/useUnstake';
import { useStakingData } from '../hooks/useStakingData';
import { NotificationManager } from './NotificationManager';
import { isOnline } from '../utils';

const NotificationBanner = ({ message, type }) => (
  <div className={`notification-banner ${type}`}>
    {message}
  </div>
);

const StakeForm = () => {
  const [amount, setAmount] = useState('');
  const [stakeType, setStakeType] = useState('stake');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  const { data: stakeData } = useStake();
  const { data: unstakeData = useUnstake();
  const { data: stakingData, isLoading: isDataLoading } = useStakingData();

  useEffect(() => {
    if (stakeError || unstakeError) {
      setError(stakeError || unstakeError);
      setIsLoading(false);
    }
  }, [stakeError, unstakeError]);

  const validateAmount = (value) => {
    const numValue = parseFloat(value);
    return !isNaN(numValue) && numValue > 0;
  };

  const validateAmount = (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    
    if (!validateAmount(amount)) {
      setError('Please enter a valid amount');
      return;
    }

    if (!isOnline()) {
      setError('No internet connection. Please check your network.');
      return;
    }

    try {
      if (stakeType === 'stake') {
        await stake(parseFloat(amount));
        setSuccess('Staking successful!');
      } else {
        await unstake(parseFloat(amount));
        setSuccess('Unstaking successful!');
      }
      setAmount('');
    } catch (err) {
      setError(err.message || 'Transaction failed');
    } finally {
      setAmount('');
    }
  };

  const handleAmountChange = (e) => {
    const value = e.target.value;
    if (value === '' || /^\d*\.?\d*$/.test(value)) {
      setAmount(value);
    }
  };

  return (
    <div className="stake-form-container">
      <div className="balance-info">
        <p>Available Balance: {stakingData?.balance} tokens</p>
        <p>Staked: {stakingData?.staked} tokens</p>
      </div>
      {isDataLoading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
        </div>
      )}
    </div>
  );
};

export default StakeForm;