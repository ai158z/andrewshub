import pytest
from gravitational_data import DataSource, DataProcessor, ReportGenerator, __version__, __all__


def test_package_version():
    """Test that the package version is correctly exposed"""
    assert __version__ == '0.1.0'


def test_package_exposes_correct_api():
    """Test that the package exposes the correct public API"""
    expected = ['DataSource', 'DataProcessor', 'ReportGenerator']
    assert __all__ == expected


def test_datasource_class_importable():
    """Test that DataSource class is importable from package"""
    assert DataSource is not None


def test_dataprocessor_class_importable():
    """Test that DataProcessor class is importable from package"""
    assert DataProcessor is not None


def test_reportgenerator_class_importable():
    """Test that ReportGenerator class is importable from package"""
    assert ReportGenerator is not None


def test_package_imports_all_classes():
    """Test that all expected classes are imported at package level"""
    from gravitational_data import DataSource, DataProcessor, ReportGenerator
    assert DataSource is not None
    assert DataProcessor is not None
    assert ReportGenerator is not None


def test_version_attribute_exists():
    """Test that version attribute exists"""
    assert hasattr(__version__, '__str__')


def test_all_attribute_exists():
    """Test that __all__ attribute exists and contains expected items"""
    assert isinstance(__all__, list)
    assert len(__all__) == 3
    assert 'DataSource' in __all__
    assert 'DataProcessor' in __all__
    assert 'ReportGenerator' in __all__


def test_version_is_string():
    """Test that version is a string"""
    assert isinstance(__version__, str)


def test_all_is_list():
    """Test that __all__ is a list"""
    assert isinstance(__all__, list)


def test_no_duplicate_entries_in_all():
    """Test that there are no duplicate entries in __all__"""
    assert len(__all__) == len(set(__all__))


def test_expected_classes_in_all():
    """Test that all expected classes are in __all__"""
    expected_items = ['DataSource', 'DataProcessor', 'ReportGenerator']
    assert __all__ == expected_items


def test_version_format():
    """Test that version follows semantic versioning format"""
    import re
    assert re.match(r'^\d+\.\d+\.\d+$', __version__)


def test_all_contains_only_strings():
    """Test that __all__ contains only string entries"""
    assert all(isinstance(item, str) for item in __all__)


def test_all_no_extra_items():
    """Test that __all__ doesn't contain unexpected items"""
    expected = ['DataSource', 'DataProcessor', 'ReportGenerator']
    assert __all__ == expected


def test_all_items_are_exportable():
    """Test that all items in __all__ can be imported"""
    from gravitational_data import __all__ as all_items
    assert 'DataSource' in all_items
    assert 'DataProcessor' in all_items
    assert 'ReportGenerator' in all_items


def test_version_not_empty():
    """Test that version is not empty"""
    assert __version__ != ''


def test_all_not_empty():
    """Test that __all__ is not empty"""
    assert len(__all__) > 0


def test_all_has_three_items():
    """Test that __all__ contains exactly three items"""
    assert len(__all__) == 3


def test_package_imports_do_not_raise():
    """Test that importing the package doesn't raise exceptions"""
    from gravitational_data import DataSource, DataProcessor, ReportGenerator, __version__
    assert True  # Import succeeded if no exception was raised