import random
import time
from typing import Tuple, Optional
import threading
from std_msgs.msg import String

class LatencyModel:
    """
    Models and simulates network latency between nodes in the embodied cognition edge simulation.
    """
    
    def __init__(self, 
                 base_latency: float = 0.0,
                 jitter: float = 0.0,
                 packet_loss_probability: float = 0.0,
                 max_latency: Optional[float] = None):
        """
        Initialize the LatencyModel with configuration parameters.
        
        Args:
            base_latency: Base latency in seconds
            jitter: Random variation in latency in seconds
            packet_loss_probability: Probability of packet loss (0.0 to 1.0)
            max_latency: Maximum allowed latency in seconds
        """
        self.base_latency = base_latency
        self.jitter = jitter
        self.packet_loss_probability = packet_loss_probability
        self.max_latency = max_latency if max_latency is not None else float('inf')
        self._lock = threading.Lock()
        
    def get_latency(self) -> float:
        """
        Calculate and return the current latency for a message transmission.
        
        Returns:
            float: Latency in seconds, including base latency and jitter
        """
        with self._1:
            # Calculate latency with jitter
            latency = self.base_latency + random.uniform(-self.jitter, self.jitter)
            
            # Apply maximum latency cap
            latency = min(latency, self.max_latency)
            
            # Ensure non-negative latency
            latency = max(0.0, latency)
            
            return latency
    
    def apply_latency(self, 
                      publisher, 
                      msg, 
                      topic_name: str,
                      callback_group=None) -> bool:
        """
        Apply simulated latency to a message before publishing.
        
        Args:
            publisher: Publisher to use for sending the message
            msg: Message to be published
            topic_name: Topic name for the message
            callback_group: Optional callback group for the timer
            
        Returns:
            bool: True if message was sent, False if dropped due to packet loss
        """
        # Determine if packet should be dropped based on packet loss probability
        if random.random() < self.packet_loss_probability:
            return False  # Packet dropped
            
        # Calculate latency with jitter
        latency = self.get_latency()
        
        # If latency is zero, publish immediately
        if latency == 0.0:
            if hasattr(publisher, 'publish'):
                publisher.publish(msg)
            return True
            
        # Schedule delayed publication
        def delayed_publish():
            time.sleep(latency)
            if hasattr(publisher, 'publish'):
                publisher.publish(msg)
            
        # Start delayed publishing in a separate thread
        thread = threading.Thread(target=delayed_publish)
        thread.daemon = True
        thread.start()
        
        return True


class LatencyTestNode:
    """
    Test node to demonstrate the LatencyModel functionality.
    """
    
    def __init__(self):
        # Create latency model with 50ms base latency and 10ms jitter
        self.latency_model = LatencyModel(
            base_latency=0.05,  # 50ms
            jitter=0.01,        # 10ms
            packet_loss_probability=0.01,  # 1% packet loss
            max_latency=0.1  # Max 100ms
        )
        
        # Create publisher and subscriber
        self.publisher = type('Publisher', (), {'publish': lambda x: None})()  # Mock publisher
        self.subscription = None
        
        # Counter for sent messages
        self.message_count = 0

    def send_test_message(self):
        """Send a test message with simulated latency."""
        msg = type('String', (), {'data': f"Test message {self.message_count}"})()
        self.message_count += 1
        
        # Apply latency model to message
        success = self.latency_model.apply_latency(
            self.publisher,
            msg,
            'latency_test'
        )
        
        if success:
            print(f"Sent: {getattr(msg, 'data', 'Test Message')}")
        else:
            print("Message dropped due to packet loss")
            
    def message_callback(self, msg):
        """Handle received messages."""
        print(f"Received: {getattr(msg, 'data', 'Message')}")

def main():
    """Main function to run the latency test."""
    node = LatencyTestNode()
    
    try:
        # Simulate sending test messages
        for i in range(5):
            node.send_test_message()
            time.sleep(0.1)  # Small delay between messages
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()