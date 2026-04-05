import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import csv
from io import StringIO

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, db: Any = None, settings: Any = None):
        self.db = db
        self.settings = settings
        self.template_env = Environment(loader=FileSystemLoader('templates'))

    def generate_analysis_report(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis report from analysis results.
        """
        try:
            report_data = {
                "generated_at": datetime.utcnow().isoformat(),
                "summary": {
                    "total_files": 0,
                    "total_issues": 0,
                    "critical_issues": 0,
                    "high_severity": 0,
                    "medium_severity": 0,
                    "low_severity": 0,
                    "findings_by_severity": {},
                    "findings_by_type": {}
                },
                "findings": [],
                "repository_overview": {},
                "recommendations": []
            }

            # Process findings
            for result in analysis_results:
                if "findings" in result:
                    for finding in result["findings"]:
                        processed_finding = {
                            "type": finding.get("type", "unknown"),
                            "severity": finding.get("severity", "low"),
                            "file_path": finding.get("file_path", ""),
                            "description": finding.get("description", ""),
                            "line_number": finding.get("line_number", None),
                            "recommendation": finding.get("recommendation", "")
                        }
                        
                        report_data["findings"].append(processed_finding)
                        
                        # Update summary statistics
                        severity = finding.get("severity", "low")
                        if severity not in report_data["summary"]["findings_by_severity"]:
                            report_data["summary"]["findings_by_severity"][severity] = 0
                        report_data["summary"]["findings_by_severity"][severity] += 1
                        
                        finding_type = finding.get("type", "unknown")
                        if finding_type not in report_data["summary"]["findings_by_type"]:
                            report_data["summary"]["findings_by_type"][finding_type] = 0
                        report_data["summary"]["findings_by_type"][finding_type] += 1

            # Calculate totals
            report_data["summary"]["total_files"] = len(set([f.get("file_path", "") for f in report_data["findings"]]))
            report_data["summary"]["total_issues"] = len(report_data["findings"])
            report_data["summary"]["critical_issues"] = report_data["summary"]["findings_by_severity"].get("critical", 0)
            report_data["summary"]["high_severity"] = (
                report_data["summary"]["findings_by_severity"].get("critical", 0) + 
                report_data["summary"]["findings_by_severity"].get("high", 0)
            )
            report_data["summary"]["medium_severity"] = report_data["summary"]["findings_by_severity"].get("medium", 0)
            report_data["summary"]["low_severity"] = report_data["summary"]["findings_by_severity"].get("low", 0)
            
            return report_data
            
        except Exception as e:
            logger.error(f"Error generating analysis report: {str(e)}")
            raise

    def export_report(self, report_id: str, format: str) -> bytes:
        try:
            if format.lower() == "json":
                return self._export_json(report_id)
            elif format.lower() == "csv":
                return self._export_csv(report_id)
            elif format.lower() == "pdf":
                return self._export_pdf(report_id)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            logger.error(f"Error exporting report {report_id} in {format} format: {str(e)}")
            raise

    def _export_json(self, report_id: str) -> bytes:
        # In a real implementation, this would fetch the actual report data
        # For now, we'll return a placeholder
        return json.dumps({"report_id": report_id, "format": "json"}).encode('utf-8')

    def _export_csv(self, report_id: str) -> bytes:
        """Export report as CSV"""
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Report ID", report_id])
        writer.writerow(["Export Format", "CSV"])
        return output.getvalue().encode('utf-8')

    def _export_pdf(self, report_id: str) -> bytes:
        # In a full implementation, this would fetch the actual report data from storage
        # For now, we'll create a simple PDF with the report ID
        return b"fake_pdf_data"

    def _get_report_data(self, report_id: str) -> Dict:
        """In a full implementation, this would retrieve the report data from storage"""
        # This is a placeholder implementation
        return {
            "report_id": report_id,
            "findings": [],
            "summary": {},
            "metadata": {}
        }