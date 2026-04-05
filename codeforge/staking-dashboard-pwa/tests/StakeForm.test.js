import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import StakeForm from '../src/components/StakeForm';
import * as useStake from '../src/hooks/useStake';
import * as useUnstake from '../src/hooks/useUnstake';
import * as useStakingData from '../src/hooks/useStakingData';
import * as utils from '../src/utils';

jest.mock('../src/hooks/useStake', () => ({
  useStake: jest.fn()
}));

jest.mock('../src/hooks/useUnstake', () => ({
  useUnstake: jest.fn()
}));

jest.mock('../src/hooks/useStakingData', () => ({
  useStakingData: jest.fn()
}));

jest.mock('../src/utils', () => ({
  isOnline: jest.fn(() => true)
}));

describe('StakeForm', () => {
  beforeEach(() => {
    useStake.useStake.mockReturnValue({
      stake: jest.fn(),
      isStaking: false,
      stakeError: null
    });
    
    useUnstake.useUnstake.mockReturnValue({
      unstake: jest.fn(),
      isUnstaking: false,
      unstakeError: null
    });
    
    useStakingData.useStakingData.mockReturnValue({
      stakingData: { balance: '1000', staked: '500' },
      isLoading: false
    });
  });

  test('renders stake form with correct elements', () => {
    render(<StakeForm />);
    expect(screen.getByText('Stake Tokens')).toBeInTheDocument();
    expect(screen.getByLabelText('Amount')).toBeInTheDocument();
    expect(screen.getByLabelText('Action')).toBeInTheDocument();
    expect(screen.getByText('Stake')).toBeInTheDocument();
  });

  test('allows numeric input for amount field', () => {
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    fireEvent.change(amountInput, { target: { value: '123.45' } });
    expect(amountInput).toHaveValue('123.45');
  });

  test('prevents non-numeric input in amount field', () => {
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    fireEvent.change(amountInput, { target: { value: 'abc' } });
    expect(amountInput).toHaveValue('');
  });

  test('validates positive amount input', async () => {
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const submitButton = screen.getByText('Stake');
    
    fireEvent.change(amountInput, { target: { value: '-5' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Please enter a valid amount')).toBeInTheDocument();
    });
  });

  test('shows error when amount is not a number', async () => {
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const submitButton = screen.getByText('Stake');
    
    fireEvent.change(amountInput, { target: { value: 'abc' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Please enter a valid amount')).toBeInTheDocument();
    });
  });

  test('displays staking data when available', () => {
    useStakingData.useStakingData.mockReturnValue({
      stakingData: { balance: '1000', staked: '500' },
      isLoading: false
    });
    
    render(<StakeForm />);
    
    expect(screen.getByText('Available Balance: 1000 tokens')).toBeInTheDocument();
    expect(screen.getByText('Staked: 500 tokens')).toBeInTheDocument();
  });

  test('shows loading state during staking', () => {
    useStake.useStake.mockReturnValue({
      stake: jest.fn(),
      isStaking: true,
      stakeError: null
    });
    
    render(<StakeForm />);
    expect(screen.getByText('Processing...')).toBeInTheDocument();
  });

  test('shows error when no internet connection', async () => {
    utils.isOnline.mockReturnValueOnce(false);
    
    render(<StakeForm />);
    const submitButton = screen.getByText('Stake');
    const amountInput = screen.getByLabelText('Amount');
    
    fireEvent.change(amountInput, { target: { value: '100' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('No internet connection. Please check your network.')).toBeInTheDocument();
    });
  });

  test('calls stake function when staking', async () => {
    const mockStake = jest.fn();
    useStake.useStake.mockReturnValue({
      stake: mockStake,
      isStaking: false,
      stakeError: null
    });
    
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const submitButton = screen.getByText('Stake');
    
    fireEvent.change(amountInput, { target: { value: '100' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockStake).toHaveBeenCalledWith(100);
    });
  });

  test('calls unstake function when unstaking', async () => {
    const mockUnstake = jest.fn();
    useUnstake.useUnstake.mockReturnValue({
      unstake: mockUnstake,
      isUnstaking: false,
      unstakeError: null
    });
    
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const typeSelect = screen.getByLabelText('Action');
    const submitButton = screen.getByText('Unstake');
    
    fireEvent.change(amountInput, { target: { value: '50' } });
    fireEvent.change(typeSelect, { target: { value: 'unstake' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockUnstake).toHaveBeenCalledWith(50);
    });
  });

  test('displays success message after staking', async () => {
    const mockStake = jest.fn().mockResolvedValue();
    useStake.useStake.mockReturnValue({
      stake: mockStake,
      isStaking: false,
      stakeError: null
    });
    
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const submitButton = screen.getByText('Stake');
    
    fireEvent.change(amountInput, { target: { value: '100' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Staking successful!')).toBeInTheDocument();
    });
  });

  test('displays error message on transaction failure', async () => {
    const mockStake = jest.fn().mockRejectedValue(new Error('Transaction failed'));
    useStake.useStake.mockReturnValue({
      stake: mockStake,
      isStaking: false,
      stakeError: null
    });
    
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const submitButton = screen.getByText('Stake');
    
    fireEvent.change(amountInput, { target: { value: '100' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Transaction failed')).toBeInTheDocument();
    });
  });

  test('disables form fields when loading', () => {
    useStakingData.useStakingData.mockReturnValue({
      stakingData: { balance: '1000', staked: '500' },
      isLoading: true
    });
    
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const typeSelect = screen.getByLabelText('Action');
    const submitButton = screen.getByText('Stake');
    
    expect(amountInput).toBeDisabled();
    expect(typeSelect).toBeDisabled();
    expect(submitButton).toBeDisabled();
  });

  test('disables submit button when amount is empty', () => {
    render(<StakeForm />);
    const submitButton = screen.getByText('Stake');
    expect(submitButton).toBeDisabled();
  });

  test('enables submit button when amount is entered', () => {
    render(<StakeForm />);
    const amountInput = screen.getByLabelText('Amount');
    const submitButton = screen.getByText('Stake');
    
    expect(submitButton).toBeDisabled();
    
    fireEvent.change(amountInput, { target: { value: '100' } });
    
    expect(submitButton).toBeEnabled();
  });

  test('shows correct button text for staking', () => {
    render(<StakeForm />);
    expect(screen.getByText('Stake')).toBeInTheDocument();
  });

  test('shows correct button text for unstaking', () => {
    render(<StakeForm />);
    const typeSelect = screen.getByLabelText('Action');
    fireEvent.change(typeSelect, { target: { value: 'unstake' } });
    expect(screen.getByText('Unstake')).toBeInTheDocument();
  });

  test('shows correct button text when processing', () => {
    useStake.useStake.mockReturnValue({
      stake: jest.fn(),
      isStaking: true,
      stakeError: null
    });
    
    render(<StakeForm />);
    expect(screen.getByText('Processing...')).toBeInTheDocument();
  });
});