import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session
from app.services.metric_service import (
    get_all_metrics,
    get_metrics_for_agent,
    create_metric,
    get_metric_by_id,
    delete_metric
)
from app.models.metric import Metric
from app.models.agent import Agent
from app.schemas.metric import MetricCreate
from datetime import datetime

@pytest.fixture
def mock_db_session():
    return Mock(spec=Session)

@pytest.fixture
def mock_metric():
    metric = Mock(spec=Metric)
    metric.id = 1
    metric.agent_id = 1
    metric.metric_type = "cpu"
    metric.value = 80.0
    metric.timestamp = datetime.now()
    return metric

def test_get_all_metrics_success(mock_db_session):
    mock_metrics = [Mock(spec=Metric) for _ in range(3)]
    mock_db_session.query.return_value.all.return_value = mock_metrics
    
    result = get_all_metrics(mock_db_session)
    
    assert result == mock_metrics
    mock_db_session.query.assert_called_once_with(Metric)

def test_get_all_metrics_exception(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        get_all_metrics(mock_db_session)

def test_get_metrics_for_agent_success(mock_db_session):
    mock_agent = Mock(spec=Agent)
    mock_agent.id = 1
    mock_metrics = [Mock(spec=Metric) for _ in range(2)]
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_agent
    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_metrics
    
    result = get_metrics_for_agent(mock_db_session, 1)
    
    assert result == mock_metrics

def test_get_metrics_for_agent_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(ValueError, match="Agent with id 999 not found"):
        get_metrics_for_agent(mock_db_session, 999)

def test_get_metrics_for_agent_exception(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        get_metrics_for_agent(mock_db_session, 1)

def test_create_metric_success(mock_db_session, mock_metric):
    mock_agent = Mock(spec=Agent)
    mock_agent.id = 1
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_agent
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_metric
    
    metric_data = MetricCreate(
        agent_id=1,
        metric_type="cpu",
        value=75.0,
        timestamp=datetime.now()
    )
    
    result = create_metric(mock_db_session, metric_data)
    
    assert result == mock_metric
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_create_metric_agent_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    metric_data = MetricCreate(
        agent_id=999,
        metric_type="cpu",
        value=75.0,
        timestamp=datetime.now()
    )
    
    with pytest.raises(ValueError, match="Agent with id 999 not found"):
        create_metric(mock_db_session, metric_data)

def test_create_metric_exception(mock_db_session, mock_metric):
    mock_db_session.add.side_effect = Exception("Creation failed")
    mock_agent = Mock(spec=Agent)
    mock_agent.id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_agent
    
    metric_data = MetricCreate(
        agent_id=1,
        metric_type="cpu",
        value=75.0,
        timestamp=datetime.now()
    )
    
    with pytest.raises(Exception, match="Creation failed"):
        create_metric(mock_db_session, metric_data)

def test_get_metric_by_id_found(mock_db_session, mock_metric):
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_metric
    
    result = get_metric_by_id(mock_db_session, 1)
    
    assert result == mock_metric

def test_get_metric_by_id_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    result = get_metric_by_id(mock_db_session, 999)
    
    assert result is None

def test_get_metric_by_id_exception(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        get_metric_by_id(mock_db_session, 1)

def test_delete_metric_success(mock_db_session, mock_metric):
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_metric
    
    result = delete_metric(mock_db_session, 1)
    
    assert result is True
    mock_db_session.delete.assert_called_once_with(mock_metric)
    mock_db_session.commit.assert_called_once()

def test_delete_metric_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(ValueError, match="Metric with id 999 not found"):
        delete_metric(mock_db_session, 999)

def test_delete_metric_exception(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        delete_metric(mock_db_session, 1)