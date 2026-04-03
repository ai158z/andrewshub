import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import PoseStamped
import json
from collections import defaultdict
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class GlobalIntegrator(Node):
    def __init__(self):
        super().__init__('global_integrator')
        
        # Create subscribers with reliable QoS
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        
        self._lock = threading.Lock()
        self._edge_data: Dict[str, Any] = defaultdict(dict)
        self._processed_insights: Dict[str, Any] = defaultdict(dict)
        
        # Subscribers for edge node data
        self._edge_status_sub = self.create_subscription(
            String,
            '/edge_status',
            self._edge_status_callback,
            qos_profile
        )
        
        self._edge_sensor_sub = self.create_subscription(
            PointCloud2,
            '/edge_sensor_data',
            self._edge_sensor_callback,
            qos_profile
        )
        
        self._edge_pose_sub = self.create_subscription(
            PoseStamped,
            '/edge_pose',
            self._edge_pose_callback,
            qos_profile
        )
        
        # Publishers for global awareness
        self._global_insight_pub = self.create_publisher(
            String,
            '/global_insight',
            qos_profile
        )
        
        # Timer for periodic global insight publishing
        self._insight_timer = self.create_timer(1.0, self._publish_global_insights)
        
        self.get_logger().info("GlobalIntegrator node initialized")

    def _edge_status_callback(self, msg: String) -> None:
        """Handle incoming status messages from edge nodes"""
        try:
            data = json.loads(msg.data)
            edge_id = data.get('edge_id')
            if not edge_id:
                self.get_logger().warning("Received status message without edge_id")
                return
                
            with self._lock:
                self._edge_data[edge_id]['status'] = data
                self._processed_insights[edge_id] = data
                
            self.get_logger().debug(f"Updated status for edge node {edge_id}")
        except json.JSONDecodeError:
            self.get_logger().error("Failed to decode JSON from edge status message")
        except Exception as e:
            self.get_logger().error(f"Error processing edge status: {str(e)}")

    def _edge_sensor_callback(self, msg: PointCloud2) -> None:
        """Handle incoming sensor data from edge nodes"""
        try:
            # In a real implementation, we would deserialize the point cloud data
            # For now, we'll store metadata about the message
            edge_id = msg.header.frame_id or "unknown_edge"
            
            with self._lock:
                self._edge_data[edge_id]['sensor_data'] = {
                    'timestamp': msg.header.stamp,
                    'frame_id': msg.header.frame_id,
                    'point_count': len(msg.data) if hasattr(msg, 'data') else 0
                }
                self._processed_insights[edge_id] = self._edge_data[edge_id]
                
            self.get_logger().debug(f"Updated sensor data for edge node {edge_id}")
        except Exception as e:
            self.get_logger().error(f"Error processing sensor data: {str(e)}")

    def _edge_pose_callback(self, msg: PoseStamped) -> None:
        """Handle incoming pose data from edge nodes"""
        try:
            edge_id = msg.header.frame_id or "unknown_edge"
            
            with self._lock:
                self._edge_data[edge_id]['pose'] = {
                    'position': {
                        'x': msg.pose.position.x,
                        'y': msg.pose.position.y,
                        'z': msg.pose.position.z
                    },
                    'orientation': {
                        'x': msg.pose.orientation.x,
                        'y': msg.pose.orientation.y,
                        'z': msg.pose.orientation.z,
                        'w': msg.pose.orientation.w
                    }
                }
                self._processed_insights[edge_id] = self._edge_data[edge_id]
                
            self.get_logger().debug(f"Updated pose for edge node {edge_id}")
        except Exception as e:
            self.get_logger().error(f"Error processing pose data: {str(e)}")

    def _publish_global_insights(self) -> None:
        """Aggregate and publish global insights"""
        try:
            with self._lock:
                # Create a summary of all processed insights
                global_insight = {
                    'timestamp': self.get_clock().now().to_msg().sec,
                    'edge_node_count': len(self._processed_insights),
                    'insights': dict(self._processed_insights)
                }
            
            # Publish the global insight
            msg = String()
            msg.data = json.dumps(global_insight)
            self._global_insight_pub.publish(msg)
            
            self.get_logger().debug("Published global insights")
        except Exception as e:
            self.get_logger().error(f"Error publishing global insights: {str(e)}")

    def get_global_insight(self) -> Dict:
        """Return the current global insight data"""
        with self._lock:
            return dict(self._processed_insights)

def main(args=None):
    rclpy.init(args=args)
    global_integrator = GlobalIntegrator()
    
    try:
        rclpy.spin(global_integrator)
    except KeyboardInterrupt:
        pass
    finally:
        global_integrator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()