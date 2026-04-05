import pytest
from datetime import datetime
from typing import List
from pydantic import ValidationError
from backend.app.schemas.metric import (
    MetricBase, 
    MetricCreate, 
    MetricResponse, 
    MetricListResponse, 
    MetricResponseList, 
    MetricCreateList,
    MetricBaseModel,
    MetricCreate as DuplicatedMetricCreate,
    MetricResponse as DuplicatedMetricResponse
)

class TestMetricBase:
    def test_valid_metric_base(self):
        # Test valid creation of MetricBase
        metric = MetricBase(
            value=25.5,
            timestamp=datetime.now(),
            agent_id=1,
            unit="kg",
            description="test metric"
        )
        assert metric.value == 25.5
        assert metric.agent_id == 1

    def test_metric_base_without_optional_fields(self):
        # Test MetricBase with only required fields
        metric = MetricBase(
            value=100,
            timestamp=datetime.now()
        )
        assert metric.value == 100
        assert metric.agent_id is None  # Should default to None

class TestMetricCreate:
    def test_valid_metric_create(self):
        # Test valid MetricCreate
        metric = MetricCreate(
            value=30.0,
            agent_id=1,
            unit="celsius",
            description="temperature",
            timestamp=datetime.now(),
            data=[]
        )
        assert metric.value == 30.0
        assert metric.agent_id == 1

    def test_metric_create_missing_required_fields(self):
        # Test that required fields are validated
        with pytest.raises(ValidationError):
            MetricCreate()

class TestDuplicatedMetricModels:
    def test_duplicated_metric_create(self):
        # Test the duplicated MetricCreate model
        data_list = [{"key": "value"}]
        metric = DuplicatedMetricCreate(
            value=25.0,
            agent_id=2,
            unit="m",
            description="distance",
            timestamp=datetime.now(),
            data=data_list
        )
        assert metric.agent_id == 2
        assert metric.data == data_list

    def test_duplicated_metric_response(self):
        # Test the duplicated MetricResponse model
        data_list = [{"test": "data"}]
        metric = DuplicatedMetricResponse(
            id=5,
            value=10.5,
            agent_id=3,
            unit="km",
            description="distance metric",
            timestamp=datetime.now(),
            data=data_list
        )
        assert metric.id == 5
        assert metric.agent_id == 3
        assert metric.data == data_list

class TestMetricResponseModels:
    def test_metric_response_from_orm(self):
        # Test MetricResponse creation with from_orm
        class MockMetric:
            def __init__(self, id, agent_id, value, unit, description, timestamp):
                self.id = id
                self.agent_id = agent_id
                self.value = value
                self.unit = unit
                self.description = description
                self.timestamp = timestamp

        mock_data = MockMetric(1, 2, 42.0, "kg", "weight", datetime.now())
        response = MetricResponse.from_orm([mock_data] * 6)
        assert response.id == 1
        assert response.agent_id == 2
        assert response.value == 42.0

    def test_metric_list_response_from_orm(self):
        # Test MetricListResponse from_orm method
        class MockMetric:
            def __init__(self, id, agent_id, value, unit, description, timestamp):
                self.id = id
                self.agent_id = agent_id
                self.value = value
                self.unit = unit
                self.description = description
                self.timestamp = timestamp

        mock_data = MockMetric(1, 1, 100, "g", "test", datetime.now())
        mock_list = [mock_data]
        response = MetricListResponse.from_orm(mock_list)
        assert len(response.data) == 1
        assert response.data[0].value == 100

    def test_metric_response_list_from_orm(self):
        # Test MetricResponseList from_orm method
        data = [
            type('MockData', (), {
                'id': 1,
                'agent_id': 1,
                'value': 50,
                'unit': 'm',
                'description': 'length',
                'timestamp': datetime.now()
            })()
        ] * 6

        response = MetricResponseList.from_orm(data)
        # This should properly create a response with the first element's data
        assert response is not None

class TestMetricBaseModel:
    def test_metric_base_model_from_orm(self):
        # Test MetricBaseModel from_orm method
        mock_data = [
            type('MockData', (), {'id': 1})(),
            type('MockData', (), {'agent_id': 2})(),
            type('MockData', (), {'value': 100.0})(),
            type('MockData', (), {'unit': 'unit'})(),
            type('MockData', (), {'description': 'test'})(),
            type('MockData', (), {'timestamp': datetime.now()})(),
            type('MockData', (), {'data': []})()
        ]

        # This tests the from_orm implementation
        response = MetricBaseModel.from_orm(mock_data)
        assert response is not None

class TestMetricCreateList:
    def test_metric_create_list(self):
        # Test MetricCreateList model
        metric = MetricCreateList(
            value=75.5,
            timestamp=datetime.now(),
            data=[]
        )
        assert metric.value == 75.5

    def test_metric_create_list_from_base(self):
        # Test creating MetricCreateList from base data
        metric = MetricCreateList(
            value=10,
            timestamp=datetime.now()
        )
        assert metric.value == 10

class TestEdgeCases:
    def test_metric_base_with_invalid_data(self):
        # Test that invalid data raises validation error
        with pytest.raises(ValidationError):
            MetricBase(value="invalid", timestamp="not_a_date")

    def test_metric_create_optional_fields(self):
        # Test MetricCreate with minimal required fields
        metric = MetricCreate(
            value=1.0,
            agent_id=1,
            timestamp=datetime.now(),
            data=[]
        )
        assert metric.value == 1.0
        assert metric.agent_id == 1