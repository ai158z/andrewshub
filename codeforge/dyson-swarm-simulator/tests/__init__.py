import unittest
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_tests(loader, tests, pattern):
    """Load all tests from the test modules"""
    # Discover and add tests from test_calculations.py
    calc_suite = loader.discover(start_dir='tests', pattern='test_calculations.py')
    # Discover and add tests from test_models.py
    model_suite = loader.discover(start_dir='tests', pattern='test_models.py')

    # Add all test suites to the main test suite
    suite = unittest.TestSuite()
    suite.addTests(calc_suite)
    suite.addTests(model_suite)
    return suite

if __name__ == '__main__':
    # Run all tests when this module is executed directly
    # Create a test suite and run it
    loader = unittest.TestLoader()
    suite = load_tests(loader, None, 'test*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)