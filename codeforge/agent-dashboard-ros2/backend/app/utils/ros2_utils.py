import importlib
from typing import Dict, Any, Optional
import logging
import rclpy
from rclpy.node import Node
from backend.app.ros2_bridge import init_ros2_node, get_agent_status, get_system_metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import rclpy, but allow failure in test environments
try:
    import rclpy
    from rclpy.node import Node
    RCLPY_AVAILABLE = True
    rclpy.init()
except ImportError:
    rclpy = None
    Node = object
    RCLPY_AVAILABLE = False

class ROS2NodeManager:
    def __init__(self):
        self.node: Optional[Node] = None
        self.node_initialized = False

    def initialize_node(self, node_name: str = 'agent_dashboard_node') -> bool:
        """Initialize the ROS2 node if not already initialized"""
        try:
            if not RCLPY_AVAILABLE:
                logger.warning("rclpy not available, skipping ROS2 node initialization")
                return False
                
            if not self.node_initialized:
                self.node = init_ros2_node(node_name)
                self.node_initialized = True
                logger.info(f"ROS2 node '{node_name}' initialized successfully")
                return True
            return True
        except Exception as e:
            logger.error(f"Failed to initialize ROS2 node: {str(e)}")
            return False

    def cleanup_node(self) -> bool:
        """Clean up the ROS2 node"""
        if not RCLPY_AVAILABLE:
            return True  # If rclpy is not available, nothing to clean up
            
        try:
            if self.node_initialized:
                if self.node:
                    self.node.destroy_node()
                rclpy.shutdown()
                self.node_initialized = False
                logger.info("ROS2 node cleaned up successfully")
                return True
            return True
        except Exception as e:
            logger.error(f"Error during node cleanup: {str(e)}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the ROS2 node"""
        return {
            "initialized": self.node_initialized,
            "node": self.node.get_name() if self.node and self.node_initialized else None
        }

# Global instance for managing the node
_node_manager = ROS2NodeManager()

def create_ros2_node(node_name: str = 'agent_dashboard_node') -> bool:
    """Create and initialize a new ROS2 node"""
    return _node_manager.initialize_node(node_name)

def destroy_ros2_node() -> bool:
    """Destroy the current ROS2 node"""
    return _node_manager.cleanup_node()

def get_node_status() -> Dict[str, Any]:
    """Get the current status of the ROS2 node manager"""
    return _node_manager.get_status()