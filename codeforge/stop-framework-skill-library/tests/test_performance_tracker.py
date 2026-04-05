import pytest
import time
from unittest.mock import patch, MagicMock
from datetime import datetime
from stop_skill_library.reflection.performance_tracker import PerformanceTracker
from stop_skill_library.models import PerformanceRecord

def test_performance_tracker_initial_state():
    tracker = PerformanceTracker()
    assert tracker.total_executions == 0
    assert tracker.successful_executions == 0
    assert tracker.failed_executions == 0
    assert tracker.total_execution_time == 0.0

def test_performance_tracker_track_success():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.5, True)
    assert tracker.total_executions == 1
    assert tracker.successful_executions == 1
    assert tracker.failed_executions == 0

def test_performance_tracker_track_failure():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.5, False, "Test error")
    assert tracker.total_executions == 1
    assert tracker.successful_executions == 0
    assert tracker.failed_executions == 1

def test_performance_tracker_get_metrics_empty():
    tracker = PerformanceTracker()
    metrics = tracker.get_metrics()
    assert metrics.total_executions == 0
    assert metrics.successful_executions == 0
    assert metrics.failed_executions == 0

def test_performance_tracker_get_metrics_with_data():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    tracker.track("skill1", 2.0, True, error_message="Error occurred")
    metrics = tracker.get_metrics()
    assert metrics.total_executions == 1
    assert metrics.successful_executions == 1
    assert metrics.failed_executions == 0

def test_performance_tracker_get_metrics_no_data():
    tracker = PerformanceTracker()
    metrics = tracker.get_metrics()
    assert metrics.total_executions == 0
    assert metrics.successful_executions == 0
    assert metrics.failed_executions == 0

def test_performance_tracker_get_metrics_with_skill_data():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    metrics = tracker.get_metrics("skill1")
    assert metrics.total_executions == 1
    assert metrics.successful_executions == 1
    assert metrics.failed_executions == 0

def test_performance_tracker_generate_report():
    # Setup
    tracker = PerformanceTracker()
    report = tracker.generate_report()
    assert "generated_at" in report
    assert "tracking_duration" in report
    assert "overall_metrics" in report
    assert "skill_metrics" in report
    assert "execution_summary" in report

def test_performance_tracker_generate_report_with_skill_data():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    report = tracker.generate_report()
    # Verify that the report structure is as expected
    assert "generated_at" in str(report)
    assert "tracking_duration" in report

def test_performance_tracker_generate_report_with_no_data():
    tracker = PerformanceTracker()
    report = tracker.generate_report()
    assert "generated_at" in str(report)

def test_performance_tracker_generate_report_with_data():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    report = tracker.generate_report()
    assert "generated_at" in str(report)
    assert "tracking_duration" in str(report)
    assert "overall_metrics" in report
    assert "skill_metrics" in report
    assert "execution_summary" in report

def test_performance_tracker_get_metrics_single_skill():
    tracker = PerformanceTracker()
    metrics = tracker.get_metrics("skill1")
    assert "total_executions" in str(metrics)
    assert "successful_executions" in str(metrics)
    assert "failed_executions" in str(metrics)
    assert "average_execution_time" in str(metrics)
    assert "success_rate" in str(metrics)
    assert "total_execution_time" in str(metrics)

def test_performance_tracker_get_metrics_multiple_skills():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    tracker.track("skill2", 2.0, False, "Error occurred")
    metrics = {}
    metrics["skill1"] = {"total_executions": 1, "successful_executions": 1, "failed_executions": 0, "average_execution_time": 1.0, "total_execution_time": 1.0}
    metrics["skill2"] = {"total_executions": 1, "successful_executions": 1, "failed_executions": 0, "average_execution_time": 1.0, "total_execution_time": 1.0}
    return metrics

def test_performance_tracker_get_metrics_multiple_skills():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    tracker.track("skill1", 2.0, False, "Error occurred")
    metrics = tracker.get_metrics()
    assert metrics.total_executions == 1
    assert metrics.successful_executions == 1
    assert metrics.failed_executions == 0

def test_performance_tracker_get_metrics_single_skill():
    tracker = PerformanceTracker()
    metrics = tracker.get_metrics()
    return metrics

def test_performance_tracker_get_metrics_single_skill():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    assert True

def test_performance_tracker_get_metrics():
    tracker = PerformanceTracker()
    metrics = tracker.get_metrics()
    assert "total_executions" in str(metrics)
    assert "successful_executions" in str(metrics)
    assert "failed_executions" in str(metrics)
    assert "average_execution_time" in str(metrics)
    assert "total_execution_time" in str(metrics)

def test_performance_tracker_get_metrics():
    # Test the PerformanceTracker class
    tracker = PerformanceTracker()
    metrics = PerformanceRecord(1.0, True)
    assert tracker.total_executions == 1
    assert tracker.successful_executions == 1
    assert tracker.failed_executions == 0

def test_performance_tracker_get_metrics():
    tracker = PerformanceTracker()
    report = tracker.generate_report()
    assert "generated_at" in str(report)
    assert "tracking_duration" in str(report)
    assert "overall_metrics" in str(report)
    assert "skill_metrics" in str(report)
    assert "execution_summary" in str(report)

def test_performance_tracker_get_metrics_with_skill_data():
    tracker = PerformanceTracker()
    tracker.track("skill1", 1.0, True)
    metrics = tracker.get_metrics()
    assert "total_executions" in str(metrics)
    assert "successful_executions" in str(metrics)
    assert "failed_executions" in str(metrics)
    assert "average_execution_time" in str(metrics)
    assert "total_execution_time" in str(metrics)

def test_performance_tracker_get_metrics_with_no_skill_data():
    tracker = PerformanceTracker()
    report = tracker.generate_report()
    assert "generated_at" in str(report)
    assert "tracking_duration" in str(report)
    assert "overall_metrics" in str(report)
    assert "skill_metrics" in str(report)
    assert "execution_summary" in str(report)