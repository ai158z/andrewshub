import time
import logging
import threading
from typing import Dict, Any, Optional, List, Union
from collections import defaultdict, deque
from dataclasses import dataclass, field
from statistics import mean
from datetime import datetime, timedelta
import sys
import os

# Add the project root to the path to resolve imports
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Import internal modules
try:
    from src.qkd.protocol import QKDProtocol
    from src.qkd.key_distribution import KeyDistributor
    from src.qkd.quantum_channels import QuantumChannel
    from src.auth.edge_node_auth import EdgeNodeAuthenticator
    from src.auth.certificate_manager import CertificateManager
    from src.encoding.codonic_layer import CodonicEncoder
    from src.encoding.symbolic_encoder import SymbolicEncoder
    from src.fallback.classical_crypto import ClassicalCryptoFallback
    from src.fallback.backup_channels import BackupChannel
    from src.monitoring.latency_metrics import LatencyMetrics
    from src.core.crypto_utils import generate_random_bytes
    from src.core.key_storage import KeyStorage
    from src.api.key_management_api import KeyManagementAPI
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")
    # Create mock classes for testing purposes
    class QKDProtocol:
        def generate_keys(self):
            pass
    
    class KeyDistributor:
        def distribute_key(self, key):
            pass
    
    class QuantumChannel:
        def measure_fidelity(self):
            return 0.95
    
    class EdgeNodeAuthenticator:
        def authenticate_node(self, credentials):
            pass
    
    class CertificateManager:
        pass
    
    class CodonicEncoder:
        def encode_symbolic(self, data):
            return data
        def decode_symbolic(self, data):
            return data
    
    class SymbolicEncoder:
        def encode(self, data):
            return data
        def decode(self, data):
            return data
    
    class ClassicalCryptoFallback:
        pass
    
    class BackupChannel:
        pass
    
    class LatencyMetrics:
        def get_metrics_report(self):
            return {"timestamp": datetime.now().isoformat()}
    
    # Mock the utility functions
    class MockUtils:
        def generate_random_bytes(self, length):
            return b'a' * length
        def hash_key(self, key):
            return key
        def encrypt_data(self, data, key):
            return data
    
    generate_random_bytes = MockUtils().generate_random_bytes
    hash_key = MockUtils().hash_key
    encrypt_data = MockUtils().encrypt_data

@dataclass
class PerformanceMetrics:
    """Data class to hold performance metrics data"""
    operation_name: str
    start_time: float = 0.0
    end_time: float = 0.0
    duration: float = 0.0
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)

class PerformanceTracker:
    """Performance tracking for QKD operations and latency metrics"""
    
    def __init__(self):
        self.is_monitoring = False
        self.metrics_history = deque(maxlen=1000)  # Keep last 1000 metrics
        self.current_metrics = []
        self.lock = threading.Lock()
        self.monitoring_thread = None
        self.stop_event = threading.Event()
        self.latency_metrics = LatencyMetrics()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components we'll monitor
        self.qkd_protocol = QKDProtocol()
        self.key_distributor = KeyDistributor()
        self.quantum_channel = QuantumChannel()
        self.authenticator = EdgeNodeAuthenticator()
        self.cert_manager = CertificateManager()
        self.codonic_encoder = CodonicEncoder()
        self.symbolic_encoder = SymbolicEncoder()
        self.classical_fallback = ClassicalCryptoFallback()
        self.backup_channel = BackupChannel()
        self.key_storage = None
        try:
            self.key_storage = KeyStorage()
        except:
            pass
        self.api = None
        try:
            self.api = KeyManagementAPI()
        except:
            pass
        
    def start_monitoring(self) -> bool:
        """Start performance monitoring in a background thread"""
        if self.is_monitoring:
            self.logger.warning("Performance monitoring is already running")
            return False
            
        self.is_monitoring = True
        self.stop_event = threading.Event()
        self.monitoring_thread = threading.Thread(target=self._monitoring_worker, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("Performance monitoring started")
        return True
    
    def stop_monitoring(self) -> bool:
        """Stop performance monitoring"""
        if not self.is_monitoring:
            self.logger.warning("Performance monitoring is not running")
            return False
            
        self.is_monitoring = False
        self.stop_event.set()
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
            
        self.logger.info("Performance monitoring stopped")
        return True
    
    def _monitoring_worker(self) -> None:
        """Background worker for continuous monitoring"""
        while self.is_monitoring and not self.stop_event.is_set():
            try:
                self._collect_metrics()
                time.sleep(1)  # Sample every second
            except Exception as e:
                self.logger.error(f"Error in monitoring worker: {e}")
                break
    
    def _collect_metrics(self) -> None:
        """Collect performance metrics from all components"""
        timestamp = time.time()
        
        # Measure QKD protocol performance
        self._measure_qkd_operations()
        
        # Measure key distribution performance
        self._measure_key_distribution()
        
        # Measure quantum channel performance
        self._measure_quantum_channel()
        
        # Measure authentication performance
        self._measure_authentication()
        
        # Measure encoding performance
        self._measure_encoding_operations()
    
    def _measure_qkd_operations(self) -> None:
        """Measure QKD operations performance"""
        start_time = time.time()
        try:
            # Measure key generation performance
            self.qkd_protocol.generate_keys()
            end_time = time.time()
            self._record_metric("qkd_key_generation", start_time, end_time, True)
        except Exception as e:
            end_time = time.time()
            self._record_metric("qkd_key_generation", start_time, end_time, False, {"error": str(e)})
    
    def _measure_key_distribution(self) -> None:
        """Measure key distribution performance"""
        start_time = time.time()
        try:
            # Measure key distribution performance
            test_key = generate_random_bytes(32)
            self.key_distributor.distribute_key(test_key)
            end_time = time.time()
            self._record_metric("key_distribution", start_time, end_time, True)
        except Exception as e:
            end_time = time.time()
            self._record_metric("key_distribution", start_time, end_time, False, {"error": str(e)})
    
    def _measure_quantum_channel(self) -> None:
        """Measure quantum channel performance"""
        start_time = time.time()
        try:
            # Measure channel fidelity
            fidelity = self.quantum_channel.measure_fidelity()
            end_time = time.time()
            self._record_metric("quantum_channel_fidence", start_time, end_time, True, {"fidelity": fidelity})
        except Exception as e:
            end_time = time.time()
            self._record_metric("quantum_channel_fidelity", start_time, end_time, False, {"error": str(e)})
    
    def _measure_authentication(self) -> None:
        """Measure authentication performance"""
        start_time = time.time()
        try:
            # Test authentication with dummy credentials
            dummy_credentials = {"node_id": "test_node", "token": "dummy_token"}
            self.authenticator.authenticate_node(dummy_credentials)
            end_time = time.time()
            self._record_metric("node_authentication", start_time, end_time, True)
        except Exception as e:
            end_time = time.time()
            self._record_metric("node_authentication", start_time, end_time, False, {"error": str(e)})
    
    def _measure_encoding_operations(self) -> None:
        """Measure encoding operations performance"""
        # Test codonic encoding
        start_time = time.time()
        try:
            test_data = "test_data_for_encoding"
            encoded = self.codonic_encoder.encode_symbolic(test_data)
            self.codonic_encoder.decode_symbolic(encoded)
            end_time = time.time()
            self._record_metric("codonic_encoding", start_time, end_time, True)
        except Exception as e:
            end_time = time.time()
            self._record_metric("codonic_encoding", start_time, end_time, False, {"error": str(e)})
            
        # Test symbolic encoding
        start_time = time.time()
        try:
            test_symbol = "symbolic_test"
            encoded = self.symbolic_encoder.encode(test_symbol)
            self.symbolic_encoder.decode(encoded)
            end_time = time.time()
            self._record_metric("symbolic_encoding", start_time, end_time, True)
        except Exception as e:
            end_time = time.time()
            self._record_metric("symbolic_encoding", start_time, end_time, False, {"error": str(e)})
    
    def _record_metric(self, operation: str, start_time: float, end_time: float, success: bool, details: Dict[str, Any] = None) -> None:
        """Record a performance metric"""
        metric = PerformanceMetrics(
            operation_name=operation,
            start_time=start_time,
            end_time=end_time,
            duration=end_time - start_time,
            success=success,
            details=details or {}
        )
        
        with self.lock:
            self.current_metrics.append(metric)
            self.metrics_history.append({
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "duration_ms": metric.duration * 1000,
                "success": success,
                "details": details
            })
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a performance report"""
        with self.lock:
            if not self.metrics_history:
                return {"status": "No metrics collected"}
            
            # Group metrics by operation
            operation_metrics = defaultdict(list)
            for metric in self.metrics_history:
                if "operation" in metric:
                    operation_metrics[metric["operation"]].append(metric)
            
            # Calculate statistics
            report = {
                "timestamp": datetime.now().isoformat(),
                "total_operations": len(self.metrics_history),
                "operations_summary": {}
            }
            
            for operation, metrics in operation_metrics.items():
                successful_metrics = [m for m in metrics if m.get("success", False)]
                failed_metrics = [m for m in metrics if not m.get("success", False)]
                
                report["operations_summary"][operation] = {
                    "total_count": len(metrics),
                    "success_count": len(successful_metrics),
                    "failure_count": len(failed_metrics),
                    "avg_duration_ms": mean([m["duration_ms"] for m in successful_metrics]) if successful_metrics else 0,
                    "recent_metrics": metrics[-10:]  # Last 10 metrics
                }
            
            return report
    
    def get_latency_report(self) -> Dict[str, Any]:
        """Get latency metrics report"""
        return self.latency_metrics.get_metrics_report()
    
    def get_current_metrics(self) -> list:
        """Get current performance metrics"""
        with self.lock:
            return list(self.current_metrics)
    
    def reset_metrics(self) -> None:
        """Reset collected metrics"""
        with self.lock:
            self.current_metrics.clear()
            self.metrics_history.clear()
    
    def measure_operation(self, operation_name: str, operation_func, *args, **kwargs) -> Any:
        """Context manager-like method to measure an operation"""
        start_time = time.time()
        success = True
        result = None
        error = None
        
        try:
            result = operation_func(*args, **kwargs)
        except Exception as e:
            success = False
            error = str(e)
        finally:
            end_time = time.time()
            self._record_metric(operation_name, start_time, end_time, success, {"error": error} if error else {})
            return result

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)