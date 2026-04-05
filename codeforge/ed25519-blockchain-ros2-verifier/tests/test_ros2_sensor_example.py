import json
import base64
import pytest
from unittest.mock import patch, MagicMock, mock_open
from examples.ros2_sensor_example import sign_sensor_data, verify_sensor_data, SensorDataPublisher, SensorDataSubscriber
from ed25519_verifier.exceptions import ROS2SignatureError

def test_sign_sensor_data_success():
    test_data = {"temperature": 23.5, "humidity": 65.0}
    private_key = b"test_private_key_12345"
    
    with patch("ed25519_verifier.ROS2SignatureHandler.sign_message") as mock_sign:
        mock_sign.return_value = b"fake_signature"
        result = sign_sensor_data(test_data, private_key)
        expected_signature = base64.b64encode(b"fake_signature").decode('utf-8')
        assert result == expected_signature

def test_sign_sensor_data_exception():
    test_data = {"temperature": 23.5, "humidity": 65.0}
    private_key = b"test_private_key_12345"
    
    with patch("ed25519_verifier.ROS2SignatureHandler.sign_message", side_effect=Exception("Signing failed")):
        with pytest.raises(ROS2SignatureError):
            sign_sensor_data(test_data, private_key)

def test_verify_sensor_data_success():
    test_data = {"temperature": 23.5, "humidity": 65.0}
    signature_b64 = base64.b64encode(b"fake_signature").decode('utf-8')
    public_key = b"test_public_key_12345"
    
    with patch("ed25519_verifier.ROS2SignatureHandler.verify_message", return_value=True):
        result = verify_sensor_data(test_data, signature_b64, public_key)
        assert result is True

def test_verify_sensor_data_exception():
    test_data = {"temperature": 23.5, "humidity": 65.0}
    signature_b64 = base64.b64encode(b"fake_signature").decode('utf-8')
    public_key = b"test_public_key_12345"
    
    with patch("ed25519_verifier.ROS2SignatureHandler.verify_message", side_effect=Exception("Verification failed")):
        with pytest.raises(ROS2SignatureError):
            verify_sensor_data(test_data, signature_b64, public_key)

def test_sensor_data_publisher_init():
    with patch("rclpy.node.Node.__init__"):
        publisher = SensorDataPublisher()
        assert publisher.private_key is not None
        assert publisher.public_key is not None

def test_sensor_data_publisher_publish_sensor_data():
    with patch("rclpy.node.Node.__init__"), \
         patch("rclpy.node.Node.create_publisher"), \
         patch("rclpy.node.Node.get_logger") as mock_logger, \
         patch("ed25519_verifier.ROS2SignatureHandler.get_public_key"), \
         patch("examples.ros2_sensor_example.sign_sensor_data", return_value="fake_signature"):
        
        publisher = SensorDataPublisher()
        mock_publisher = MagicMock()
        publisher.publisher_ = mock_publisher
        publisher.private_key = b"test_key"
        publisher.public_key = b"test_pub_key"
        
        test_data = {"temperature": 23.5}
        publisher.publish_sensor_data(test_data)
        
        mock_publisher.publish.assert_called_once()
        mock_logger().info.assert_called()

def test_sensor_data_publisher_publish_exception():
    with patch("rclpy.node.Node.__init__"), \
         patch("rclpy.node.Node.create_publisher"), \
         patch("rclpy.node.Node.get_logger") as mock_logger, \
         patch("examples.ros2_sensor_example.sign_sensor_data", side_effect=Exception("Signing error")):
        
        publisher = SensorDataPublisher()
        test_data = {"temperature": 23.5}
        publisher.publish_sensor_data(test_data)
        mock_logger().error.assert_called()

def test_sensor_data_subscriber_init():
    with patch("rclpy.node.Node.__init__"), \
         patch("rclpy.node.Node.create_subscription"):
        
        subscriber = SensorDataSubscriber()
        assert subscriber.subscription is not None

def test_sensor_data_subscriber_callback_success():
    with patch("rclpy.node.Node.__init__"), \
         patch("rclpy.node.Node.create_subscription"), \
         patch("rclpy.node.Node.get_logger") as mock_logger:
        
        subscriber = SensorDataSubscriber()
        mock_msg = MagicMock()
        mock_msg.data = json.dumps({
            "data": {"temperature": 23.5},
            "signature": "fake_signature",
            "public_key": base64.b64encode(b"test_pub_key").decode('utf-8')
        })
        
        with patch("ed25519_verifier.ROS2SignatureHandler.verify_message", return_value=True):
            subscriber.listener_callback(mock_msg)
            mock_logger().info.assert_called_with("Verified data: {'temperature': 23.5}")

def test_sensor_data_subscriber_callback_verification_failed():
    with patch("rclpy.node.Node.__init__"), \
         patch("rclpy.node.Node.create_subscription"), \
         patch("rclpy.node.Node.get_logger") as mock_logger:
        
        subscriber = SensorDataSubscriber()
        mock_msg = MagicMock()
        mock_msg.data = json.dumps({
            "data": {"temperature": 23.5},
            "signature": "fake_signature",
            "public_key": base64.b64encode(b"test_pub_key").decode('utf-8')
        })
        
        with patch("ed25519_verifier.ROS2SignatureHandler.verify_message", return_value=False):
            subscriber.listener_callback(mock_msg)
            mock_logger().warn.assert_called_with("Signature verification failed")

def test_sensor_data_subscriber_callback_exception():
    with patch("rclpy.node.Node.__init__"), \
         patch("rclpy.node.Node.create_subscription"), \
         patch("rclpy.node.Node.get_logger") as mock_logger:
        
        subscriber = SensorDataSubscriber()
        mock_msg = MagicMock()
        mock_msg.data = "invalid_json"
        
        subscriber.listener_callback(mock_msg)
        mock_logger().error.assert_called()

def test_ros2_node_example():
    with patch("rclpy.init"), \
         patch("rclpy.spin_once"), \
         patch("rclpy.shutdown"), \
         patch("examples.ros2_sensor_example.SensorDataPublisher") as mock_publisher, \
         patch("examples.ros2_sensor_example.SensorDataSubscriber") as mock_subscriber:
        
        from examples.ros2_sensor_example import ros2_node_example
        ros2_node_example()
        
        mock_publisher().publish_sensor_data.assert_called()
        mock_publisher().destroy_node.assert_called()
        mock_subscriber().destroy_node.assert_called()

def test_sign_sensor_data_empty_dict():
    test_data = {}
    private_key = b"test_private_key_12345"
    
    with patch("ed25519_verifier.ROS2SignatureHandler.sign_message") as mock_sign:
        mock_sign.return_value = b"fake_signature"
        result = sign_sensor_data(test_data, private_key)
        assert isinstance(result, str)

def test_verify_sensor_data_empty_data():
    test_data = {}
    signature_b64 = base64.b64encode(b"fake_signature").decode('utf-8')
    public_key = b"test_public_key_12345"
    
    with patch("ed25519_verifier.ROS2SignatureHandler.verify_message", return_value=True):
        result = verify_sensor_data(test_data, signature_b64, public_key)
        assert result is True

def test_sign_sensor_data_invalid_input():
    with pytest.raises(ROS2SignatureError):
        sign_sensor_data("invalid_input", b"key")

def test_verify_sensor_data_invalid_input():
    with pytest.raises(ROS2SignatureError):
        verify_sensor_data("invalid_data", "invalid_signature", b"key")

def test_sign_sensor_data_none_data():
    with pytest.raises(ROS2SignatureError):
        sign_sensor_data(None, b"key")

def test_verify_sensor_data_none_data():
    with pytest.raises(ROS2SignatureError):
        verify_sensor_data(None, "signature", b"key")