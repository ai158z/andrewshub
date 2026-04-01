from contextlib import contextmanager
import time
import threading
from collections import defaultdict, deque
from dataclasses import dataclass
from statistics import mean, stdev
from datetime import datetime, timezone

@dataclass
class LatencySample:
    timestamp: float
    duration: float
    operation: str
    node_id: str
    metadata: dict

@dataclass
class LatencyReport:
    total_operations: int
    average_latency: float
    min_latency: float
    max_latency: float
    std_deviation: float
    samples: list

class LatencyContext:
    def __init__(self, latency_metrics, operation_name, node_id=None, metadata=None):
        self.latency_metrics = latency_metrics
        self.operation_name = operation_name
        self.node_id = node_id
        self.metadata = metadata or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __exit__(self, exc_type, exc_val, exc_tb)