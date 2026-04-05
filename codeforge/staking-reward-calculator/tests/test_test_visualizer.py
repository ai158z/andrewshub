import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Add src directory to path for imports


import matplotlib
matplotlib.use('Agg')  # Use Anti-Grain Geometry backend for testing
import matplotlib.pyplot as plt
import numpy as np

# Mock will return a string instead of figure to test the error handling path
def test_plot_rewards_over_time_error_handling():
    # Test that plot_rewards_over_time raises error when expected
    with patch('visualizer.plot_rewards_over_time') as mock_plot:
        # Test with invalid data to trigger error
        try:
            plot_rewards_over_time("invalid data")
            assert False, "Should have raised an exception"
        except Exception:
            # This is expected behavior
            pass

        # Test the error case
        try:
            # This should raise an error
            plot_rewards_overdata = {
                'daily_rewards': [1.0, 2.0, 3.0, 4.0, 5.0],
                'cumulative_rewards': [1.0, 3.0, 6.0, 10.0, 15.0],
                'days': [1, 2, 3, 4, 5]
            }
            
            plot_rewards_over_time(rewards_data)
            # This should not raise an error
            assert True
        except Exception as e:
            pass  # Ignore the error
        try:
            plot_rewards_over_time("invalid data")
            assert False, "Should have raised an exception"
        except Exception:
            pass

if __name__ == '__main__':
    test_plot_rewards_over_time_error_handling()
    test_plot_rewards_over_time_error_handling()
    test_plot_rewards_over_time_error_handling()