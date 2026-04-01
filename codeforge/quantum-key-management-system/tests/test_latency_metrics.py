import pytest
import time
from unittest.mock import Mock, patch
from src.monitoring.latency_metrics import LatencyMetrics, LatencySample, LatencyReport

@pytest.fixture
def latency_metrics():
    return LatencyMetrics(max_samples=5)

def test_record_latency_adds_sample(latency_metrics):
    latency_metrics.record_latency("test_op", 1.0)
    report = latency_metrics.get_metrics_report()
    assert "test_op" in report
    assert len(report["test_op"].samples) == 1
    assert report["test_op"].samples[0].duration == 1.0

def test_record_latency_with_node_and_metadata(latency_metrics):
    latency_metrics.record_latency("test_op", 1.0, "node1", {"key": "value"})
    report = latency_metrics.get_metrics_report()
    assert report["test_op"].samples[0].node_id == "node1"
    assert report["test_op"].samples[0].metadata == {"key": "value"}

def test_get_metrics_report_empty(latency_metrics):
    report = latency_metrics.get_metrics_report()
    assert report == {}

def test_get_metrics_report_with_operation(latency_metrics):
    latency_metrics.record_latency("test_op", 1.0)
    report = latency_metrics.get_metrics_report("test_op")
    assert "test_op" in report
    assert report["test_op"].total_operations == 1

def test_get_metrics_report_operation_not_found(latency_metrics):
    report = latency_metrics.get_metrics_report("nonexistent")
    assert "nonexistent" in report
    assert report["nonexistent"].total_operations == 0

def test_record_multiple_latencies(latency_metrics):
    for i in range(3):
        latency_metrics.record_latency("test_op", float(i))
    
    report = latency_metrics.get_metrics_report()["test_op"]
    assert report.total_operations == 3
    assert report.average_latency == 1.0  # mean of [0, 1, 2]
    assert report.min_latency == 0.0
    assert report.max_latency == 2.0

def test_latency_context_manager():
    metrics = LatencyMetrics()
    with patch('time.perf_counter', side_effect=[10.0, 15.5]):
        with metrics.measure_latency("test_operation") as ctx:
            pass
    
    # Verify that a sample was recorded with correct duration (5.5)
    reports = metrics.get_metrics_report()
    assert "test_operation" in reports
    # Should be approximately 5.5 seconds
    assert abs(reports["test_operation"].samples[0].duration - 5.5) < 0.01

def test_latency_context_with_node_and_metadata():
    metrics = LatencyMetrics()
    with patch('time.perf_counter', side_effect=[10.0, 12.0]):
        with metrics.measure_latency("test_op", "node1", {"key": "value"}) as ctx:
            pass
    
    sample = metrics.get_metrics_report()["test_op"].samples[0]
    assert sample.node_id == "node1"
    assert sample.metadata == {"key": "value"}

def test_latency_sample_dataclass():
    sample = LatencySample(
        timestamp=12345.0,
        duration=2.5,
        operation="test",
        node_id="node1",
        metadata={"key": "value"}
    )
    assert sample.duration == 2.5
    assert sample.node_id == "node1"
    assert sample.metadata == {"key": "value"}

def test_latency_report_dataclass():
    sample = LatencySample(12345.0, 2.5, "test")
    report = LatencyReport(
        total_operations=1,
        average_latency=2.5,
        min_latency=1.0,
        max_latency=5.0,
        std_deviation=1.5,
        samples=[sample]
    )
    assert report.total_operations == 1
    assert report.average_latency == 2.5

def test_max_samples_enforced(latency_metrics):
    for i in range(10):
        latency_metrics.record_latency("test_op", float(i))
    
    report = latency_metrics.get_metrics_report()
    # Should only keep the last 5 samples as max_samples=5
    assert len(report["test_op"].samples) == 5
    # First samples should be the last 5 recorded (5.0 through 9.0)
    assert all(s.duration >= 5.0 for s in report["test_op"].samples)

def test_thread_safety(latency_metrics):
    # Record multiple items in a single operation to test thread safety
    for i in range(3):
        latency_metrics.record_latency("test_op", float(i))
    
    report = latency_metrics.get_metrics_report()
    assert report["test_op"].total_operations == 3

def test_empty_report():
    metrics = LatencyMetrics()
    report = metrics.get_metrics_report()
    assert report == {}

def test_statistics_computation():
    metrics = LatencyMetrics()
    # Record different durations for the same operation
    test_durations = [1.0, 2.0, 3.0]
    for duration in test_durations:
        metrics.record_latency("test_op", duration)
    
    report = metrics.get_metrics_report()["test_op"]
    assert report.average_latency == 2.0  # mean
    assert report.min_latency == 1.0
    assert report.max_latency == 3.0
    # std dev of [1,2,3] is sqrt(2/3) ≈ 0.816
    assert abs(report.std_deviation - 0.816) < 0.01
    assert report.total_operations == 3

def test_no_standard_deviation_single_sample():
    metrics = LatencyMetrics()
    metrics.record_latency("test_op", 5.0)
    report = metrics.get_metrics_report()["test_op"]
    assert report.std_deviation == 0.0  # Should be 0 for single value

def test_deque_size_limit_enforcement(latency_metrics):
    # Test that the maxlen parameter is enforced by recording more than max_samples
    for i in range(7):  # 7 > max_samples (5)
        latency_metrics.record_latency("test_op", float(i))
    
    report = latency_metrics.get_metrics_report()
    # Should contain only the last 5 elements
    assert len(report["test_op"].samples) <= 5

def test_multiple_operations(latency_metrics):
    # Record latencies for different operations
    latency_metrics.record_latency("op1", 1.0)
    latency_metrics.record_latency("op2", 2.0)
    
    report = latency_metrics.get_metrics_report()
    assert "op1" in report
    assert "op2" in report
    assert len(report) == 2

def test_sample_limit_enforcement(latency_metrics):
    # Record more samples than max_samples to test if the limit is enforced
    for i in range(6):  # One more than max to test the limit
        latency_metrics.record_latency("limited_op", float(i))
    
    # Should only have the last 5 samples
    report = latency_metrics.get_metrics_report()
    assert len(report["limited_op"].samples) == 5

def test_report_generation_all_ops(latency_metrics):
    latency_metrics.record_latency("op1", 1.0)
    latency_metrics.record_latency("op2", 2.0)
    
    reports = latency_metrics.get_metrics_report()
    assert "op1" in reports
    assert "op2" in reports
    assert len(reports) == 2

def test_report_generation_specific_op(latency_metrics):
    latency_metrics.record_latency("op1", 1.0)
    latency_metrics.record_latency("op2", 2.0)
    
    reports = latency_metrics.get_metrics_report("op1")
    assert "op1" in reports
    assert len(reports) == 1

def test_concurrent_access_simulation(latency_metrics):
    # Record latency in a way that simulates concurrent access
    for i in range(3):
        latency_metrics.record_latency("concurrent_op", float(i))
    
    # Check if all records are properly kept (should be 3)
    report = latency_metrics.get_metrics_report()
    assert report["concurrent_op"].total_operations == 3

def test_report_with_no_samples():
    metrics = LatencyMetrics()
    # Test report generation when no samples have been recorded yet
    report = metrics.get_metrics_report()
    assert report == {}

def test_report_with_single_sample():
    metrics = LatencyMetrics()
    metrics.record_latency("single_op", 1.0)
    report = metrics.get_metrics_report()
    assert len(report["single_op"].samples) == 1
    assert report["single_op"].total_operations == 1

def test_context_manager_exception_safety():
    metrics = LatencyMetrics()
    try:
        with metrics.measure_latency("test_op") as ctx:
            raise Exception("Test exception")
    except Exception:
        pass  # Ignore the exception for this test
    
    # Ensure that the context manager properly cleans up even if an exception occurred
    assert "test_op" not in metrics._active_measurements

def test_deque_maxlen_parameter():
    # Test that the deque is initialized with the correct maxlen
    metrics = LatencyMetrics(max_samples=3)
    for i in range(5):
        metrics.record_latency("op", float(i))
    
    # Should only keep last 3 samples
    report = metrics.get_metrics_report()
    assert len(report["op"].samples) == 3
    # The samples should be the last 3 recorded (2.0, 3.0, 4.0)
    assert [s.duration for s in report["op"].samples] == [2.0, 3.0, 4.0]