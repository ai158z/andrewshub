import pytest
from datetime import datetime
from uuid import UUID, uuid4
from unittest.mock import Mock, patch, MagicMock
from src.backend.quantum.nodes import (
    QuantumNode, NodeStatus, NodeManager, NodeCommunicator, 
    create_node_manager, create_node_communicator
)
from fastapi import HTTPException


def test_create_node_manager():
    session = Mock()
    manager = create_node_manager(session)
    assert isinstance(manager, NodeManager)
    assert manager.db_session == session


def test_create_node_communicator():
    redis_mock = Mock()
    rabbit_mock = Mock()
    communicator = create_node_communicator(redis_mock, rabbit_mock)
    assert isinstance(communicator, NodeCommunicator)
    assert communicator.redis_client == redis_mock
    assert communicator.rabbitmq_connection == rabbit_mock


def test_quantum_node_model():
    node_id = uuid4()
    node = QuantumNode(
        id=node_id,
        name="test-node",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=["sensor", "actuation"]
    )
    assert node.id == node_id
    assert node.name == "test-node"
    assert "sensor" in node.capabilities


def test_node_status_model():
    status = NodeStatus(
        node_id=uuid4(),
        status="active",
        cpu_usage=45.5,
        memory_usage=60.2,
        network_latency=15.3,
        last_updated=datetime.now()
    )
    assert status.status == "active"
    assert status.cpu_usage == 45.5


def test_node_manager_register_node_success():
    session = Mock()
    manager = NodeManager(session)
    node = QuantumNode(
        id=uuid4(),
        name="test",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    
    node_id = manager.register_node(node)
    assert node_id == node.id
    assert node_id in manager.nodes


def test_node_manager_register_node_db_error():
    session = Mock()
    session.add.side_effect = Exception("DB Error")
    manager = NodeManager(session)
    node = QuantumNode(
        id=uuid4(),
        name="test",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    
    with pytest.raises(HTTPException):
        manager.register_node(node)


def test_node_manager_get_node():
    session = Mock()
    manager = NodeManager(session)
    node = QuantumNode(
        id=uuid4(),
        name="test",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    manager.register_node(node)
    
    # Test existing node
    result = manager.get_node(node.id)
    assert result is not None
    assert result.id == node.id
    
    # Test non-existing node
    result = manager.get_node(uuid4())
    assert result is None


def test_node_manager_update_node():
    session = Mock()
    manager = NodeManager(session)
    node = QuantumNode(
        id=uuid4(),
        name="test",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    manager.register_node(node)
    
    # Update existing node
    success = manager.update_node(node.id, {"name": "updated_name"})
    assert success
    assert manager.nodes[node.id].name == "updated_name"
    
    # Update non-existing node
    success = manager.update_node(uuid4(), {"name": "new_name"})
    assert not success


def test_node_manager_remove_node():
    session = Mock()
    manager = NodeManager(session)
    node = QuantumNode(
        id=uuid4(),
        name="test",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    manager.register_node(node)
    
    # Remove existing node
    success = manager.remove_node(node.id)
    assert success
    assert node.id not in manager.nodes
    
    # Remove non-existing node
    success = manager.remove_node(uuid4())
    assert not success


def test_node_manager_list_nodes():
    session = Mock()
    manager = NodeManager(session)
    node1 = QuantumNode(
        id=uuid4(),
        name="test1",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    node2 = QuantumNode(
        id=uuid4(),
        name="test2",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    manager.register_node(node1)
    manager.register_node(node2)
    
    node_ids = manager.list_nodes()
    assert len(node_ids) == 2
    assert node1.id in node_ids
    assert node2.id in node_ids


def test_node_manager_get_node_status():
    session = Mock()
    manager = NodeManager(session)
    node = QuantumNode(
        id=uuid4(),
        name="test",
        status="active",
        last_heartbeat=datetime.now(),
        capabilities=[]
    )
    manager.register_node(node)
    
    status = manager.get_node_status(node.id)
    assert isinstance(status, NodeStatus)
    assert status.node_id == node.id
    assert status.status == "active"


def test_node_manager_get_node_status_not_found():
    session = Mock()
    manager = NodeManager(session)
    
    with pytest.raises(HTTPException):
        manager.get_node_status(uuid4())


def test_node_communicator_send_quantum_state():
    redis_mock = Mock()
    rabbit_mock = Mock()
    rabbit_mock.publish = Mock(return_value=None)
    communicator = NodeCommunicator(redis_mock, rabbit_mock)
    
    node_id = uuid4()
    success = communicator.send_quantum_state(node_id, b"test data", b"key")
    assert success


def test_node_communicator_receive_quantum_state():
    redis_mock = Mock()
    rabbit_mock = Mock()
    rabbit_mock.consume = Mock(return_value=(None, None, b"test data"))
    rabbit_mock.keys = [b"key"]
    
    communicator = NodeCommunicator(redis_mock, rabbit_mock)
    result = communicator.receive_quantum_state(uuid4(), b"key")
    
    assert result == b"test data"


def test_node_communicator_broadcast_to_nodes():
    redis_mock = Mock()
    rabbit_mock = Mock()
    communicator = NodeCommunicator(redis_mock, rabbit_mock)
    
    success = communicator.broadcast_to_nodes(b"test message")
    assert success


def test_node_communicator_sync_node_states():
    redis_mock = Mock()
    rabbit_mock = Mock()
    communicator = NodeCommunicator(redis_mock, rabbit_mock)
    node_id = uuid4()
    
    # Setup mock node
    node = Mock()
    node.state = {}
    communicator.node_manager = Mock()
    communicator.node_manager.get_node.return_value = node
    
    states = [{"node_id": str(node_id), "test": "data"}]
    success = communicator.sync_node_states(states)
    assert success


def test_node_communicator_get_node_state():
    redis_mock = Mock()
    rabbit_mock = Mock()
    communicator = NodeCommunicator(redis_mock, rabbit_mock)
    
    node = Mock()
    node.state = {"key": "value"}
    communicator.node_manager = Mock()
    communicator.node_manager.get_node.return_value = node
    
    state = communicator.get_node_state(uuid4())
    assert state == {"key": "value"}


def test_node_communicator_update_node_state():
    redis_mock = Mock()
    rabbit_mock = Mock()
    communicator = NodeCommunicator(redis_mock, rabbit_mock)
    
    node = Mock()
    node.state = {"existing": "data"}
    communicator.node_manager = Mock()
    communicator.node_manager.get_node.return_value = node
    
    success = communicator.update_node_state(uuid4(), {"new": "value"})
    assert success
    assert node.state == {"existing": "data", "new": "value"}


def test_node_communicator_update_node_state_node_not_found():
    redis_mock = Mock()
    rabbit_mock = Mock()
    communicator = NodeCommunicator(redis_mock, rabbit_mock)
    communicator.node_manager = Mock()
    communicator.node_manager.get_node.return_value = None
    
    success = communicator.update_node_state(uuid4(), {"new": "value"})
    assert not success


def test_get_node_manager_standalone():
    # This should create a manager with default initialization
    manager = get_node_manager()
    assert isinstance(manager, NodeManager)