import json
import base64
import os
from typing import Dict, Any

# Mock implementations to avoid ROS2 dependencies during testing
try:
    import rclpy
    from rclpy.node import Node
    from rclpy.qos import QoSProfile
    from std_msgs.msg import String
    from ed25519_verifier import Ed25519Verifier, BlockchainVerifier, ROS2SignatureHandler
    from ed25519_verifier.exceptions import ROS2SignatureError
except (ImportError, ModuleNotFoundError):
    # Create mock classes if ROS2 is not available
    class MockNode:
        pass
    
    class MockQoSProfile:
        depth = 10
    
    class MockString:
        def __init__(self):
            self.data = ""
    
    class MockPublisher:
        def __init__(self, *args, **kwargs):
            pass
        
        def publish(self, msg):
            pass
    
    # Create a module-like object for rclpy
    class MockRclpy:
        def __init__(self):
            self.Node = MockNode
            self.QoSProfile = MockQoSProfile
            self.String = MockString
            self.Publisher = MockPublisher
            self.init = lambda: None
            self.create_node = lambda node_name: None
            self.spin = lambda: None
            self.shutdown = lambda: None
            self.get_logger = lambda: None
            self.spin_once = lambda: None
            self.ok = lambda: None
            self.create_publisher = lambda *args, **kwargs: MockPublisher()
            self.create_subscription = lambda *args, **kwargs: MockPublisher()
    
    rclpy = MockRclpy()
    
    # Fix the signature handler mock
    rclpy.Publisher = MockPublisher
    rclpy.Node = MockNode
    rclpy.QoSProfile = MockQoSProfile

class SensorDataPublisher(rclpy.Node):
    def __init__(self):
        super().__init__('sensor_data_publisher')
        self.publisher_ = self.create_publisher(rclpy.String, 'signed_sensor_data', 10)
        # Generate or load keys (in a real application, you'd load these securely)
        self.private_key = os.urandom(32)
        from ed25519_verifier import ROS2SignatureHandler  # Import here to avoid circular imports
        self.handler = ROS2SignatureHandler()
        self.public_key = self.handler.get_public_key(self.private_key)

    def publish_sensor_data(self, data):
        try:
            # Sign the data
            signature_b64 = sign_sensor_data(data, self.private_key)
            
            # Create message with data and signature
            message = {
                'data': data,
                'signature': signature_b64,
                'public_key': base64.b64encode(self.public_key).decode('utf-8')
            }
            
            # Create rclpy message
            ros_message = rclpy.String()
            ros_message.data = json.dumps(message)
            
            # Publish the message
            self.publisher_.publish(ros_message)
            self.get_logger().info(f'Publishing signed sensor data: {data}')
        except Exception as e:
            self.get_logger().error(f'Error signing and publishing: {str(e)}')

class SensorDataSubscriber(rclpy.Node):
    def __init__(self):
        super().__init__('sensor_data_subscriber')
        self.subscription = self.create_subscription(
            rclpy.String,
            'signed_sensor_data',
            self.listener_callback,
            rclpy.QoSProfile(depth=10)
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        try:
            # Parse the message
            message_data = json.loads(msg.data)
            sensor_data = message_data['data']
            signature_b64 = message_data['signature']
            public_key_b64 = message_data['public_key']
            public_key = base64.b64decode(public_key_b64)
            
            # Verify the signature
            if verify_sensor_data(sensor_data, signature_b64, public_key):
                self.get_logger().info(f"Verified data: {sensor_data}")
            else:
                self.get_logger().warn("Signature verification failed")
        except Exception as e:
            self.get_logger().error(f'Error processing message: {str(e)}')

def sign_sensor_data(data: Dict[str, Any], private_key: bytes) -> str:
    """Sign sensor data and return base64 encoded signature."""
    try:
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        from ed25519_verifier import ROS2SignatureHandler
        handler = ROS2SignatureHandler()
        data_str = json.dumps(data, sort_keys=True)
        signature = handler.sign_message(data_str, private_key)
        return base64.b64encode(signature).decode('utf-8')
    except Exception as e:
        from ed25519_verifier.exceptions import ROS2SignatureError
        raise ROS2SignatureError(f"Error signing data: {str(e)}")

def verify_sensor_data(data: Dict[str, Any], signature_b64: str, public_key: bytes) -> bool:
    """Verify the signature of sensor data."""
    try:
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        from ed25519_verifier import ROS2SignatureHandler
        handler = ROS2SignatureHandler()
        data_str = json.dumps(data, sort_keys=True)
        signature = base64.b64decode(signature_b64)
        return handler.verify_message(data_str, signature, public_key)
    except Exception as e:
        from ed25519_verifier.exceptions import ROS2SignatureError
        raise ROS2SignatureError(f"Error verifying data: {str(e)}")

def ros2_node_example():
    """Example of a ROS2 node that signs and verifies sensor data."""
    rclpy.init()
    
    # Create publisher node
    publisher = SensorDataPublisher()
    
    # Create subscriber node
    subscriber = SensorDataSubscriber()
    
    # Example sensor data
    sample_data = {
        "sensor_id": "temp_001",
        "timestamp": "2023-01-01T12:00:00Z",
        "temperature": 23.5,
        "humidity": 65.0
    }
    
    # Publish signed data
    publisher.publish_sensor_data(sample_data)
    
    # Spin both nodes
    rclpy.spin_once(publisher)
    rclpy.spin_once(subscriber)
    
    # Clean up
    publisher.destroy_node()
    subscriber.destroy_node()
    rclpy.shutdown()

def main():
    ros2_node_example()

if __name__ == '__main__':
    main()