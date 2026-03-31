import rclpy
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.subscription import Subscription
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import String
from typing import Dict, Any, Optional, Callable
import json
from codonic_layer.quantum_states import QuantumStates
from codonic_layer.interference_tracker import InterferenceTracker

class ROS2Bridge(Node):
    """ROS2 compatibility layer for message passing and robotic system integration"""
    
    def __init__(self, node_name: str = 'quantum_codonic_bridge'):
        super().__init__(node_name)
        self._publishers: Dict[str, Publisher] = {}
        self._subscriptions: Dict[str, Subscription] = {}
        self._quantum_states = None
        self._interference_tracker = None

    def create_quantum_publisher(self, topic_name: str, msg_type: Any = String) -> Publisher:
        if topic_name in self._publishers:
            return self._publishers[topic_name]
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            depth=10
        )
        
        publisher = self.create_publisher(msg_type, topic_name, qos_profile)
        self._publishers[topic_name] = publisher
        return publisher

    def create_interference_subscription(
        self, 
        topic_name: str, 
        callback: Callable,
        msg_type: Any = String
    ) -> Subscription:
        if topic_name in self._subscriptions:
            return self._subscriptions[topic_name]
            
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            depth=10
        )
        
        subscription = self.create_subscription(
            msg_type, 
            topic_name, 
            callback, 
            qos_profile
        )
        self._subscriptions[topic_name] = subscription
        return subscription

    def publish_quantum_state(
        self, 
        state: QuantumStates, 
        topic_name: str = '/quantum_state'
    ) -> None:
        if not isinstance(state, QuantumStates):
            raise TypeError("State must be an instance of QuantumStates")
        
        # Create publisher if it doesn't exist
        if topic_name not in self._publishers:
            self.create_quantum_publisher(topic_name)
            
        publisher = self._publishers[topic_name]
        
        # Create and publish message
        msg = String()
        state_data = {
            'state_vector': state.get_state().tolist() if hasattr(state.get_state(), 'tolist') else str(state.get_state()),
            'timestamp': self.get_clock().now().nanoseconds,
            'state_type': type(state).__name__
        }
        msg.data = json.dumps(state_data)
        publisher.publish(msg)

    def initialize_quantum_system(self) -> None:
        try:
            self._quantum_states = QuantumStates()
            self._interference_tracker = InterferenceTracker()
            self.get_logger().info("Quantum system initialized successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to initialize quantum system: {e}")
            raise

    def set_quantum_states(self, states: QuantumStates) -> None:
        if not isinstance(states, QuantumStates):
            raise TypeError("States must be an instance of QuantumStates")
        self._quantum_states = states

    def set_interference_tracker(self, tracker: InterferenceTracker) -> None:
        if not isinstance(tracker, InterferenceTracker):
            raise TypeError("Tracker must be an instance of InterferenceTracker")
        self._interference_tracker = tracker

    def get_quantum_publisher(self, topic_name: str) -> Optional[Publisher]:
        return self._publishers.get(topic_name, None)

    def get_interference_subscription(self, topic_name: str) -> Optional[Subscription]:
        return self._subscriptions.get(topic_name, None)

    def subscribe_interference(self, topic_name: str, callback=None) -> None:
        if callback is None:
            # Default callback that processes interference data
            def default_callback(msg):
                self.get_logger().info(f"Received interference data: {msg.data}")
            callback = default_callback
            
        self.create_interference_subscription(topic_name, callback)

    def cleanup(self) -> None:
        self.get_logger().info("Cleaning up ROS2 bridge resources")
        # Clear all collections
        self._publishers.clear()
        self._subscriptions.clear()
        self._quantum_states = None
        self._interference_tracker = None