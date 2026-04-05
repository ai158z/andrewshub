import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { getReport } from '../services/api';
import AnalysisReport from './AnalysisReport';

jest.mock('../services/api', () => ({
  getReport: jest.fn()
}));

const mockReportData = {
  id: '123',
  repository: {
    name: 'test-repo',
    url: 'https://github.com/test/repo'
  },
  created_at: '2023-01-01T12:00:00Z',
  summary: {
    total_files: 10,
    total_lines: 1000,
    total_issues: 5,
    vulnerabilities: 2,
    code_quality: 'A'
  },
  findings: [
    {
      severity: 'high',
      type: 'SQL Injection',
      file_path: 'src/db.js',
      description: 'Potential SQL injection vulnerability',
      code_sample: 'SELECT * FROM users WHERE id = ' + userId,
      annotations: []
    }
  ],
  vulnerabilities: [
    {
      id: 'vuln-1',
      severity: 'high',
      title: 'High Severity Vulnerability',
      description: 'A critical security issue'
    }
  ],
  metrics: {
    average_complexity: 5.5,
    maintainability_index: 75
  }
};

describe('AnalysisReport', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('shows loading state initially', () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    expect(screen.getByText('Loading analysis report...')).toBeInTheDocument();
  });

  test('displays error when API call fails', async () => {
    getReport.mockRejectedValueOnce(new Error('API Error'));
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('Error loading report: API Error')).toBeInTheDocument();
    });
  });

  test('renders summary tab by default', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Summary')).toBeInTheDocument();
    });
  });

  test('renders report data correctly when loaded', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Report: test-repo')).toBeInTheDocument();
    });
  });

  test('switches to findings tab when clicked', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const findingsButton = screen.getByText('Security Findings');
      userEvent.click(findingsButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Security Findings')).toBeInTheDocument();
    });
  });

  test('switches to vulnerabilities tab when clicked', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const vulnButton = screen.getByText('Vulnerabilities');
      userEvent.click(vulnButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('High Severity Vulnerability')).toBeInTheDocument();
    });
  });

  test('switches to metrics tab when clicked', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const metricsButton = screen.getByText('Code Metrics');
      userEvent.click(metricsButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Code Metrics')).toBeInTheDocument();
    });
  });

  test('renders correct severity class for high severity finding', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const findingItem = screen.getByText('SQL Injection').closest('.finding-item');
      expect(findingItem).toHaveClass('severity-high');
    });
  });

  test('renders correct severity class for medium severity finding', async () => {
    const mediumSeverityReport = {
      ...mockReportData,
      findings: [{
        ...mockReportData.findings[0],
        severity: 'medium'
      }]
    };
    
    getReport.mockResolvedValueOnce(mediumSeverityReport);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const findingItem = screen.getByText('SQL Injection').closest('.finding-item');
      expect(findingItem).toHaveClass('severity-medium');
    });
  });

  test('renders correct severity class for low severity finding', async () => {
    const lowSeverityReport = {
      ...mockReportData,
      findings: [{
        ...mockReportData.findings[0],
        severity: 'low'
      }]
    };
    
    getReport.mockResolvedValueOnce(lowSeverityReport);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const findingItem = screen.getByText('SQL Injection').closest('.finding-item');
      expect(findingItem).toHaveClass('severity-low');
    });
  });

  test('renders correct severity class for critical severity finding', async () => {
    const criticalSeverityReport = {
      ...mockReportData,
      findings: [{
        ...mockReportData.findings[0],
        severity: 'critical'
      }]
    };
    
    getReport.mockResolvedValueOnce(criticalSeverityReport);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const findingItem = screen.getByText('SQL Injection').closest('.finding-item');
      expect(findingItem).toHaveClass('severity-high');
    });
  });

  test('shows no report message when no data', async () => {
    getReport.mockResolvedValueOnce(null);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('No report data available')).toBeInTheDocument();
    });
  });

  test('formats date time correctly', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText(/Generated: .*2023.*/)).toBeInTheDocument();
    });
  });

  test('renders CodeViewer when code sample exists', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('SELECT * FROM users WHERE id = ')).toBeInTheDocument();
    });
  });

  test('does not render CodeViewer when no code sample', async () => {
    const reportWithoutCodeSample = {
      ...mockReportData,
      findings: [{
        ...mockReportData.findings[0],
        code_sample: null
      }]
    };
    
    getReport.mockResolvedValueOnce(reportWithoutCodeSample);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.queryByText('SELECT * FROM users WHERE id = ')).not.toBeInTheDocument();
    });
  });

  test('renders VulnerabilityList component', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const vulnButton = screen.getByText('Vulnerabilities');
      userEvent.click(vulnButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('High Severity Vulnerability')).toBeInTheDocument();
    });
  });

  test('renders metrics data correctly', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const metricsButton = screen.getByText('Code Metrics');
      userEvent.click(metricsButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Average Cyclomatic Complexity: 5.5')).toBeInTheDocument();
    });
  });

  test('renders correct repository name', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Report: test-repo')).toBeInTheDocument();
    });
  });

  test('renders correct total files count', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      const summaryButton = screen.getByText('Summary');
      userEvent.click(summaryButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Total Files:')).toBeInTheDocument();
      expect(screen.getByText('10')).toBeInTheDocument();
    });
  });

  test('renders correct total issues count', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('Issues Found:')).toBeInTheDocument();
      expect(screen.getByText('5')).toBeInTheDocument();
    });
  });

  test('renders correct vulnerability count', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('Vulnerabilities:')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument();
    });
  });

  test('renders correct code quality grade', async () => {
    getReport.mockResolvedValueOnce(mockReportData);
    render(<AnalysisReport reportId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText('Code Quality:')).toBeInTheDocument();
      expect(screen.getByText('A')).toBeInTheDocument();
    });
  });
});