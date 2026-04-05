import rclpy
from rclpy.node import Node
from std_msgs.msg import String, ByteMultiArray
import json
from typing import Any
from sha3_hasher.core import sha3_512_hash
import importlib.metadata

class HashingNode(Node):
    def __init__(self):
        super().__init__('sha3_hasher_node')
        self.publisher_ = self.create_publisher(String, 'hash_result', 10)
        self.subscription = self.create_subscription(
            ByteMultiArray,
            'data_to_hash',
            self.hashing_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info(f"SHA3 Hasher Node v{self.get_version()} started")

    def get_version(self):
        try:
            return importlib.metadata.version('sha3-hasher')
        except importlib.metadata.PackageNotFoundError:
            return "unknown"

    def hashing_callback(self, msg: ByteMultiArray) -> None:
        try:
            # Convert byte array to bytes
            data_bytes = bytes(msg.data)
            
            # Perform SHA3-512 hash
            hash_result = sha3_512_hash(data_bytes)
            
            # Prepare result message
            result_msg = {
                'input_size': len(data_bytes),
                'hash': hash_result.hex()
            }
            
            # Publish result
            response = String()
            response.data = json.dumps(result_msg)
            self.publisher_.publish(response)
            self.get_logger().info(f"Hashed {len(data_bytes)} bytes")
            
        except Exception as e:
            self.get_logger().error(f"Hashing failed: {str(e)}")

def create_ros2_node() -> Node:
    """Create and return a ROS2 node for distributed SHA3 hashing"""
    rclpy.init()
    return HashingNode()