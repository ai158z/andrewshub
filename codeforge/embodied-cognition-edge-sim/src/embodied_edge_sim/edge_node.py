import time
import json
from typing import Dict, Any, Optional
import logging

# Mock rclpy for testing purposes
class MockNode:
    def __init__(self, name):
        self.name = name
        self.logger = MockLogger()
        
    def get_logger(self):
        return self.logger
        
    def declare_parameter(self, name, default):
        # Simple parameter storage
        setattr(self, name.replace('.', '_'), default)
        return type('MockParam', (), {'value': default})()

class MockLogger:
    def __init__(self):
        self.error_calls = []
        self.info_calls = []
        self.warning_calls = []
        
    def info(self, msg):
        self.info_calls.append(msg)
        
    def error(self, msg):
        self.error_calls.append(msg)
        
    def warning(self, msg):
        self.warning_calls.append(msg)

class MockQoSProfile:
    def __init__(self, depth=10, reliability=None, durability=None):
        self.depth = depth
        self.reliability = reliability
        self.durability = durability

class MockReentrantCallbackGroup:
    pass

class MockPublisher:
    def __init__(self, node, msg_type, topic, qos_profile):
        self.node = node
        self.msg_type = msg_type
        self.topic = topic
        self.qos_profile = qos_profile
        self.publish_calls = []
        
    def publish(self, msg):
        self.publish_calls.append(msg)

class MockSubscription:
    def __init__(self, node, msg_type, topic, callback, qos_profile, callback_group=None):
        self.node = node
        self.msg_type = msg_type
        self.topic = topic
        self.callback = callback
        self.qos_profile = qos_profile
        self.callback_group = callback_group

class EdgeNode:
    """Implements individual edge node behavior with local processing capabilities"""

    def __init__(self, node_name: str = 'edge_node'):
        self.node = MockNode(node_name)
        
        # Initialize callback groups
        self.callback_group = MockReentrantCallbackGroup()
        
        # Initialize components
        self.latency_model = LatencyModel()
        self.edge_processor = EdgeProcessor()
        
        # Node configuration
        self.node_id = self.node.declare_parameter('node_id', 'edge_node_0').value
        self.simulation_mode = self.node.declare_parameter('simulation_mode', True).value
        self.processing_rate = self.node.declare_parameter('processing_rate', 10).value  # Hz
        
        # Data storage
        self.local_data = {}
        self.processed_data = {}
        self.node_state = "INIT"
        
        # Create publishers
        self.decision_publisher = MockPublisher(
            self.node, 
            str, 
            f'{self.node_id}/decision', 
            MockQoSProfile(depth=10)
        )
        
        self.status_publisher = MockPublisher(
            self.node,
            str,
            f'{self.node_id}/status',
            MockQoSProfile(depth=10)
        )
        
        # Create subscriptions
        self.scan_subscription = MockSubscription(
            self.node,
            str,
            '/scan',
            self.scan_callback,
            MockQoSProfile(depth=10),
            callback_group=self.callback_group
        )
        
        self.odom_subscription = MockSubscription(
            self.node,
            str,
            '/odom',
            self.odom_callback,
            MockQoSProfile(depth=10),
            callback_group=self.callback_group
        )
        
        # Create timers
        self.timer = "MockTimer"
        
        # Initialize state
        self.node_state = "ACTIVE"
        self.node.get_logger().info(f'EdgeNode {self.node_id} initialized')
        
    def scan_callback(self, msg) -> None:
        """Handle incoming laser scan data"""
        try:
            # Apply latency model to the data
            latency = self.latency_model.get_latency()
            processed_msg = self.latency_model.apply_latency(msg, latency)
            
            # Process the data
            processed_data = self.edge_processor.process_data(processed_msg)
            self.local_data['scan'] = processed_data
            
            # Publish status
            status_msg = json.dumps({"status": "scan_received", "data": processed_data})
            self.status_publisher.publish(status_msg)
            
        except Exception as e:
            self.node.get_logger().error(f"Error in scan_callback: {str(e)}")
            
    def odom_callback(self, msg) -> None:
        """Handle incoming odometry data"""
        try:
            # Apply latency model to the data
            latency = self.latency_model.get_latency()
            processed_msg = self.latency_model.apply_latency(msg, latency)
            
            # Process the data
            processed_data = self.edge_processor.process_data(processed_msg)
            self.local_data['odom'] = processed_data
            
            # Publish status
            status_msg = json.dumps({"status": "odom_received", "data": processed_data})
            self.status_publisher.publish(status_msg)
            
        except Exception as e:
            self.node.get_logger().error(f"Error in odom_callback: {str(e)}")
            
    def processing_timer_callback(self) -> None:
        """Periodic processing of local data"""
        try:
            if not self.local_data:
                return
                
            # Process local data
            processed = self.edge_processor.process_data(self.local_data)
            self.processed_data = processed
            
            # Publish decision
            decision_msg = json.dumps(processed)
            self.decision_publisher.publish(decision_msg)
            
        except Exception as e:
            self.node.get_logger().error(f"Error in processing_timer_callback: {str(e)}")

    def destroy_node(self) -> None:
        """Clean up resources when node is destroyed"""
        self.node.get_logger().info(f'EdgeNode {self.node_id} shutting down')

    def get_logger(self):
        """Provide access to the node's logger for testing"""
        return self.node.get_logger()


class LatencyModel:
    def get_latency(self):
        return 0.05  # 50ms default latency
        
    def apply_latency(self, msg, latency):
        # Simulate latency application
        time.sleep(latency)
        return msg


class EdgeProcessor:
    def process_data(self, data):
        # Simulate data processing
        time.sleep(0.01)  # 10ms processing time
        return {"processed": True, "data": str(data)}


def main(args=None):
    # Mock rclpy.init for simulation mode
    print("EdgeNode initialized in simulation mode")
    
    try:
        node = EdgeNode()
        print("EdgeNode created successfully")
    except Exception as e:
        logging.error(f"Error creating EdgeNode: {str(e)}")


if __name__ == '__main__':
    main()