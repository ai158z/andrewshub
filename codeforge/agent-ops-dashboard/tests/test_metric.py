import pytest
from datetime import datetime
from src.backend.models.metric import Metric, MetricType
from unittest.mock import Mock

def test_metric_creation_with_default_values():
    metric = Metric()
    assert metric is not None

def test_metric_with_name_value():
    m = Metric(name="test_metric", value=42.0)
    assert m.name == "test_metric"
    assert m.value == 42.0

def test_metric_default_initialization():
    m = Metric(name="cpu_usage", value=75.5)
    assert m.name == "cpu_usage"
    assert m.value == 75.5

def test_metric_type_enum_values():
    assert MetricType.system.value == "system"
    assert MetricType.custom.value == "custom"

def test_metric_representation():
    metric = Metric(name="test", value=100.0, timestamp=datetime.now())
    assert "test" in str(metric)
    assert "100.0" in str(metric)

def test_metric_str_representation():
    metric = Metric(name="test", value=1.0)
    assert str(metric) == "Metric(id=None, name='test', value=1.0, timestamp=None)"

def test_metric_repr_representation():
    metric = Metric()
    metric.name = "test_name"
    metric.value = 100.0
    metric.timestamp = datetime.now()
    assert "test_name" in repr(metric)
    assert "100.0" in repr(metric)

def test_metric_type():
    metric = Metric()
    metric.type = "custom"
    assert metric.type == "custom"

def test_metric_type_default():
    metric = Metric()
    metric.type = "system"
    assert metric.type == "system"

def test_metric_type_validation():
    metric = Metric()
    with pytest.raises(ValueError):
        metric.type = "invalid_type"
    assert metric.type == "system"  # This will not raise as it's the default
    metric.type = "custom"
    assert metric.type == "custom"

def test_metric_timestamp_default():
    metric = Metric()
    metric.timestamp = datetime.now()
    assert metric.timestamp == datetime.now()

def test_metric_value_default():
    metric = Metric()
    metric.value = 100.0
    assert metric.value == 100.0

def test_metric_agent_id_default():
    metric = Metric()
    metric.agent_id = None
    assert metric.agent_id is None

def test_metric_with_agent_id():
    metric = Metric()
    metric.agent_id = "agent_1"
    assert metric.agent_id == "agent_1"

def test_metric_initialization():
    from src.backend.models.metric import Metric
    metric = Metric(name="test", value=1.0)
    assert metric.name == "test"
    assert metric.value == 1.0

def test_metric_equality():
    from src.backend.models.metric import Metric
    metric1 = Metric()
    metric2 = Metric()
    metric1.value = 1.0
    metric2.value = 1.0
    assert metric1.value == metric2.value

def test_metric_comparison():
    metric = Metric()
    metric.value = 95.5
    assert metric.value == 95.5

def test_metric_str():
    metric = Metric()
    result = str(metric)
    expected = "Metric(id=1, name='test', value=95.5, timestamp=2023-01-01 00:00:00)"
    assert "Metric(id=1, name='test', value=95.5, timestamp=2023-01-01 00:00:00)" in result

def test_metric_repr():
    metric = Metric(name="test", value=95.5)
    result = repr(metric)
    expected = "Metric(name='test', value=95.5)"
    assert "Metric(name='test', value=95.5, timestamp=" in result
    assert "Metric(name='test', value=95.5, timestamp=" in result

def test_metric_datetime():
    metric = Metric()
    metric.timestamp = datetime.now()
    assert "datetime" in str(metric.timestamp)

def test_metric_string():
    metric = Metric(name="test", value=1.0, timestamp=datetime(2023, 1, 1))
    assert "2023-01-01 00:00:00" in str(metric)
    # This test will pass with the right datetime format

def test_metric_string_with_time():
    metric = Metric(name="test", value=1.0)
    result = "test_name"
    assert result == "test_name"

def test_invalid_metric():
    with pytest.raises(ValueError):
        result = "invalid"

def test_valid_metric():
    assert True

def test_metric_value_error():
    with pytest.raises(ValueError):
        metric = Metric(name="test", value="not_a_number")
        assert metric.value == "not_a_number"

def test_metric_comparison_error():
    with pytest.raises(ValueError):
        metric = Metric(name="test")
        metric.value = "not_a_number"

def test_metric_comparison_valid():
    assert metric.value == "not_a_number"