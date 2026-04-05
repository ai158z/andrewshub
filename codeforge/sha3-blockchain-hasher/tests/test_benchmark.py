import pytest
from unittest.mock import patch, MagicMock
from sha3_hasher.benchmark import benchmark_hashing_speed
from sha3_hasher.core import sha3_512_hash
import logging

def test_benchmark_hashing_speed_with_string_data():
    data = "test data"
    result = benchmark_hashing_speed(data, "test_label")
    assert result["label"] == "test_label"
    assert result["data_size"] == len(data.encode('utf-8'))
    assert "core_time" in result
    assert "utils_time" in result
    assert "hash_result" in result

def test_benchmark_hashing_speed_with_bytes_data():
    data = b"test data"
    result = benchmark_hashing_speed(data, "test_bytes")
    assert result["label"] == "test_bytes"
    assert result["data_size"] == len(data)
    assert result["core_time"] >= 0
    assert result["utils_time"] >= 0

def test_benchmark_hashing_speed_empty_data_raises_error():
    with pytest.raises(ValueError, match="Data cannot be empty for benchmarking"):
        benchmark_hashing_speed("")

def test_benchmark_hashing_speed_invalid_data_type_raises_error():
    with pytest.raises(TypeError, match="Data must be bytes or string"):
        benchmark_hashing_speed(123)

def test_benchmark_hashing_speed_invalid_label_type_raises_error():
    with pytest.raises(TypeError, match="Label must be a string"):
        benchmark_hashing_speed("test", 123)

def test_benchmark_hashing_speed_logs_output(caplog):
    with caplog.at_level("INFO"):
        data = b"benchmark test"
        benchmark_hashing_speed(data, "logging_test")
    assert "Benchmark logging_test:" in caplog.text

def test_benchmark_hashing_speed_consistency_between_implementations():
    data = b"consistent test data"
    result = benchmark_hashing_speed(data)
    core_hash = sha3_512_hash(data)
    assert result["hash_result"] == core_hash.hex()

def test_benchmark_hashing_speed_throughput_computation():
    data = b"benchmark throughput test"
    result = benchmark_hashing_speed(data)
    assert result["throughput"] is not None
    assert result["throughput"] > 0

def test_benchmark_hashing_speed_zero_data_size():
    with pytest.raises(ValueError, match="Data cannot be empty for benchmarking"):
        benchmark_hashing_speed(b"")

def test_benchmark_hashing_speed_large_data():
    data = b"A" * 10000
    result = benchmark_hashing_speed(data, "large_data_test")
    assert result["data_size"] == 10000
    assert result["core_time"] >= 0
    assert result["utils_time"] >= 0

def test_benchmark_hashing_speed_unicode_string():
    data = "🚀🌟 Unicode data test"
    result = benchmark_hashing_speed(data)
    assert result["data_size"] == len(data.encode('utf-8'))

def test_benchmark_hashing_speed_special_characters():
    data = "!@#$%^&*()_+{}|[]\\:"
    result = benchmark_hashing_speed(data)
    assert result["data_size"] == len(data.encode('utf-8'))

def test_benchmark_hashing_speed_consistent_hash_output():
    data = b"consistent output test"
    result1 = benchmark_hashing_speed(data)
    result2 = benchmark_hashing_speed(data)
    assert result1["hash_result"] == result2["hash_result"]

def test_benchmark_hashing_speed_label_none():
    data = b"test"
    result = benchmark_hashing_speed(data, None)
    assert result["label"] is None

def test_benchmark_hashing_speed_label_empty_string():
    data = b"empty label test"
    result = benchmark_hashing_speed(data, "")
    assert result["label"] == ""

def test_benchmark_hashing_speed_label_normal():
    data = b"normal label test"
    result = benchmark_hashing_speed(data, "normal")
    assert result["label"] == "normal"

def test_benchmark_hashing_speed_data_as_none():
    with pytest.raises(TypeError):
        benchmark_hashing_speed(None)

def test_benchmark_hashing_speed_data_as_int():
    with pytest.raises(TypeError):
        benchmark_hashing_speed(42)

def test_benchmark_hashing_speed_data_as_list():
    with pytest.raises(TypeError):
        benchmark_hashing_speed([1, 2, 3])

def test_benchmark_hashing_speed_data_as_dict():
    with pytest.raises(TypeError):
        benchmark_hashing_speed({"key": "value"})