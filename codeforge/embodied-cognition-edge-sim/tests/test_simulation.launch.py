import pytest
from unittest.mock import patch, MagicMock
from launch import LaunchDescription
from launch.actions import TimerAction, GroupAction
import sys
import os

# Add the simulation.launch.py to the path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock the launch utilities
with patch('ament_index_python.packages.get_package_share_directory') as mock_get_package:
    mock_get_package.return_value = '/fake/path'
    
    # We need to import after patching
    from simulation import generate_launch_description

def test_generate_launch_description_returns_launch_description():
    result = generate_launch_description()
    assert isinstance(result, LaunchDescription)

def test_launch_description_contains_group_action():
    ld = generate_launch_description()
    group_actions = [action for action in ld.children if isinstance(action, GroupAction)]
    assert len(group_actions) == 1

def test_launch_description_contains_all_expected_nodes():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    
    # Check that we have timer actions for each node (9 total)
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    assert len(timer_actions) == 9
    
    # Check that each timer has a node with expected names
    node_names = [
        'edge_node', 'network_simulator', 'cognition_interface', 'visualization_manager',
        'global_integrator', 'node_coordinator', 'physical_interface', 
        'decision_analyzer', 'data_flow_visualizer'
    ]
    
    timer_node_names = []
    for timer in timer_actions:
        # Each timer should contain a Node action with a specific name
        if hasattr(timer, 'actions') and timer.actions:
            node = timer.actions[0]
            if hasattr(node, 'name'):
                timer_node_names.append(node.name)
    
    # Check all expected nodes are present
    for name in node_names:
        assert any(name in timer_name for timer_name in timer_node_names), f"Missing node: {name}"

def test_edge_node_has_correct_parameters():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find edge_node (first one)
    edge_node_timer = None
    for timer in timer_actions:
        if timer.period == 1.0:
            edge_node_timer = timer
            break
    
    assert edge_node_timer is not None
    edge_node = edge_node_timer.actions[0]
    assert edge_node.name == 'edge_node'
    assert hasattr(edge_node, 'parameters')
    assert len(edge_node.parameters) > 0
    assert 'param1' in edge_node.parameters[0]
    assert edge_node.parameters[0]['param1'] == 'value1'

def test_data_flow_visualizer_has_update_rate_parameter():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find data_flow_visualizer (last one)
    data_flow_timer = None
    for timer in timer_actions:
        if timer.period == 8.0:
            data_flow_timer = timer.actions[0]
            break
    
    assert data_flow_timer is not None
    assert data_flow_timer.name == 'data_flow_visualizer'
    assert hasattr(data_flow_timer, 'parameters')
    assert len(data_flow_timer.parameters) > 0
    assert 'update_rate' in data_flow_timer.parameters[0]
    assert data_flow_timer.parameters[0]['update_rate'] == 30.0

def test_all_nodes_have_correct_package_and_executables():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    
    # Get all timer actions
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Check all 9 nodes
    expected_nodes = 9
    found_nodes = 0
    
    for timer in timer_actions:
        # Each timer should have one action which is a Node
        if hasattr(timer, 'actions') and len(timer.actions) > 0:
            node = timer.actions[0]
            if (hasattr(node, 'package') and 
                hasattr(node, 'executable') and 
                node.package == 'embodied_edge_sim' and
                node.executable in [
                    'edge_node', 'network_simulator', 'cognition_interface', 
                    'visualization_manager', 'global_integrator', 
                    'node_coordinator', 'physical_interface', 
                    'decision_analyzer', 'data_flow_visualizer'
                ]):
                found_nodes += 1
    
    assert found_nodes == expected_nodes, f"Expected {expected_nodes} nodes, found {found_nodes}"

def test_node_coordinator_starts_after_all_other_nodes():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Should be the 9th node (period=9.0)
    coordinator_timer = None
    for timer in timer_actions:
        if timer.period == 9.0:
            coordinator_timer = timer
            break
    
    assert coordinator_timer is not None
    node = coordinator_timer.actions[0]
    assert node.name == 'decision_analyzer'

def test_visualization_nodes_start_in_correct_order():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Check periods are in ascending order (timers should be sequential)
    periods = sorted([timer.period for timer in timer_actions])
    assert periods == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

@patch('ament_index_python.packages.get_package_share_directory')
def test_package_share_directory_called_once(mock_get_package):
    mock_get_package.return_value = '/fake/path'
    generate_launch_description()
    mock_get_package.assert_called_once_with('embodied_edge_sim')

def test_cognition_interface_is_present():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find the cognition interface timer (period 3.0)
    cognition_timer = None
    for timer in timer_actions:
        if timer.period == 3.0:
            cognition_timer = timer
            break
    
    assert cognition_timer is not None
    node = cognition_timer.actions[0]
    assert node.name == 'cognition_interface'

def test_network_simulator_is_present():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find the network simulator timer (period 2.0)
    network_timer = None
    for timer in timer_actions:
        if timer.period == 2.0:
            network_timer = timer
            break
    
    assert network_timer is not None
    node = network_timer.actions[0]
    assert node.name == 'network_simulator'

def test_physical_interface_is_present():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find the physical interface timer (period 7.0)
    physical_timer = None
    for timer in timer_actions:
        if timer.period == 7.0:
            physical_timer = timer
            break
    
    assert physical_timer is not None
    node = physical_timer.actions[0]
    assert node.name == 'physical_interface'

def test_global_integrator_is_present():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group1.children if isinstance(action, TimerAction)]
    
    # Find the global integrator timer (period 5.0)
    integrator_timer = None
    for timer in timer_actions:
        if timer.period == 5.0:
            integrator_timer = timer
            break
    
    assert integrator_timer is not None
    node = integrator_timer.actions[0]
    assert node.name == 'global_integrator'

def test_node_coordinator_is_present():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find the node coordinator timer (period 6.0)
    coordinator_timer = None
    for timer in timer_actions:
        if timer.period == 6.0:
            coordinator_timer = timer
            break
    
    assert coordinator_timer is not None
    node = coordinator_timer.actions[0]
    assert node.name == 'node_coordinator'

def test_data_flow_visualizer_is_present():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find the data flow visualizer timer (period 8.0)
    visualizer_timer = None
    for timer in timer_actions:
        if timer.period == 8.0:
            visualizer_timer = timer
            break
    
    assert visualizer_timer is not None
    node = visualizer_timer.actions[0]
    assert node.name == 'data_flow_visualizer'

def test_visualization_manager_is_present():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find the visualization manager timer (period 4.0)
    manager_timer = None
    for timer in timer_actions:
        if timer.period == 4.0:
            manager_timer = timer
            break
    
    assert manager_timer is not None
    node = manager_timer.actions[0]
    assert node.name == 'visualization_manager'

def test_all_nodes_have_screen_output():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    for timer in timer_actions:
        node = timer.actions[0]
        assert hasattr(node, 'output')
        assert node.output == 'screen'

def test_all_nodes_from_embodied_edge_sim_package():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    for timer in timer_actions:
        node = timer.actions[0]
        assert hasattr(node, 'package')
        assert node.package == 'embodied_edge_sim'

def test_all_nodes_have_unique_names():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    names = []
    for timer in timer_actions:
        node = timer.actions[0]
        names.append(node.name)
    
    assert len(names) == len(set(names)), "Duplicate node names found"

def test_all_nodes_use_correct_executables():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    expected_executables = {
        'edge_node', 'network_simulator', 'cognition_interface',
        'visualization_manager', 'global_integrator', 'node_coordinator',
        'physical_interface', 'decision_analyzer', 'data_flow_visualizer'
    }
    
    found_executables = set()
    for timer in timer_actions:
        node = timer.actions[0]
        found_executables.add(node.executable)
    
    assert found_executables == expected_executables

def test_launch_description_includes_all_required_nodes():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Should have 9 TimerActions for 9 different nodes
    assert len(timer_actions) == 9

def test_nodes_have_sequential_start_times():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    periods = [timer.period for timer in timer_actions]
    expected_periods = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    assert sorted(periods) == expected_periods

def test_decision_analyzer_is_last_node():
    ld = generate_launch_description()
    group_action = [action for action in ld.children if isinstance(action, GroupAction)][0]
    timer_actions = [action for action in group_action.children if isinstance(action, TimerAction)]
    
    # Find the decision analyzer (period 9.0)
    analyzer_timer = None
    for timer in timer_actions:
        if timer.period == 9.0:
            analyzer_timer = timer
            break
    
    assert analyzer_timer is not None
    node = analyzer_timer.actions[0]
    assert node.name == 'decision_analyzer'