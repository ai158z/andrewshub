import os
import sys
from unittest.mock import mock_open, patch

import pytest
from setuptools import find_packages


def test_package_has_correct_name():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        assert kwargs['name'] == 'staking-reward-calculator'


def test_package_has_correct_version():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        assert kwargs['version'] == '1.0.0'


def test_package_has_correct_description():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        assert kwargs['description'] == 'A library for calculating staking rewards with compound interest and penalty calculations'


def test_long_description_from_readme_file():
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="# Staking Reward Calculator\nThis is a calculator for staking rewards.")) as mock_file:
            import setup
            args, kwargs = mock_setup.call_args
            assert 'Staking Reward Calculator' in kwargs['long_description']
            mock_file.assert_called_once_with('README.md')


def test_long_description_fallback_when_file_unreadable():
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            mock_file().readable.return_value = False
            import setup
            args, kwargs = mock_setup.call_args
            assert kwargs['long_description'] == 'Staking reward calculator with compound interest'


def test_has_correct_author():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        assert kwargs['author'] == 'Staking Rewards Team'


def test_has_correct_author_email():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        assert kwargs['author_email'] == 'contact@stakingrewards.example.com'


def test_has_correct_license():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        assert kwargs['license'] == 'MIT'


def test_packages_found_using_find_packages():
    with patch("setuptools.setup") as mock_setup:
        with patch("setuptools.find_packages", return_value=['staking_calculator']) as mock_find:
            import setup
            args, kwargs = mock_setup.call_args
            mock_find.assert_called_with(exclude=['tests'])
            assert kwargs['packages'] == ['staking_calculator']


def test_install_requires_contains_required_packages():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        required = kwargs['install_requires']
        assert 'dataclasses' in required
        assert 'typing' in required
        assert 'decimal' in required


def test_python_requires_minimum_version():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        assert kwargs['python_requires'] == '>=3.7'


def test_contains_development_status_classifier():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        classifiers = kwargs['classifiers']
        assert 'Development Status :: 5 - Production/Stable' in classifiers


def test_contains_python_version_classifiers():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        classifiers = kwargs['classifiers']
        assert 'Programming Language :: Python :: 3.7' in classifiers
        assert 'Programming Language :: Python :: 3.11' in classifiers


def test_contains_topic_classifier():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        classifiers = kwargs['classifiers']
        assert 'Topic :: Software Development :: Libraries :: Python Modules' in classifiers


def test_has_correct_keywords():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        keywords = kwargs['keywords']
        assert 'staking' in keywords
        assert 'compound interest' in keywords
        assert 'cryptocurrency' in keywords


def test_has_project_urls():
    with patch("setuptools.setup") as mock_setup:
        import setup
        args, kwargs = mock_setup.call_args
        urls = kwargs['project_urls']
        assert 'Documentation' in urls
        assert 'Source' in urls
        assert 'Tracker' in urls
        assert all('github.com/staking-rewards/staking-reward-calculator' in url for url in urls.values())


def test_readme_file_is_opened():
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            import setup
            mock_file.assert_called_once_with('README.md')


def test_setup_does_not_crash_with_empty_readme():
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            mock_file().readable.return_value = True
            import setup  # Should not raise


def test_setup_does_not_crash_when_readme_missing():
    with patch("setuptools.setup") as mock_setup:
        with patch("builtins.open", side_effect=FileNotFoundError()):
            import setup  # Should not raise


def test_setup_function_called_once():
    with patch("setuptools.setup") as mock_setup:
        import setup
        mock_setup.assert_called_once()