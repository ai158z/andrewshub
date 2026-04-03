import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import String
from sensor_msgs.msg import Imu, LaserScan
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
import numpy as np
import logging
from typing import Any, Dict, List
import threading
import time

class EdgeProcessor(Node):
    def __init__(self, node_name: str = 'edge_processor'):
        super().__init__(node_name)
        self.get_logger().info("Initializing EdgeProcessor")
        
        # Configuration parameters
        self.declare_parameter('processing_rate', 30)
        self.declare_parameter('imu_topic', '/imu/data')
        self.declare_parameter('laser_topic', '/scan')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('processed_data_topic', '/processed_data')
        
        # Get parameters
        self.processing_rate = self.get_parameter('processing_rate').value
        imu_topic = self.get_parameter('imu_topic').value
        laser_topic = self.get_parameter('laser_topic').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        self.processed_data_topic = self.get_parameter('processed_data_topic').value
        
        # Create subscribers
        self.imu_sub = self.create_subscription(
            Imu,
            imu_topic,
            self.imu_callback,
            10
        )
        self.laser_sub = self.create_subscription(
            LaserScan,
            laser_topic,
            self.laser_callback,
            10
        )
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            cmd_vel_topic,
            self.cmd_vel_callback,
            10
        )
        
        # Create publisher for processed data
        self.processed_data_pub = self.create_publisher(String, self.processed_data_topic, 10)
        
        # Store sensor data
        self.imu_data = None
        self.laser_data = None
        self.cmd_vel_data = None
        self.data_lock = threading.Lock()
        
        # Timer for processing
        self.timer = self.create_timer(1.0 / self.processing_rate, self.process_callback)

    def imu_callback(self, msg: Imu) -> None:
        with self.data_lock:
            self.imu_data = msg
            
    def laser_callback(self, msg: LaserScan) -> None:
        with self.data_lock:
            self.laser_data = msg
            
    def cmd_vel_callback(self, msg: Twist) -> None:
        with self.data_lock:
            self.cmd_vel_data = msg
            
    def process_callback(self) -> None:
        # Process data at regular intervals
        processed_msg = self.process_data()
        if processed_msg:
            self.processed_data_pub.publish(processed_msg)
            
    def process_data(self) -> String:
        with self.data_lock:
            # Create a simple processing example
            if self.imu_data is not None or self.laser_data is not None or self.cmd_vel_data is not None:
                result = "Processed data: "
                
                if self.imu_data:
                    # Process IMU data
                    orientation = self.imu_data.orientation
                    result += f"IMU - Orientation: ({orientation.x}, {orientation.y}, {orientation.z}, {orientation.w}) "
                    
                if self.laser_data:
                    # Process laser data
                    ranges = self.laser_data.ranges
                    if ranges:
                        avg_range = np.mean(ranges)
                        result += f"LiDAR - Average distance: {avg_range:.2f} "
                        
                if self.cmd_vel_data:
                    # Process command velocity data
                    linear_x = self.cmd_vel_data.linear.x
                    angular_z = self.cmd_vel_data.angular.z
                    result += f"CmdVel - Linear: {linear_x:.2f}, Angular: {angular_z:.2f}"
                
                # Create and return processed message
                msg = String()
                msg.data = result
                return msg
        return None

def main(args=None):
    rclpy.init(args=args)
    node = EdgeProcessor()
    executor = SingleThreadedExecutor()
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