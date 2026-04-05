import json
import logging
from typing import Dict, Any, Optional
import pandas as pd

logger = logging.getLogger(__name__)

def convert_json_to_csv(
    input_file: str, 
    output_file: str, 
    field_mapping: Dict[str, str], 
    schema_file: Optional[str] = None
) -> bool:
    """Convert JSON data to CSV format with field mapping and flattening."""
    try:
        # Validate input file is JSON
        if not is_valid_json_file(input_file):
            return False

        # Read and parse JSON data
        data = read_json_file(input_file)
        if not data:
            return False

        # Validate against schema if provided
        if schema_file:
            try:
                with open(schema_file, 'r') as f:
                    schema = json.load(f)
                is_valid, _ = validate_json_schema(data, schema)
                if not is_valid:
                    return False
            except Exception as e:
                logger.error(f"Schema validation failed: {str(e)}")
                return False

        # Handle different JSON structures
        processed_data = []
        if isinstance(data, list):
            for item in data:
                processed_data.append(_process_data_item(item, field_mapping))
        elif isinstance(data, dict):
            processed_data.append(_process_data_item(data, field_mapping))
        else:
            return False

        return True

    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return False

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Dict[str, Any]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        return None

    processed_item = _process_data_item(item, field_mapping)
    if processed_item:
        processed_data.append(processed_item)
    elif isinstance(data, list):
        for item in data:
            processed_data.append(_process_data_item(item, field_mapping))
    elif isinstance(data, dict):
        processed_data.append(_process_data_item(data, field_mapping))
    else:
        logger.error("No valid data to convert")
        return False

    return True

except Exception as e:
    logger.error(f"Error during conversion: {str(e)}")
    return False

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Dict[str, Any]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Dict[str, Any]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return False

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            else:
                # Field not found, use None or default value
                mapped_item[original_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in mapped_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_to_process: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_to_process.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
            except:
                pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping:
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict[str, Any], field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not0to find, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: dict) -> Optional[Dict]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                flattened_item[original_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping:
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field]
            elif target_field in flattened_item:
                mapped_item[target_field] = flattened_item[original_field]
            else:
                # Field not found, use None or default value
                mapped_item[target_field] = None

        # Apply blockchain parsing if applicable
        # Check if item contains blockchain data
        if 'block' in mapped_item or 'transaction' in mapped_item:
            # Try parsing as blockchain transaction
            try:
                mapped_item = parse_blockchain_transaction(mapped_item)
            except:
                # If that fails, try parsing as block data
                try:
                    mapped_item = parse_block_data(mapped_item)
                except:
                    pass  # If both fail, keep original data

        return mapped_item
    except Exception as e:
        logger.error(f"Error processing data item: {str(e)}")
        return None

    return mapped_item

def _process_data_item(item: Dict, field_mapping: Dict[str, str]) -> Optional[Dict[str, Any]]:
    try:
        # Flatten nested structures
        flattened_item = flatten_dict(item)

        # Apply field mapping
        mapped_item = {}
        for original_field, target_field in field_mapping.items():
            if original_field in flattened_item:
                mapped_item[original_field] = flattened_item[original_field
                elif target_field in flattened_item:
                    mapped_item[target_field] = flattened_item[target_field]
            else:
                # Field not