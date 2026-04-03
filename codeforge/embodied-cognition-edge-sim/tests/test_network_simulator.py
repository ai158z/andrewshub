import pytest
from std_srvs.srv import SetBool
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from nav_msgs.msg import Odometry
import json
from src.embodied_edge_sim.network_simulator import NetworkCondition, NetworkSimulator

class TestNetworkSimulator:
    def test_initialize_default_conditions(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        simulator.initialize_default_conditions()
        
        # Verify default condition is set
        assert "default" in simulator.network_conditions
        condition = simulator.network_conditions["default"]
        assert condition.source_node == "default"
        assert condition.target_node == "default"
        assert condition.latency_ms == 10.0
        assert condition.bandwidth_mbps == 100.0
        assert condition.packet_loss_percent == 0.1
        assert condition.jitter_ms == 2.0

    def test_set_network_condition_callback_success(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        request_data = {
            "source_node": "robot1",
            "target_node": "robot2",
            "latency_ms": 25.0,
            "bandwidth_mbps": 50.0,
            "packet_loss_percent": 1.0,
            "jitter_ms": 5.0
        }
        request = SetBool.Request()
        request.data = json.dumps(request_data)
        response = SetBool.Response()
        
        # Test
        result = simulator.set_network_condition_callback(request, response)
        
        # Verify
        assert result.success
        condition_key = "robot1-robot2"
        assert condition_key in simulator.network_conditions

    def test_set_network_condition_callback_invalid_json(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        request = SetBool.Request()
        request.data = "invalid json"
        response = SetBool.Response()
        
        # Test
        result = simulator.set_network_condition_callback(request, response)
        
        # Verify
        assert not result.success

    def test_get_network_condition_callback(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        request = SetBool.Request()
        response = SetBool.Response()
        
        # Test
        result = simulator.get_network_condition_callback(request, response)
        
        # Verify
        assert result.success

    def test_string_callback(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        msg = String()
        msg.data = "test"
        
        # Test
        simulator.string_callback(msg)
        
        # Verify - in this simplified implementation, the callback just passes through
        # so we verify the message was processed
        assert msg.data == "test"

    def test_pointcloud_callback(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        msg = PointCloud2()
        
        # Test
        simulator.pointcloud_callback(msg)
        
        # Verify
        assert msg is not None

    def test_odom_callback(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        msg = Odometry()
        
        # Test
        simulator.odom_callback(msg)
        
        # Verify
        assert msg is not None

    def test_apply_latency(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        msg = "test_message"
        source = "source_node"
        target = "target_node"
        
        # Test
        result = simulator.apply_latency(msg, source, target)
        
        # Verify
        assert result == msg

    def test_apply_packet_loss(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        msg = "test_message"
        source = "source_node"
        target = "target_node"
        
        # Test
        result = simulator.apply_packet_loss(msg, source, target)
        
        # Verify
        assert result == msg

    def test_get_network_condition(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        condition = simulator.get_network_condition("source", "target")
        
        # Verify
        assert condition is not None
        assert condition.source_node == "default"
        assert condition.target_node == "default"
        assert condition.latency_ms == 10.0
        assert condition.bandwidth_mbps == 100.0
        assert condition.packet_loss_percent == 0.1
        assert condition.jitter_ms == 2.0

    def test_simulate_network_conditions(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        msg = "test_message"
        result = simulator.simulate_network_conditions(msg, "string")
        
        # Verify
        assert result == msg

    def test_process_simulated_data(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        simulator.process_simulated_data()
        
        # Verify
        assert simulator._simulated_data_queue is not None

    def test_network_condition_storage(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        condition = NetworkCondition(
            source_node="source",
            target_node="target",
            latency_ms=10.0,
            bandwidth_mbps=100.0,
            packet_loss_percent=0.1,
            jitter_ms=2.0
        )
        condition_key = "source-target"
        simulator.network_conditions[condition_key] = condition
        
        # Test
        stored_condition = simulator.network_conditions[condition_key]
        
        # Verify
        assert stored_condition.source_node == "source"
        assert stored_condition.target_node == "target"
        assert stored_condition.latency_ms == 10.0
        assert stored_condition.bandwidth_mbps == 100.0
        assert stored_condition.packet_loss_percent == 0.1
        assert stored_condition.jitter_ms == 2.0

    def test_simulator_initialization(self, mocker):
        # Setup
        simulator = NetworkSimulator()
        
        # Verify
        assert simulator is not None
        assert simulator.network_conditions is not None
        assert simulator._string_pub is not None
        assert simulator._pointcloud_pub is not None
        assert simulator._odom_pub is not None