import sys
import logging
from typing import Dict, Any
import pandas as pd

from .data_source import DataSource
from .data_processor import DataProcessor
from .report_generator import ReportGenerator
from .utils import validate_data


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def run_analysis(source: str, output_format: str = 'json') -> Dict[str, Any]:
    """
    Run gravitational data analysis on the provided data source.
    
    Args:
        source: URL for real-time data or file path for static data
        output_format: Format for the output ('json', 'csv', 'dict')
        
    Returns:
        Dictionary containing processed data and metadata
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        data_source = DataSource()
        data_processor = DataProcessor()
        report_generator = ReportGenerator()
        
        # Handle None or empty source
        if not source:
            raise ValueError("Source parameter is required")
            
        # Determine if source is URL or file path
        if source.startswith(('http://', 'https://')):
            raw_data = data_source.fetch_real_time_data(source)
        else:
            raw_data = data_source.load_static_dataset(source)
            
        # Validate data
        if not validate_data(raw_data):
            raise ValueError("Invalid data structure received")
            
        # Process data
        if raw_data is not None and not raw_data.empty:
            processed_data = data_processor.process_gravitational_data(raw_data)
            statistics = data_processor.calculate_statistics(processed_data)
            report = report_generator.generate_report(processed_data)
        else:
            processed_data = pd.DataFrame()
            statistics = {}
            report = ""
        
        # Format output
        result = {
            "data": raw_data,
            "processed_data": processed_data.to_dict('records') if isinstance(processed_data, pd.DataFrame) and not processed_data.empty else [],
            "statistics": statistics,
            "report": report
        }
        
        # Export based on format
        if output_format.lower() == 'csv':
            report_generator.export_to_csv(processed_data, "analysis_output.csv")
            result["export_file"] = "analysis_output.csv"
        elif output_format.lower() == 'json':
            # Data is already in result
            pass
            
        logger.info("Analysis completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise


def main() -> None:
    """Main entry point for CLI usage."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if len(sys.argv) < 2:
        logger.error("Usage: gravitational_data <source> [output_format]")
        sys.exit(1)
        
    source = sys.argv[1] if len(sys.argv) > 1 else None
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'json'
    
    # Handle None or empty source
    if not source:
        logger.error("Source parameter is required")
        sys.exit(1)
    
    try:
        result = run_analysis(source, output_format)
        if output_format.lower() == 'json':
            import json
            print(json.dumps(result, indent=2))
        else:
            print(f"Analysis complete. Results: {result}")
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        sys.exit(1)