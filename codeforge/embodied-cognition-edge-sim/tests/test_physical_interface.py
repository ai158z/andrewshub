import pytest
import math
from unittest.mock import Mock, patch, MagicMock
from src.embodied_edge_sim.physical_interface import PhysicalInterface
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

@pytest.fixture
def physical_interface():
    with patch('rclpy.init'), patch('rclpy.spin_once'), patch('rclpy.create_node'):
        pi = PhysicalInterface()
        pi.get_clock().now().to_msg.return_value = Mock()
        yield pi

def test_initialization(physical_interface):
    assert physical_interface.current_position == [0.0, 0.0, 0.0]
    assert physical_interface.current_velocity == [0.0, 0.0, 0.0]
    assert physical_interface.obstacle_map == {}
    assert physical_interface.sensor_data == {}

def test_cmd_vel_callback_updates_velocity(physical_interface):
    twist = Twist()
    twist.linear.x = 1.0
    twist.linear.y = 0.5
    twist.angular.z = 0.2
    
    physical_interface._cmd_vel_callback(twist)
    
    # Account for latency model which adds small delays
    assert physical_interface.current_velocity[0] == pytest.approx(1.0, abs=0.1)
    assert physical_interface.current_velocity[1] == pytest.approx(0.5, abs=0.1)
    assert physical_interface.current_velocity[2] == pytest.approx(0.2, abs=0.1)

def test_odometry_callback_updates_position(physical_interface):
    odom = Odometry()
    odom.pose.pose.position.x = 2.5
    odom.pose.pose.position.y = 1.8
    odom.pose.pose.orientation.w = 1.0  # No rotation
    
    physical_interface._odometry_callback(odom)
    
    assert physical_interface.current_position[0] == 2.5
    assert physical_interface.current_position[1] == 1.8
    assert physical_interface.current_position[2] == 0.0

def test_quaternion_to_euler_conversion():
    # Test identity quaternion (no rotation)
    q = Mock()
    q.x, q.y, q.z, q.w = 0.0, 0.0, 0.0, 1.0
    
    pi = PhysicalInterface()
    roll, pitch, yaw = pi._quaternion_to_euler(q)
    
    assert roll == 0.0
    assert pitch == 0.0
    assert yaw == 0.0

def test_quaternion_to_euler_with_rotation():
    # Test 90-degree rotation around Z axis
    q = Mock()
    q.x, q.y, q.z, q.w = 0.0, 0.0, 0.707, 0.707  # Approximately 90 degrees
    
    pi = PhysicalInterface()
    roll, pitch, yaw = pi._quaternion_to_euler(q)
    
    assert yaw == pytest.approx(math.pi/2, abs=0.01)

def test_generate_laser_scan(physical_interface):
    scan = physical_interface._generate_laser_scan()
    
    assert isinstance(scan, LaserScan)
    assert scan.angle_min == -math.pi
    assert scan.angle_max == math.pi
    assert scan.range_min == 0.1
    assert scan.range_max == 10.0
    assert len(scan.ranges) > 0

def test_simulate_obstacle_detection(physical_interface):
    # Test obstacle detection at obstacle angle
    distance = physical_interface._simulate_obstacle_detection(0.0)
    assert distance == pytest.approx(3.0, abs=0.5)  # 3.0 + noise
    
    # Test normal distance at non-obstacle angle
    distance = physical_interface._simulate_obstacle_detection(math.pi/4)
    assert distance == pytest.approx(8.0, abs=0.5)  # 8.0 + noise

def test_get_current_position(physical_interface):
    position = physical_interface.get_current_position()
    assert position == [0.0, 0.0, 0.0]
    
    # Modify position and check copy
    physical_interface.current_position = [1.0, 2.0, 3.0]
    position = physical_interface.get_current_position()
    assert position == [1.0, 2.0, 3.0]

def test_get_current_velocity(physical_interface):
    velocity = physical_interface.get_current_velocity()
    assert velocity == [0.0, 0.0, 0.0]
    
    # Modify velocity and check copy
    physical_interface.current_velocity = [1.0, 2.0, 3.0]
    velocity = physical_interface.get_current_velocity()
    assert velocity == [1.0, 2.0, 3.0]

def test_get_obstacle_map(physical_interface):
    obstacles = physical_interface.get_obstacle_map()
    assert obstacles == {}
    
    # Modify obstacle map and check copy
    physical_interface.obstacle_map = {"obstacle1": [1.0, 2.0]}
    obstacles = physical_interface.get_obstacle_map()
    assert obstacles == {"obstacle1": [1.0, 2.0]}

def test_get_sensor_data(physical_interface):
    data = physical_interface.get_sensor_data()
    assert data == {}
    
    # Modify sensor data and check copy
    physical_interface.sensor_data = {"sensor1": [1.0, 2.0, 3.0]}
    data = physical_interface.get_sensor_data()
    assert data == {"sensor1": [1.0, 2.0, 3.0]}

def test_update_obstacle_map(physical_interface):
    obstacles = {"new_obstacle": [5.0, 10.0]}
    physical_interface.update_obstacle_map(obstacles)
    assert physical_interface.obstacle_map == obstacles

def test_update_sensor_data(physical_interface):
    data = {"new_sensor": [1.0, 2.0, 3.0]}
    physical_interface.update_sensor_data(data)
    assert physical_interface.sensor_data == data

def test_start_simulation(physical_interface):
    with patch('threading.Thread') as mock_thread:
        physical_interface.start_simulation()
        mock_thread.assert_called_once()
        assert physical_interface.simulation_active == True

def test_stop_simulation(physical_interface):
    with patch('threading.Thread') as mock_thread_class:
        mock_thread_instance = Mock()
        mock_thread_class.return_value = mock_thread_instance
        physical_interface.start_simulation()
        physical_interface.stop_simulation()
        mock_thread_instance.join.assert_called_once()
        assert physical_interface.simulation_active == False

def test_sensor_simulation_loop_updates_position(physical_interface):
    physical_interface.current_velocity = [1.0, 0.0, 0.1]
    physical_interface.simulation_active = True
    
    # Run simulation for one iteration
    with patch('time.sleep'), patch('time.time', side_effect=[0, 0.1]):
        physical_interface._sensor_simulation_loop()
    
    # Position should be updated based on velocity * dt
    assert physical_interface.current_position[0] == pytest.approx(0.1, abs=0.01)
    assert physical_interface.current_position[1] == 0.0
    assert physical_interface.current_position[2] == pytest.approx(0.01, abs=0.01)

def test_periodic_update_publishes_messages(physical_interface):
    with patch.object(physical_interface.laser_pub, 'publish') as mock_laser, \
         patch.object(physical_interface.point_cloud_pub, 'publish') as mock_cloud, \
         patch.object(physical_interface.status_pub, 'publish') as mock_status:
        
        physical_interface._periodic_update()
        
        mock_laser.assert_called_once()
        mock_cloud.assert_called_once()
        mock_status.assert_called_once()

def test_cmd_vel_callback_error_handling(physical_interface, caplog):
    # Create a malformed message that will cause an error
    twist = Twist()
    twist.linear.x = float('inf')  # This will cause an error when applying latency
    
    physical_interface._cmd_vel_callback(twist)
    
    # Check that error was logged
    assert "Error processing cmd_vel" in caplog.text

def test_odometry_callback_error_handling(physical_interface, caplog):
    # Create malformed odometry that will cause conversion error
    odom = Odometry()
    odom.pose.pose.orientation.w = float('nan')  # This will cause error in quaternion conversion
    
    physical_interface._odometry_callback(odom)
    
    # Check that error was logged
    assert "Error processing odometry" in caplog.text

def test_destroy_node_stops_simulation(physical_interface):
    with patch('threading.Thread'), patch('rclpy.node.Node.destroy_node') as mock_destroy:
        physical_interface.start_simulation()
        physical_interface.destroy_node()
        assert physical_interface.simulation_active == False
        mock_destroy.assert_called_once()