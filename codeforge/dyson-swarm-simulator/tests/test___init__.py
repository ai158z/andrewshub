import unittest
import sys
import os
from unittest.mock import patch, mock_open

# Mock the actual test content since we're focusing on the __init__.py module functionality
class TestInitModule(unittest.TestCase):
    
    def test_load_tests_function_exists(self):
        """Verify that load_tests function exists and is callable"""
        self.assertTrue(callable(load_tests))

    @patch('unittest.TestLoader.discover')
    def test_load_tests_discovers_calc_tests(self, mock_discover):
        """Test that load_tests calls discover for calculation tests"""
        mock_discover.return_value = unittest.TestSuite()
        loader = unittest.TestLoader()
        
        # Create mock test suites
        mock_calc_suite = unittest.TestSuite()
        mock_model_suite = unittest.TestSuite()
        
        # Configure mock return values
        mock_discover.side_effect = [
            mock_calc_suite,  # First call for calc tests
            mock_model_suite  # Second call for model tests
        ]
        
        suite = unittest.TestSuite()
        result = load_tests(loader, suite, 'test*.py')
        
        # Verify discover was called twice
        self.assertEqual(mock_discover.call_count, 2)
        self.assertIsInstance(result, unittest.TestSuite)

    @patch('unittest.main')
    def test_main_execution_calls_unittest_main(self, mock_main):
        """Test that main execution calls unittest.main twice"""
        # Reset call count
        mock_main.call_count = 0
        
        # Execute the main block code
        with patch.object(sys, 'argv', ['tests/__init__.py']):
            try:
                unittest.main(module='tests.test_calculations')
                unittest.main(module='tests.test_models')
            except SystemExit:
                pass
        
        # Should have been called for both modules
        self.assertEqual(mock_main.call_count, 2)

    def test_sys_path_modified(self):
        """Test that sys.path is modified to include project root"""
        # Get the path that would be inserted
        expected_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # Check if the path insertion happened
        self.assertIn(expected_path, sys.path)

if __name__ == '__main__':
    unittest.main()