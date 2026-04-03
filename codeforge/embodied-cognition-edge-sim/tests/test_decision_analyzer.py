import json
from collections import deque
from unittest.mock import Mock, patch, call
import pytest
from rclpy.node import Node
from std_msgs.msg import String
from src.embodied_edge_sim.decision_analyzer import DecisionAnalyzer


class TestDecisionAnalyzer:
    @patch('rclpy.node.Node.__init__')
    @patch('rclpy.node.Node.create_publisher')
    @patch('rclpy.node.Node.create_subscription')
    @patch('rclpy.node.Node.create_timer')
    def setup_method(self):
        with patch('rclpy.node.Node.__init__'), \
             patch('rclpy.node.Node.create_publisher'), \
             patch('rclpy.node.Node.create_subscription'), \
             patch('rclpy.node.Node.create_timer'):
            self.analyzer = DecisionAnalyzer()

    def test_init(self):
        assert self.analyzer.decision_history == deque(maxlen=1000)
        assert self.analyzer.performance_history == deque(maxlen=1000)
        assert isinstance(self.analyzer.decision_stats, dict)
        assert isinstance(self.analyzer.node_performance, dict)

    def test_decision_callback_valid_data(self):
        msg = String()
        msg.data = json.dumps({
            'node_id': 'test_node',
            'type': 'navigation',
            'parameters': {'param1': 'value1'},
            'outcome': 'success'
        })
        
        with patch.object(self.analyzer, 'get_clock') as mock_clock:
            mock_clock.return_value.now.return_value.nanoseconds = 12345
            self.analyzer.decision_callback(msg)
            
        assert len(self.analyzer.decision_history) == 1
        assert self.analyzer.decision_history[0]['node_id'] == 'test_node'

    def test_decision_callback_invalid_json(self):
        msg = String()
        msg.data = "invalid json"
        
        with patch.object(self.analyzer.get_logger(), 'error') as mock_error:
            self.analyzer.decision_callback(msg)
            mock_error.assert_called()

    def test_performance_callback_valid_data(self):
        msg = String()
        msg.data = json.dumps({
            'node_id': 'perf_node',
            'metric': 'latency',
            'value': 0.5,
            'unit': 'ms'
        })
        
        with patch.object(self.analyzer, 'get_clock') as mock_clock:
            mock_clock.return_value.now.return_value.nanoseconds = 12345
            self.analyzer.performance_callback(msg)
            
        assert len(self.analyzer.performance_history) == 1
        assert self.analyzer.performance_history[0]['node_id'] == 'perf_node'

    def test_performance_callback_invalid_json(self):
        msg = String()
        msg.data = "invalid json"
        
        with patch.object(self.analyzer.get_logger(), 'error') as mock_error:
            self.analyzer.performance_callback(msg)
            mock_error.assert_called()

    def test_calculate_decision_stats(self):
        with patch.object(self.analyzer, 'decision_history', deque([{'decision_type': 'navigation'}, {'decision_type': 'control'}])):
            self.analyzer._calculate_decision_stats()
            assert self.analyzer.decision_stats['navigation'] == 1
            assert self.analyzer.decision_stats['control'] == 1

    def test_calculate_performance_metrics(self):
        with patch.object(self.analyzer, 'performance_history', deque([{'node_id': 'node1', 'metric': 'latency', 'value': 0.5, 'unit': 'ms'}])):
            self.analyzer._calculate_performance_metrics()
            assert 'node1' in self.analyzer.node_performance

    def test_publish_analysis(self):
        with patch.object(self.analyzer, 'decision_analysis_pub') as mock_pub1, \
             patch.object(self.analyzer, 'performance_metrics_pub') as mock_pub2:
            
            msg = String()
            msg.data = json.dumps({'test': 'data'})
            
            self.analyzer._publish_analysis()
            
            mock_pub1.publish.assert_called()
            mock_pub2.publish.assert_called()

    def test_get_decision_pattern_summary(self):
        summary = self.analyzer.get_decision_pattern_summary()
        assert 'decision_stats' in summary
        assert 'total_decisions' in summary
        assert 'last_analysis_time' in summary

    def test_get_performance_summary(self):
        summary = self.analyzer.get_performance_summary()
        assert 'node_performance' in summary
        assert 'total_metrics' in summary
        assert 'last_analysis_time' in summary

    def test_reset_analysis(self):
        self.analyzer.decision_history.append({'test': 'data'})
        self.analyzer.performance_history.append({'test': 'data'})
        self.analyzer.decision_stats['test_type'] = 1
        self.analyzer.node_performance['test_node'] = [{'metric': 'test', 'value': 1, 'unit': 'ms'}]
        
        self.analyzer.reset_analysis()
        
        assert len(self.analyzer.decision_history) == 0
        assert len(self.analyzer.performance_history) == 0
        assert len(self.analyzer.decision_stats) == 0
        assert len(self.analyzer.node_performance) == 0

    def test_get_qos_profile(self):
        qos_profile = self.analyzer.get_qos_profile()
        assert qos_profile.depth == 10

    def test_analyze_decisions_error_handling(self):
        with patch.object(self.analyzer, '_calculate_decision_stats', side_effect=Exception("Test error")), \
             patch.object(self.analyzer.get_logger(), 'error') as mock_error:
            self.analyzer.analyze_decisions()
            mock_error.assert_called()

    def test_analyze_decisions_success(self):
        with patch.object(self.analyzer, '_calculate_decision_stats'), \
             patch.object(self.analyzer, '_calculate_performance_metrics'), \
             patch.object(self.analyzer, '_publish_analysis'):
            self.analyzer.analyze_decisions()

    def test_publish_analysis_error(self):
        with patch.object(self.analyzer.decision_analysis_pub, 'publish', side_effect=Exception("Test error")), \
             patch.object(self.analyzer.get_logger(), 'error') as mock_error, \
             patch.object(self.analyzer, 'decision_stats', return_value={}):
            self.analyzer._publish_analysis()
            mock_error.assert_called()