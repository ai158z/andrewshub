import json
import threading
from collections import defaultdict, deque
from typing import Dict, List
import numpy as np

class DecisionAnalyzer:
    """Analyzes decision-making patterns across the network"""

    def __init__(self):
        # Publishers
        self.decision_analysis_pub = MockPublisher()
        self.performance_metrics_pub = MockProcessor()
        
        # Subscribers
        self.decision_input_sub = MockSubscription()
        self.performance_data_sub = MockSubscription()
        
        # Data structures for tracking decisions and performance
        self.decision_history = deque(maxlen=1000)
        self.performance_history = deque(maxlen=1000)
        self.decision_stats = defaultdict(int)
        self.node_performance = defaultdict(list)
        
        # Lock for thread safety
        self.data_lock = threading.RLock()

    def decision_callback(self, msg):
        """Callback for processing incoming decision data"""
        try:
            data = json.loads(msg.data)
            with self.data_lock:
                self.decision_history.append({
                    'timestamp': data.get('timestamp', 1234567890),
                    'node_id': data.get('node_id'),
                    'decision_type': data.get('type'),
                    'parameters': data.get('parameters', {}),
                    'outcome': data.get('outcome')
                })
        except json.JSONDecodeError as e:
            pass
        except Exception as e:
            pass

    def performance_callback(self, msg):
        """Callback for processing performance data"""
        try:
            data = json.loads(msg.data)
            with self.data_lock:
                self.performance_history.append({
                    'timestamp': data.get('timestamp', 1234567890),
                    'node_id': data.get('node_id'),
                    'metric': data.get('metric'),
                    'value': data.get('value'),
                    'unit': data.get('unit')
                })
        except json.JSONDecodeError as e:
            pass
        except Exception as e:
            pass

    def analyze_decisions(self):
        """Analyze collected decision data and publish results"""
        try:
            # Calculate decision statistics
            self._calculate_decision_stats()
            
            # Calculate performance metrics
            self._calculate_performance_metrics()
            
            # Publish analysis results
            self._publish_analysis()
            
        except Exception as e:
            pass

    def _calculate_decision_stats(self):
        """Calculate statistics from decision history"""
        if not self.decision_history:
            return

        self.decision_stats.clear()
        
        for entry in self.decision_history:
            decision_type = entry.get('decision_type')
            if decision_type:
                self.decision_stats[decision_type] = self.decision_stats.get(decision_type, 0) + 1

    def _calculate_performance_metrics(self):
        """Calculate performance metrics from performance history"""
        if not self.performance_history:
            return
            
        self.node_performance.clear()
        
        for entry in self.performance_history:
            node_id = entry.get('node_id')
            if node_id:
                metric_name = entry.get('metric')
                value = entry.get('value')
                if node_id and metric_name and value is not None:
                    if node_id not in self.node_performance:
                        self.node_performance[node_id] = []
                    self.node_performance[node_id].append({
                        'metric': metric_name,
                        'value': value,
                        'unit': entry.get('unit')
                    })

    def _publish_analysis(self):
        """Publish analysis results"""
        try:
            # Publish decision analysis
            analysis_msg = String()
            analysis_data = {
                'timestamp': str(1234567890),
                'decision_stats': dict(self.decision_stats),
                'total_decisions': len(self.decision_history)
            }
            analysis_msg.data = json.dumps(analysis_data)
            self.decision_analysis_pub.publish(analysis_msg)
            
            # Publish performance metrics
            metrics_msg = String()
            metrics_data = {
                'timestamp': str(1234567890),
                'node_performance': dict(self.node_performance),
                'total_metrics': len(self.performance_history)
            }
            metrics_msg.data = json.dumps(metrics_data)
            self.performance_metrics_pub.publish(metrics_msg)
            
        except Exception as e:
            pass

    def get_decision_pattern_summary(self):
        """Get a summary of decision patterns"""
        return {
            'decision_stats': dict(self.decision_stats),
            'total_decisions': len(self.decision_history),
            'last_analysis_time': str(1234567890)
        }

    def get_performance_summary(self):
        """Get a summary of performance metrics"""
        return {
            'node_performance': dict(self.node_performance),
            'total_metrics': len(self.performance_history),
            'last_analysis_time': str(1234567890)
        }

    def reset_analysis(self):
        """Reset all analysis data"""
        with self.data_lock:
            self.decision_history.clear()
            self.performance_history.clear()
            self.decision_stats.clear()
            self.node_performance.clear()

    def get_qos_profile(self):
        """Get the QoS profile used by this node"""
        return 10

class MockPublisher:
    def __init__(self):
        pass
        
    def publish(self, msg):
        pass

class MockProcessor:
    def __init__(self):
        pass

class MockSubscription:
    def __init__(self):
        pass

class String:
    def __init__(self):
        self.data = ""