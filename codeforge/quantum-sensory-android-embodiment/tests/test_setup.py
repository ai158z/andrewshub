import os
import pytest
from unittest.mock import mock_open, patch, MagicMock
from setup import read_requirements, read_requirements_from_file

class TestReadRequirements:
    @patch("os.path.exists")
    def test_read_requirements_with_existing_file(self, mock_exists):
        mock_exists.return_value = True
        with patch("builtins.open", mock_open(read_data="requests>=2.25.0\nnumpy==1.21.0")) as mock_file:
            requirements = read_requirements()
            assert requirements == ["requests>=2.25.0", "numpy==1.21.0"]

    @patch("os.path.exists")
    def test_read_requirements_no_file(self, mock_exists):
        mock_exists.return_value = False
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            requirements = read_requirements()
            assert requirements == []

    @patch("os.path.exists")
    def test_read_requirements_empty_file(self, mock_exists):
        mock_exists.return_value = True
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            requirements = read_requirements()
            assert requirements == []

    def test_read_requirements_from_file_with_comments_and_empty_lines(self):
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="# comment\n\nrequests>=2.25.0")) as mock_file:
                requirements = read_requirements_from_file()
                assert requirements == ["requests>=2.25.0"]

    def test_read_requirements_from_file_with_existing_file(self):
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="pandas>=1.3.0")) as mock_file:
                requirements = read_requirements_from_file()
                assert requirements == ["pandas>=1.3.0"]

    def test_read_requirements_from_file_no_file(self):
        with patch("os.path.exists", return_value=False):
            requirements = read_requirements_from_file()
            assert requirements == []

    def test_read_requirements_from_file_with_mixed_content(self):
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data="# comment\nrequests>=2.25.0\n\n# another comment\nnumpy==1.21.0")) as mock_file:
                requirements = read_requirements_from_file()
                assert requirements == ["requests>=2.25.0", "numpy==1.21.0"]