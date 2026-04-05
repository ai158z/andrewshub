from flask import Blueprint, request, jsonify
from decimal import Decimal, InvalidOperation
from src.calculator import calculate_rewards
import logging

logger = logging.getLogger(__name__)
api = Blueprint('api', __name__)

def validate_input(data):
    """Validate input data for staking calculation"""
    required_fields = ['principal', 'apr', 'duration']
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
        if not isinstance(data[field], (int, float, str)):
            return False
    try:
        principal = Decimal(str(data['principal']))
        apr = float(data['apr'])
        duration = int(data['duration'])
    except (InvalidOperation, ValueError, TypeError):
        return False
    return True

def register_routes(app):
    app.register_blueprint(api, url_prefix='/api')

@api.route('/calculate', methods=['POST'])
def calculate():
    if not request.json:
        return jsonify({'error': 'Invalid input format'}), 400

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        principal = Decimal(str(data.get('principal', 0)))
        apr = Decimal(str(data.get('apr', 0)))
        duration = int(data.get('duration', 0))
    except (ValueError, InvalidOperation) as e:
        return jsonify({'error': 'Invalid input values'}), 400

    try:
        result = calculate_rewards(principal, apr, duration)
        return jsonify({'rewards': float(result)}), 200
    except (InvalidOperation, ValueError, KeyError) as e:
        return jsonify({'error': 'Invalid calculation parameters'}), 500
    except Exception as e:
        return jsonify({'error': 'Calculation error'}), 500