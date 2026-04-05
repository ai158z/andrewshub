import pytest
from datetime import datetime
from src.backend.models.agent import Agent, AgentStatus
from sqlalchemy.exc import SQLAlchemyError


def test_agent_creation_with_valid_data():
    agent = Agent(
        name="test-agent",
        description="Test agent description",
        status=AgentStatus.ACTIVE,
        is_online=True,
        ip_address="192.168.1.1",
        hostname="test-host",
        port=8080
    )
    assert agent.name == "test-agent"
    assert agent.description == "Test agent description"
    assert agent.status == AgentStatus.ACTIVE
    assert agent.is_online is True
    assert agent.ip_address == "192.168.1.1"
    assert agent.hostname == "test-host"
    assert agent.port == 8080
    assert isinstance(agent.last_heartbeat, datetime)


def test_agent_creation_with_minimal_data():
    agent = Agent(name="minimal-agent")
    assert agent.name == "minimal-agent"
    assert agent.description is None
    assert agent.status == AgentStatus.ACTIVE
    assert agent.is_online is False
    assert agent.ip_address is None
    assert agent.hostname is None
    assert agent.port is None


def test_agent_name_validation_empty():
    with pytest.raises(ValueError, match="Agent name cannot be empty"):
        Agent(name="")


def test_agent_name_validation_too_long():
    long_name = "a" * 101
    with pytest.raises(ValueError, match="Agent name must be less than 100 characters"):
        Agent(name=long_name)


def test_agent_port_validation_invalid_type():
    with pytest.raises(ValueError, match="Port must be an integer between 1 and 65535"):
        Agent(name="test", port="invalid")


def test_agent_port_validation_out_of_range_low():
    with pytest.raises(ValueError, match="Port must be an integer between 1 and 65535"):
        Agent(name="test", port=0)


def test_agent_port_validation_out_of_range_high():
    with pytest.raises(ValueError, match="Port must be an integer between 1 and 65535"):
        Agent(name="test", port=65536)


def test_agent_port_validation_none():
    agent = Agent(name="test", port=None)
    assert agent.port is None


def test_agent_port_validation_valid():
    agent = Agent(name="test", port=8080)
    assert agent.port == 8080


def test_agent_repr():
    agent = Agent(name="test-agent")
    repr_str = repr(agent)
    assert "Agent(id=" in repr_str
    assert "name='test-agent'" in repr_str


def test_agent_status_enum_values():
    agent_active = Agent(name="active-agent", status=AgentStatus.ACTIVE)
    agent_inactive = Agent(name="inactive-agent", status=AgentStatus.INACTIVE)
    agent_maintenance = Agent(name="maint-agent", status=AgentStatus.MAINTENANCE)
    agent_error = Agent(name="error-agent", status=AgentStatus.ERROR)
    
    assert agent_active.status == AgentStatus.ACTIVE
    assert agent_inactive.status == AgentStatus.INACTIVE
    assert agent_maintenance.status == AgentStatus.MAINTENANCE
    assert agent_error.status == AgentStatus.ERROR


def test_agent_default_values():
    agent = Agent(name="default-test")
    assert agent.status == AgentStatus.ACTIVE
    assert agent.is_online is False
    assert agent.created_at is not None
    assert agent.updated_at is not None
    assert agent.last_heartbeat is not None


def test_agent_init_with_valid_port():
    agent = Agent(name="port-test", port=9000)
    assert agent.port == 9000


def test_agent_init_with_none_port():
    agent = Agent(name="none-port-test")
    assert agent.port is None


def test_agent_init_with_valid_ip_and_hostname():
    agent = Agent(name="network-agent", ip_address="10.0.0.1", hostname="network-host")
    assert agent.ip_address == "10.0.0.1"
    assert agent.hostname == "network-host"


def test_agent_init_with_no_description():
    agent = Agent(name="no-desc-test")
    assert agent.description is None


def test_agent_init_with_description():
    agent = Agent(name="desc-test", description="This is a test agent")
    assert agent.description == "This is a test agent"


def test_agent_init_with_status():
    agent = Agent(name="status-test", status=AgentStatus.MAINTENANCE)
    assert agent.status == AgentStatus.MAINTENANCE


def test_agent_init_with_is_online():
    agent = Agent(name="online-test", is_online=True)
    assert agent.is_online is True


def test_agent_init_with_heartbeat():
    agent = Agent(name="heartbeat-test")
    assert isinstance(agent.last_heartbeat, datetime)