import pytest
from unittest.mock import Mock, patch, mock_open
from src.services.report_generator import ReportGenerator
from datetime import datetime
import json
import pandas as pd

def test_generate_analysis_report_success():
    analysis_results = [
        {
            "findings": [
                {
                    "type": "security",
                    "severity": "critical",
                    "file_path": "/path/to/file1",
                    "description": "Test critical issue",
                    "line_number": 42,
                    "recommendation": "Fix the issue"
                },
                {
                    "type": "security",
                    "severity": "high",
                    "file_path": "/path/to/file2",
                    "description": "Test high issue",
                    "line_number": 100,
                    "recommendation": "Review the code"
                }
            ]
        }
    ]
    
    report_gen = ReportGenerator(db=None, settings=None)
    result = report_gen.generate_analysis_report(analysis_results)
    
    assert "generated_at" in result
    assert result["summary"]["total_files"] == 2
    assert result["summary"]["total_issues"] == 2
    assert result["summary"]["critical_issues"] == 1
    assert result["summary"]["high_severity"] == 1
    assert result["summary"]["medium_severity"] == 0
    assert result["summary"]["low_severity"] == 0
    assert result["summary"]["findings_by_severity"] == {"critical": 1, "high": 1}
    assert result["summary"]["findings_by_type"] == {"security": 2}
    assert len(result["findings"]) == 2
    assert result["findings"][0]["type"] == "security"
    assert result["findings"][0]["severity"] == "critical"
    assert result["findings"][0]["file_path"] == "/path/to/file1"
    assert result["findings"][0]["description"] == "Test critical issue"
    assert result["findings"][0]["line_number"] == 42
    assert result["findings"][0]["recommendation"] == "Fix the issue"

def test_generate_analysis_report_empty_results():
    report_gen = ReportGenerator(db=None, settings=None)
    result = report_gen.generate_analysis_report([])
    
    assert result["findings"] == []
    assert result["summary"]["total_files"] == 0
    assert result["summary"]["total_issues"] == 0
    assert result["summary"]["critical_issues"] == 0
    assert result["summary"]["high_severity"] == 0
    assert result["summary"]["medium_severity"] == 0
    assert result["summary"]["low_severity"] == 0
    assert result["summary"]["findings_by_severity"] == {}
    assert result["summary"]["findings_by_type"] == {}

def test_generate_analysis_report_no_findings_key():
    analysis_results = [
        {
            "repository": "test-repo",
            "commit": "abc123"
        }
    ]
    
    report_gen = ReportGenerator(db=None, settings=None)
    result = report_gen.generate_analysis_report(analysis_results)
    
    assert result["findings"] == []
    assert result["summary"]["total_issues"] == 0

def test_export_report_json_format():
    report_gen = ReportGenerator(db=None, settings=None)
    result = report_gen.export_report("test_report_id", "json")
    expected = json.dumps({"report_id": "test_report_id", "format": "json"}).encode('utf-8')
    assert result == expected

def test_export_report_csv_format():
    report_gen = ReportGenerator(db=None, settings=None)
    result = report_gen._export_csv("test_report")
    assert isinstance(result, bytes)

def test_export_report_pdf_format():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with patch('src.services.report_generator.pdfkit') as mock_pdfkit:
        mock_pdfkit.from_string.return_value = b"fake_pdf_data"
        result = report_gen._export_pdf("test_report")
        assert isinstance(result, bytes)

def test_export_report_unsupported_format():
    report_gen = ReportGenerator(db=None, settings=None)
    with pytest.raises(ValueError):
        report_gen.export_report("test_report", "xml")

def test_export_report_formats():
    report_gen = ReportGenerator(db=None, settings=None)
    
    json_result = report_gen._export_json("test_report")
    assert b'test_report' in json_result
    
    csv_result = report_gen._export_csv("test_report")
    assert b'Export Format' in csv_result

def test_export_report_pdf_fallback():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with patch('src.services.report_generator.pdfkit') as mock_pdfkit:
        mock_pdfkit.from_string.side_effect = Exception("PDF generation failed")
        result = report_gen._export_pdf("test_report")
        assert b'<h1>Analysis Report</h1>' in result
        assert b'test_report' in result

def test_generate_analysis_report_missing_fields():
    analysis_results = [
        {
            "findings": [
                {
                    "type": "security"
                }
            ]
        }
    ]
    
    report_gen = ReportGenerator(db=None, settings=None)
    result = report_gen.generate_analysis_report(analysis_results)
    
    assert result["findings"][0]["severity"] == "low"
    assert result["findings"][0]["file_path"] == ""
    assert result["findings"][0]["description"] == ""
    assert result["findings"][0]["recommendation"] == ""

def test_generate_analysis_report_exception():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with patch.object(report_gen, '_get_report_data', side_effect=Exception("Database error")):
        try:
            report_gen._get_report_data("test_id")
            assert False, "Expected exception not raised"
        except Exception:
            pass

def test_export_report_json_exception():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with patch.object(report_gen, '_export_json', side_effect=Exception("Export error")):
        with pytest.raises(Exception):
            report_gen._export_json("test_id")

def test_export_report_csv_exception():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with patch.object(report_gen, '_export_csv', side_effect=Exception("Export error")):
        with pytest.raises(Exception):
            report_gen._export_csv("test_id")

def test_export_report_pdf_exception():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with patch('src.services.report_generator.pdfkit') as mock_pdfkit:
        mock_pdfkit.from_string.side_effect = Exception("PDF error")
        result = report_gen._export_pdf("test_id")
        assert b'<h1>Analysis Report</h1>' in result
        assert b'<p>Report ID: test_id</p>' in result

def test_export_report_unsupported_format_exception():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with pytest.raises(ValueError):
        report_gen.export_report("test_id", "xml")

def test_export_report_missing_format():
    report_gen = ReportGenerator(db=None, settings=None)
    
    with pytest.raises(ValueError) as exc_info:
        report_gen.export_report("test_id", "xml")
    assert "Unsupported format" in str(exc_info.value)