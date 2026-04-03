import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """Generate launch description for all simulation nodes"""
    
    package_share_directory = get_package_share_directory('embodied_edge_sim')
    
    # Edge node
    edge_node = Node(
        package='embodied_edge_sim',
        executable='edge_node',
        name='edge_node',
        output='screen',
        parameters=[{
            'param1': 'value1'
        }]
    )
    
    # Network simulator node
    network_simulator = Node(
        package='embodied_edge_sim',
        executable='network_simulator',
        name='network_simulator',
        output='screen'
    )
    
    # Cognition interface node
    cognition_interface = Node(
        package='embodied_edge_sim',
        executable='cognition_interface',
        name='cognition_interface',
        output='screen'
    )
    
    # Visualization manager node
    visualization_manager = Node(
        package='embodied_edge_sim',
        executable='visualization_manager',
        name='visualization_manager',
        output='screen'
    )
    
    # Global integrator node
    global_integrator = Node(
        package='embodied_edge_sim',
        executable='global_integrator',
        name='global_integrator',
        output='screen'
    )
    
    # Node coordinator
    node_coordinator = Node(
        package='embodied_edge_sim',
        executable='node_coordinator',
        name='node_coordinator',
        output='screen'
    )
    
    # Physical interface
    physical_interface = Node(
        package='embodied_edge_sim',
        executable='physical_interface',
        name='physical_interface',
        output='screen'
    )
    
    # Decision analyzer
    decision_analyzer = Node(
        package='embodied_edge_sim',
        executable='decision_analyzer',
        name='decision_analyzer',
        output='screen'
    )
    
    # Data flow visualizer
    data_flow_visualizer = Node(
        package='embodied_edge_sim',
        executable='data_flow_visualizer',
        name='data_flow_visualizer',
        output='screen',
        parameters=[{
            'update_rate': 30.0
        }]
    )
    
    return LaunchDescription([
        launch.actions.GroupAction([
            launch.actions.TimerAction(period=1.0, actions=[edge_node]),
            launch.actions.TimerAction(period=2.0, actions=[network_simulator]),
            launch.actions.TimerAction(period=3.0, actions=[cognition_interface]),
            launch.actions.TimerAction(period=4.0, actions=[visualization_manager]),
            launch.actions.TimerAction(period=5.0, actions=[global_integrator]),
            launch.actions.TimerAction(period=6.0, actions=[node_coordinator]),
            launch.actions.TimerAction(period=7.0, actions=[physical_interface]),
            launch.actions.TimerAction(period=8.0, actions=[data_flow_visualizer]),
            launch.actions.TimerAction(period=9.0, actions=[decision_analyzer])
        ])
    ])