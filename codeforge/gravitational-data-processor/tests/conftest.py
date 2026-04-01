import pytest
import pandas as pd
import logging
from typing import Dict, Any
from src.gravitational_data.data_source import DataSource
from src.gravitational_data.data_processor import DataProcessor
from src.gravitational_data.report_generator import ReportGenerator


class MockDataSource(DataSource):
    def fetch_real_time_data(self, url: str) -> Dict[Any, Any]:
        return {"test": "data"}

    def load_static_dataset(self, file_path: str) -> Dict[Any, Any]:
        return {"test": "data"}


class MockDataProcessor(DataProcessor):
    def process_gravitational_data(self, data: dict) -> pd.DataFrame:
        return pd.DataFrame([data])

    def calculate_statistics(self, data: pd.DataFrame) -> dict:
        return {"stat": "test"}


class MockReportGenerator(ReportGenerator):
    def generate_report(self, data: pd.DataFrame) -> str:
        return "test_report"

    def export_to_csv(self, data: pd.DataFrame, filename: str) -> None:
        pass


@pytest.fixture
def mock_data_source():
    return MockDataSource()


@pytest.fixture
def mock_data_processor():
    return MockDataProcessor()


@pytest.fixture
def mock_report_generator():
    return MockReportGenerator()


@pytest.fixture
def sample_gravitational_data():
    return {
        "timestamp": "2023-01-01T00:00:00Z",
        "measurements": [
            {"x": 1.0, "y": 2.0, "z": 3.0},
            {"x": 4.0, "y": 5.0, "z": 6.0}
        ]
    }


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


def pytest_runtest_makereport(item, call):
    if call.when == "teardown":
        logging.info(f"Test {item.name} finished with outcome: {call.excinfo}")


@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(level=logging.INFO)