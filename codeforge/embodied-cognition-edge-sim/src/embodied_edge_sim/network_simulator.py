import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
import random
import time
from typing import Dict, List, Tuple
import threading
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from std_srvs.srv import SetBool as SetBoolSrv
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import json
from collections import defaultdict, deque
from dataclasses import dataclass
import numpy as np

@dataclass
class NetworkCondition:
    source_node: str
    target_node: str
    latency_ms: float
    bandwidth_mbps: float
    packet_loss_percent: float
    jitter_ms: float

class NetworkSimulator(Node):
    def __init__(self):
        super().__init__('network_simulator')
        
        # Service for setting network conditions
        self._condition_service = self.create_service(
            SetBoolSrv,
            'set_network_condition',
            self.set_network_condition_callback,
            callback_group=ReentrantCallbackGroup()
        )
        
        # Service for getting network conditions
        self._get_condition_service = self.create_service(
            SetBoolSrv,
            'get_network_condition',
            self.get_network_condition_callback,
            callback_group=ReentrantCallbackGroup()
        )
        
        # Publishers for simulated network traffic
        self._string_pub = self.create_publisher(
            String, 
            'simulated_string_data', 
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
            callback_group=ReentrantCallbackGroup()
        )
        
        self._pointcloud_pub = self.create_publisher(
            PointCloud2,
            'simulated_pointcloud_data',
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
            callback_group=ReentrantCallbackGroup()
        )
        
        self._odom_pub = self.create_publisher(
            Odometry,
            'simulated_odom_data',
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
            callback_group=ReentrantCallbackGroup()
        )
        
        # Subscriber for incoming data to simulate
        self._string_sub = self.create_subscription(
            String,
            'string_data',
            self.string_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
            callback_group=ReentrantCallbackGroup()
        )
        
        self._pointcloud_sub = self.create_subscription(
            PointCloud2,
            'pointcloud_data',
            self.pointcloud_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
            callback_group=ReentrantCallbackGroup()
        )
        
        self._odom_sub = self.create_subscription(
            Odometry,
            'odom_data',
            self.odom_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
            callback_group=ReentrantCallbackGroup()
        )
        
        # Network condition storage
        self.network_conditions: Dict[str, NetworkCondition] = {}
        self._condition_lock = threading.Lock()
        
        # Simulated data queues
        self._simulated_data_queue: Dict[str, deque] = defaultdict(deque)
        self._queue_lock = threading.Lock()
        
        # Timer for processing simulated data
        self._timer = self.create_timer(0.01, self.process_simulated_data)
        
        # Initialize default network conditions
        self.initialize_default_conditions()
        
    def initialize_default_conditions(self):
        """Initialize default network conditions for all node pairs"""
        with self._condition_lock:
            # Default conditions: low latency, high bandwidth, minimal packet loss
            default_condition = NetworkCondition(
                source_node="default",
                target_node="default",
                latency_ms=10.0,
                bandwidth_mbps=100.0,
                packet_loss_percent=0.1,
                jitter_ms=2.0
            )
            self.network_conditions["default"] = default_condition

    def set_network_condition_callback(self, request, response):
        """Service callback to set network conditions"""
        try:
            condition_data = json.loads(request.data)
            condition = NetworkCondition(
                source_node=condition_data.get("source_node", "default"),
                target_node=condition_data.get("target_node", "default"),
                latency_ms=condition_data.get("latency_ms", 10.0),
                bandwidth_mbps=condition_data.get("bandwidth_mbps", 100.0),
                packet_loss_percent=condition_data.get("packet_loss_percent", 0.1),
                jitter_ms=condition_data.get("jitter_ms", 2.0)
            )
            
            condition_key = f"{condition.source_node}-{condition.target_node}"
            with self._condition_lock:
                self.network_conditions[condition_key] = condition
                
            response.success = True
            response.message = f"Set network condition for {condition_key}"
            return response
        except Exception as e:
            response.success = False
            response.message = f"Failed to set network condition: {str(e)}"
            return response

    def get_network_condition_callback(self, request, response):
        """Service callback to get network conditions"""
        try:
            with self._condition_lock:
                conditions_str = json.dumps([
                    {
                        "source_node": cond.source_node,
                        "target_node": cond.target_node,
                        "latency_ms": cond.latency_ms,
                        "bandwidth_mbps": cond.bandwidth_mbps,
                        "packet_loss_percent": cond.packet_loss_percent,
                        "jitter_ms": cond.jitter_ms
                    }
                    for cond in self.network_conditions.values()
                ])
            
            response.success = True
            response.message = json.dumps(conditions_str)
            return response
        except Exception as e:
            response.success = False
            response.message = f"Failed to get network conditions: {str(e)}"
            return response

    def string_callback(self, msg):
        """Callback for string data messages"""
        # Apply network simulation
        simulated_msg = self.simulate_network_conditions(msg, "string")
        if simulated_msg:
            self._string_pub.publish(simulated_msg)

    def pointcloud_callback(self, msg):
        """Callback for point cloud data messages"""
        # Apply network simulation
        simulated_msg = self.simulate_network_conditions(msg, "pointcloud")
        if simulated_msg:
            self._pointcloud_pub.publish(simulated_msg)

    def odom_callback(self, msg):
        """Callback for odometry data messages"""
        # Apply network simulation
        simulated_msg = self.simulate_network_conditions(msg, "odometry")
        if simulated_msg:
            self._odom_pub.publish(simulated_msg)

    def simulate_network_conditions(self, msg, msg_type):
        """
        Apply network conditions to a message.
        This is a simplified simulation that would add latency and packet loss.
        """
        # In a real implementation, this would apply actual network conditions
        # For now, we just pass the message through with potential modifications
        return msg

    def process_simulated_data(self):
        """Process and send simulated data from queues"""
        # This method would be called periodically to process queued data
        pass

    def apply_latency(self, msg, source, target):
        """Apply latency to a message based on network conditions"""
        # In a real implementation, this would delay the message based on 
        # network conditions between source and target
        return msg

    def apply_packet_loss(self, msg, source, target):
        """Apply packet loss based on network conditions"""
        # In a real implementation, this would potentially drop packets
        # based on the packet loss percentage in network conditions
        return msg

    def get_network_condition(self, source_node, target_node):
        """Get network condition between two nodes"""
        condition_key = f"{source_node}-{target_node}"
        with self._condition_lock:
            return self.network_conditions.get(condition_key, self.network_conditions.get("default"))

def main(args=None):
    rclpy.init(args=args)
    node = NetworkSimulator()
    
    # Use a multi-threaded executor to handle callbacks
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()