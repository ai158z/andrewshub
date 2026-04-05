import pytest
from datetime import datetime
from backend.app.schemas.agent import (
    AgentStatus, AgentBase, AgentCreate, AgentUpdate, 
    AgentInDBBase, Agent, AgentStatusUpdate, AgentHealth, 
    SystemHealth, MetricData, AgentMetrics
)
from pydantic import ValidationError


def test_agent_base_required_fields():
    with pytest.raises(ValidationError):
        AgentBase()


def test_agent_base_with_valid_data():
    agent = AgentBase(
        name="Test Agent",
        status=AgentStatus.ONLINE,
        ros2_node_name="/test_node"
    )
    assert agent.name == "Test Agent"
    assert agent.status == AgentStatus.ONLINE
    assert agent.ros2_node_name == "/test_node"


def test_agent_base_optional_fields_default():
    agent = AgentBase(name="Test Agent", status=AgentStatus.OFFLINE)
    assert agent.description is None
    assert agent.ros2_node_name is None
    assert agent.capabilities == []
    assert agent.config == {}
    assert agent.last_heartbeat is None
    assert agent.metadata == {}


def test_agent_create_inherits_base():
    agent_create = AgentCreate(
        name="Create Agent",
        description="Test description",
        status=AgentStatus.MAINTENANCE,
        ros2_node_name="/create_test"
    )
    assert agent_create.name == "Create Agent"
    assert agent_create.description == "Test description"
    assert agent_create.status == AgentStatus.MAINTENANCE
    assert agent_create.ros2_node_name == "/create_test"


def test_agent_update_allows_partial_updates():
    agent_update = AgentUpdate(name="Updated Agent")
    assert agent_update.name == "Updated Agent"
    assert agent_update.status is None  # Not required


def test_agent_in_db_requires_id_and_timestamps():
    with pytest.raises(ValidationError):
        AgentInDBBase()


def test_agent_in_db_full_data():
    agent = Agent(
        id=1,
        name="DB Agent",
        status=AgentStatus.ONLINE,
        created_at=datetime(2023, 1, 1, 12, 0, 0)
    )
    assert agent.id == 1
    assert agent.name == "DB Agent"
    assert agent.status == AgentStatus.ONLINE
    assert agent.created_at == datetime(2023, 1, 1, 12, 0, 0)


def test_agent_status_update_requires_status():
    with pytest.raises(ValidationError):
        AgentStatusUpdate()


def test_agent_status_update_with_status():
    update = AgentStatusUpdate(status=AgentStatus.WARNING)
    assert update.status == AgentStatus.WARNING
    assert update.last_heartbeat is None
    assert update.metadata is None


def test_agent_health_model():
    health = AgentHealth(
        status=AgentStatus.ONLINE,
        response_time=0.1,
        details={"cpu": "normal"}
    )
    assert health.status == AgentStatus.ONLINE
    assert health.response_time == 0.1
    assert health.details == {"cpu": "normal"}


def test_system_health_model():
    health = SystemHealth(
        status="healthy",
        agents_active=5,
        agents_total=10,
        timestamp=datetime(2023, 1, 1, 12, 0, 0)
    )
    assert health.status == "healthy"
    assert health.agents_active == 5
    assert health.agents_total == 10
    assert health.timestamp == datetime(2023, 1, 1, 12, 0, 0)


def test_system_health_optional_metrics():
    health = SystemHealth(
        status="healthy",
        agents_active=5,
        agents_total=10,
        timestamp=datetime(2023, 1, 1, 12, 0, 0),
        metrics={"cpu": 45.5}
    )
    assert health.metrics == {"cpu": 45.5}


def test_metric_data_model():
    metric = MetricData(
        name="cpu_usage",
        value=45.5,
        unit="%",
        timestamp=datetime(2023, 1, 1, 12, 0, 0)
    )
    assert metric.name == "cpu_usage"
    assert metric.value == 45.5
    assert metric.unit == "%"
    assert metric.timestamp == datetime(2023, 1, 1, 12, 0, 0)


def test_agent_metrics_model():
    metrics_data = [
        MetricData(
            name="cpu_usage",
            value=30.0,
            unit="%",
            timestamp=datetime(2023, 1, 1, 12, 0, 0)
        )
    ]
    agent_metrics = AgentMetrics(
        agent_id=1,
        metrics=metrics_data,
        timestamp=datetime(2023, 1, 1, 12, 0, 0)
    )
    assert agent_metrics.agent_id == 1
    assert agent_metrics.metrics == metrics_data
    assert agent_metrics.timestamp == datetime(2023, 1, 1, 12, 0, 0)


def test_agent_status_enum_values():
    assert AgentStatus.ONLINE == "online"
    assert AgentStatus.OFFLINE == "offline"
    assert AgentStatus.ERROR == "error"
    assert AgentStatus.WARNING == "warning"
    assert AgentStatus.MAINTENANCE == "maintenance"


def test_agent_base_with_all_fields():
    config_data = {"param1": "value1"}
    metadata_data = {"version": "1.0"}
    capabilities_data = ["navigate", "scan"]
    agent = AgentBase(
        name="Full Agent",
        description="Test agent with all fields",
        status=AgentStatus.WARNING,
        ros2_node_name="/full_node",
        capabilities=capabilities_data,
        config=config_data,
        last_heartbeat=datetime(2023, 1, 1, 12, 0, 0),
        metadata=metadata_data
    )
    assert agent.name == "Full Agent"
    assert agent.description == "Test agent with all fields"
    assert agent.status == AgentStatus.WARNING
    assert agent.ros2_node_name == "/full_node"
    assert agent.capabilities == capabilities_data
    assert agent.config == config_data
    assert agent.last_heartbeat == datetime(2023, 1, 1, 12, 0, 0)
    assert agent.metadata == metadata_data


def test_agent_in_db_base_orm_mode():
    # Test that orm_mode allows dict conversion
    data = {
        "id": 1,
        "name": "Test",
        "status": "online",
        "created_at": datetime(2023, 1, 1, 12, 0, 0),
        "updated_at": datetime(2023, 1, 1, 13, 0, 0)
    }
    agent = AgentInDBBase(**data)
    assert agent.dict() == data


def test_agent_status_update_includes_metadata():
    update = AgentStatusUpdate(
        status=AgentStatus.ERROR,
        metadata={"error": "Connection failed"}
    )
    assert update.status == AgentStatus.ERROR
    assert update.metadata == {"error": "Connection failed"}


def test_system_health_with_none_metrics():
    health = SystemHealth(
        status="healthy",
        agents_active=3,
        agents_total=10,
        timestamp=datetime(2023, 1, 1, 12, 0, 0)
    )
    assert health.metrics is None