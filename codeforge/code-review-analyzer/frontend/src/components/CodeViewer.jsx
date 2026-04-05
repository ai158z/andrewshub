import React, { useState, useEffect } from 'react';
import { getAnalysis }4
function CodeViewer({ code, annotations }) {
  const [highlightedCode, setHighlightedCode] = useState([]);
  const [lineNumbers, setLineNumbers] = useState([]);
  const [findings, setFindings] = useState([]);

  useEffect(() => {
    const newFindings = annotations.map(ann => ({
      line: ann.line,
      message: ann.message,
      type: ann.type,
      severity: ann.severity
    }));

    setFindings(newFindings);
    const lines = code.split('\n');
    setLineNumbers(Array.from({ length: lines.length }, (_, i) => i + 1));
    setHighlightedCode(lines);
  }, [code, annotations]);

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'error': return 'bg-red-100 border-l-4 border-red-500';
      case 'warning': return 'bg-yellow-100 border-l-4 border-yellow-500';
      case 'info': return 'bg-blue-100 border-l-4 border-blue-500';
      default: return 'border-l-4 border-gray-300';
    }
  };

  const renderCode = () => {
    return highlightedCode.map((line, index) => {
      const lineNumber = index + 1;
      const lineFindings = findings.filter(f => f.line === lineNumber);
      const hasFindings = lineFindings.length > 0;
      const severityClass = hasFindings ? getSeverityClass(lineFindings[0].severity) : '';

      return (
        <div key={index} className={`flex ${severityClass}`}>
          <div className="w-8 text-right pr-2 text-gray-500">
            {lineNumber}
          </div>
          <div className="flex-1 font-mono pl-2">
            {line}
          </div>
          {hasFindings && (
            <div className="text-red-500 pl-2">
              {lineFindings.map((finding, i) => (
                <div key={i} className="text-xs">
                  {finding.message}
                </div>
              ))}
            </div>
          )}
        </div>
      );
    });
  };

  return (
    <div className="border rounded font-mono text-sm">
      <pre className="p-4">
        {renderCode()}
      </pre>
    </div>
  );
}

export default CodeViewer;