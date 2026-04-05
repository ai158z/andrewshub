import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import Dict
import logging

logger = logging.getLogger(__name__)

def plot_rewards_over_time(rewards_data: Dict) -> 'matplotlib.figure.Figure':
    """
    Generate a visualization of reward projections over time.
    
    Args:
        rewards_data: Dictionary containing reward projection data with 'dates' key
                     containing date string keys with reward values
    
    Returns:
        matplotlib.figure.Figure: The generated figure object
    """
    try:
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Extract and parse date-value pairs
        dates = []
        values = []
        
        # Get the dates data from rewards_data
        dates_data = rewards_data.get('dates', {})
        
        # Handle case where we have nested projection data
        if isinstance(dates_data, dict) and 'projections' in dates_data:
            projection_data = dates_data['projections']
            for date_str, value in projection_data.items():
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    dates.append(date_obj)
                    values.append(value)
                except ValueError:
                    logger.warning(f"Invalid date format: {date_str}")
                    continue
        else:
            # Handle direct date-value mapping
            for date_str, value in dates_data.items():
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    dates.append(date_obj)
                    values.append(value)
                except ValueError:
                    logger.warning(f"Invalid date format: {date_str}")
                    continue

        # Check if we have data to plot
        if not dates or not values:
            logger.warning("No valid data to plot")
            return fig

        # Sort data by dates
        sorted_data = sorted(zip(dates, values))
        if sorted_data:
            x_dates, y_values = zip(*sorted_data)
            
            # Create the plot
            ax.plot(x_dates, y_values, 'o-', linewidth=2, markersize=4)
            ax.set_xlabel('Time')
            ax.set_ylabel('Rewards')
            ax.set_title('Rewards Over Time')
            
            # Format x-axis dates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate()
        
        return fig
        
    except Exception as e:
        logger.error(f"Error generating plot: {str(e)}")
        # Return empty figure in case of error
        fig, ax = plt.subplots(figsize=(12, 8))
        return fig