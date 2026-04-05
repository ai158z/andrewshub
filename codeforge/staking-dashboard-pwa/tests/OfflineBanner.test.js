import React from 'react';
import { render, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import { useNetworkStatus } from '../hooks/useNetworkStatus';

jest.mock('../hooks/useNetworkStatus', () => {
  return {
    useNetworkStatus: jest.fn()
  };
});

jest.mock('../hooks/useNetworkStatus', () => {
  const originalModule = jest.requireActual('../hooks/useNetworkStatus');
  return {
    useNetworkStatus: Object.assign({}, originalModule, {
      useNetworkStatus: jest.fn()
    })
});

const mockUseNetworkStatus = useNetworkStatus;

const originalModule = jest.requireActual('./src/components/OfflineBanner');
const { useNetworkStatus } = originalModule;

global.navigator.onLine = true;

jest.mock('./src/components/OfflineBanner', () => {
  const originalModule = jest.requireActual('./src/components/OfflineBanner');
  return {
    useNetworkStatus: jest.fn()
  };
});

const OfflineBanner = originalModule;

global.navigator.onLine = true;

const mockUseNetworkStatus = useNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = 'You are currently offline. Some features may be unavailable.';

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const not.toBe(false);

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus;

const mockUseNetworkStatus = mockUseNetworkStatus