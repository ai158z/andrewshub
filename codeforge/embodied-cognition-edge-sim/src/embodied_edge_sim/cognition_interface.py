import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np
import logging
from typing import Dict, List, Optional
from embodied_edge_sim.edge_processor import EdgeProcessor
from embodied_edge_sim.latency_model import LatencyModel
from embodied_edge_sim.data_flow_visualizer import DataFlowVisualizer


class CognitionInterface(Node):
    def __init__(self, node_name: str = 'cognition_interface'):
        super().__init__(node_name)
        
        # Initialize components
        self.edge_processor = EdgeProcessor()
        self.latency_model = LatencyModel()
        self.data_visualizer = DataFlowVisualizer()
        
        # Create callback group for concurrent callbacks
        self.callback_group = ReentrantCallbackGroup()
        
        # Create subscribers
        self.create_subscription(
            String,
            '/sensor_data',
            self.sensor_data_callback,
            10,
            callback_group=self.callback_group
        )
        
        self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10,
            callback_group=self.callback_group
        )
        
        # Create publishers
        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        self.scan_publisher = self.create_publisher(
            LaserScan,
            '/scan',
            10
        )
        
        # Initialize state
        self.current_pose = None
        self.current_scan = None
        self.decision_history: List[Dict] = []
        
        # Initialize logging
        self.logger = logging.getLogger(node_name)
        self.logger.info("CognitionInterface initialized")

    def sensor_data_callback(self, msg: String) -> None:
        """Handle incoming sensor data messages."""
        try:
            # Process the data with edge processor
            processed_data = self.edge_processor.process_data(msg.data)
            
            # Apply latency model
            latency = self.latency_model.get_latency()
            processed_data = self.latency_model.apply_latency(processed_data, latency)
            
            # Visualize the data flow
            self.data_visualizer.visualize_flow(processed_data)
            
            # Store decision history
            self.decision_history.append({
                'timestamp': self.get_clock().now().to_msg(),
                'data': processed_data
            })
            
            self.logger.info("Processed sensor data")
        except Exception as e:
            self.logger.error(f"Error processing sensor data: {str(e)}")

    def odom_callback(self, msg: Odometry) -> None:
        """Handle odometry updates."""
        try:
            self.current_pose = msg.pose.pose
            self.logger.info("Odometry updated")
        except Exception as e:
            self.logger.error(f"Error handling odometry: {str(e)}")

    def make_decision(self) -> Optional[Twist]:
        """Make a decision based on current sensor data."""
        try:
            if not self.decision_history:
                self.logger.warning("No decision history available")
                return None
                
            # Process latest data to make decision
            latest_data = self.decision_history[-1] if self.decision_history else None
            
            if latest_data:
                # Create a movement command based on processed data
                cmd = Twist()
                cmd.linear.x = 0.5  # Forward velocity
                cmd.angular.z = 0.0  # Angular velocity
                
                self.logger.info("Decision made based on sensor data")
                return cmd
                
            return None
        except Exception as e:
            self.logger.error(f"Error making decision: {str(e)}")
            return None

    def execute_action(self, cmd: Twist) -> None:
        """Execute a movement command."""
        try:
            if cmd:
                self.cmd_vel_publisher.publish(cmd)
                self.logger.info("Executed action command")
        except Exception as e:
            self.logger.error(f"Error executing action: {str(e)}")

    def publish_scan(self, scan_data: LaserScan) -> None:
        """Publish processed laser scan data."""
        try:
            self.scan_publisher.publish(scan_data)
            self.current_scan = scan_data
            self.logger.info("Published laser scan data")
        except Exception as e:
            self.logger.error(f"Error publishing scan: {str(e)}")

    def get_current_state(self) -> Dict:
        """Get the current state of the cognition interface."""
        return {
            'current_pose': self.current_pose,
            'current_scan': self.current_scan,
            'decision_history': self.decision_history
        }

    def cleanup(self) -> None:
        """Clean up resources."""
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    
    try:
        cognition_interface = CognitionInterface()
        executor = SingleThreadedExecutor()
        executor.add_node(cognition_interface)
        
        try:
            executor.spin()
        finally:
            executor.shutdown()
            cognition_interface.cleanup()
    except Exception as e:
        logging.getLogger('cognition_interface').error(f"Error in main: {str(e)}")
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()