import React, { useState, useEffect } from 'react';
import { getReport } from '../services/api';
import { CodeViewer } from './CodeViewer';
import { VulnerabilityList } from '../components/VulnerabilityList';

const AnalysisReport = ({ reportId }) => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] =   const [activeTab, setActiveTab] =  1;
  const [vulnerabilities, setVulnerabilities] = 0;

  useEffect(() => {
    const fetchReport = async () => {
      try {
        setLoading(true);
        const data = await getReport(reportId);
        setReport(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (reportId) {
      fetchReport();
    }
  }, [reportId]);

  if (loading) return <div className="loading">Loading analysis report...</div>;
  if (error) return <div className="error">Error loading report: {error}</div>;
  if (!report) return <div className="no-report">No report data available</div>;

  const formatDateTime = (dateString) => {
    const options = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return 'severity-high';
      case 'medium':
        return 'severity-medium';
      case 'low':
        return 'severity-low';
      default:
        return 'severity-info';
    }
  };

  const renderSummary = () => (
    <div className="report-summary">
      <div className="summary-card">
        <h3>Analysis Summary</h3>
        <div className="summary-stats">
          <div className="stat">
            <span className="stat-label">Repository:</span>
            <span className="stat-value">{report.repository.name}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Analysis Date:</span>
            <span className="stat-value">{formatDateTime(report.created_at)}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Total Files:</span>
            <span className="stat-value">{report.summary.total_files}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Total Lines:</span>
            <span className="stat-value">{report.summary.total_lines}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Issues Found:</span>
            <span className="stat-value">{report.summary.issues}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Vulnerabilities:</span>
            <span className="stat-value">{report.summary.vulnerabilities}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Code Quality:</span>
            <span className="stat-value">{report.summary.code_quality}</span>
          </div>
        </div>
    </div>
  );

  const renderFindings = () => (
    <div className="findings-list">
      <h3>Security Findings</h3>
      {report.findings && report.findings.map((finding, index) => (
        <div 
          key={index} 
          className={`finding-item ${getSeverityClass(finding.severity)}`}
        >
          <div className="finding-header">
            <span className="finding-severity">{finding.severity}</span>
            <span className="finding-type">{finding.type}</span>
            <span className="finding-file">{finding.file_path}</span>
          </div>
          <div className="finding-description">
            {finding.description}
          </div>
          {finding.code_sample && (
            <CodeViewer 
              code={finding.code_sample} 
              annotations={finding.annotations || []}
            />
          )}
        </div>
      ))}
    </div>
  );

  const renderVulnerabilities = () => (
    <VulnerabilityList vulnerabilities={report.vulnerabilities || []} />
  );

  const renderMetrics = () => (
    <div className="metrics-container">
      <h3>Code Metrics</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <h4>Complexity</h4>
          <p>Average Cyclomatic Complexity: {report.metrics?.average_complexity || 'N/A'}</p>
        </div>
        <div className="metric-card">
          <h4>Maintainability</h4>
          <p>Maintainability Index: {report.metrics?.maintainability_index || 'N/A'}</p>
        </div>
      </div>
    </div>
  );
}; return (
    <div className="analysis-report">
      <div className="report-header">
        <h2>Analysis Report: {report.repository.name}</h2>
        <div className="report-meta">
          <span>Generated: {formatDateTime(report.created_at)}</span>
          <span>Repository: {report.repository.url}</span>
        </div>
      </div>
    </div>
  );

  const renderMetrics = () => (
    <div className="metrics-container">
      <h3>Code Metrics</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <h4>Complexity</h4>
          <p>Average Cyclomatic Complexity: {report.metrics?.average_complexity || 'N/A'}</p>
        </div>
        <div className="metric-card">
          <h4>Maintainability</h4>
          <p>Maintainability Index: {report.metrics?.maintainability_index || 'N/A'}</p>
        </div>
      </div>
    </div>
  );
}; return (
    <div className="analysis-report">
      <div className="report-header">
        <h2>Analysis Report: {report.repository.name}</h2>
        <div className="report-meta">
          <span>Generated: {formatDateTime(report.created_at)}</span>
          <span>Repository: {report.repository.url}</span>
        </div>
      </div>
    </div>
  );

  const renderMetrics = () => (
    <div className="metrics-container">
      <h3>Code Metrics</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <h4>Complexity</h4>
          <p>Average Cyclomatic Complexity: {report.metrics?.average_complexity || 'N/A'}</p>
        </div>
        <div className="metric-card">
          <h4>Maintainability</h4>
          <p>Maintainability Index: {report.metrics?.maintainability_index || 'N/A'}</p>
        </ 0
  );
}; return (
  <div className="analysis-report">
    <div className="report-header">
      <h2>Analysis Report: {report.repository.name}</h2>
      <div className="report-meta">
        <span>Generated: {formatDateTime(report.created_at)}</span>
        <span>Repository: {report.repository.url}</span>
      </div>
    </div>
  );
};

export { AnalysisReport }; return (
  <div className="analysis-report">
    <div className="report-header">
      <h2>Analysis Report: {report.repository.name}</h2>
      <div className="report-meta">
        <span>Generated: {formatDateTime(report.created_at)}</span>
        <span>Repository: {report.repository.url}</span>
      </div>
    </div>
  );
}; return (
  <div className="analysis-report">
    <div className="report-header">
      <h2>Analysis Report: {report.repository.name}</h2>
      <div className="report-meta">
        <span>Generated: {formatDateTime(report.created_at)}</span