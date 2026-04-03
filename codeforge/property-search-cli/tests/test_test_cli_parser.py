import sys
from unittest.mock import patch
import pytest
from src.cli_parser import parse_args


def test_parse_args_with_all_options():
    test_args = [
        'program_name',
        '--location', 'New York',
        '--min-price', '100000',
        '--max-price', '500000',
        '--bedrooms', '3',
        '--property-type', 'apartment',
        '--min-area', '1000',
        '--max-area', '2000',
        '--keywords', 'parking,garden'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.location == 'New York'
        assert args.min_price == 100000
        assert args.max_price == 500000
        assert args.bedrooms == 3
        assert args.property_type == 'apartment'
        assert args.min_area == 1000
        assert args.max_area == 2000
        assert args.keywords == ['parking', 'garden']


def test_parse_percentage_args():
    test_args = [
        'program_name',
        '--broker-fee', '5.5',
        '--down-payment', '20'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.broker_fee == 5.5
        assert args.down_payment == 20.0


def test_parse_numeric_args():
    test_args = [
        'program_name',
        '--min-price', '150000',
        '--max-price', '750000',
        '--bedrooms', '4'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.min_price == 150000
        assert args.max_price == 750000
        assert args.bedrooms == 4


def test_parse_args_with_partial_options():
    test_args = [
        'program_name',
        '--location', 'Los Angeles',
        '--property-type', 'house'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.location == 'Los Angeles'
        assert args.property_type == 'house'


def test_parse_args_with_single_keyword():
    test_args = [
        'program_name',
        '--keywords', 'garden'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.keywords == ['garden']


def test_parse_args_with_empty_keywords():
    test_args = [
        'program_name',
        '--keywords', ''
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.keywords == ['']


def test_parse_args_with_no_options():
    test_args = ['program_name']
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.location is None
        assert args.min_price is None
        assert args.max_price is None
        assert args.bedrooms is None
        assert args.property_type is None
        assert args.min_area is None
        assert args.max_area is None
        assert args.keywords is None
        assert args.broker_fee is None
        assert args.down_payment is None


def test_parse_args_with_zero_values():
    test_args = [
        'program_name',
        '--min-price', '0',
        '--max-price', '0',
        '--bedrooms', '0',
        '--broker-fee', '0.0',
        '--down-payment', '0.0'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.min_price == 0
        assert args.max_price == 0
        assert args.bedrooms == 0
        assert args.broker_fee == 0.0
        assert args.down_payment == 0.0


def test_parse_args_with_float_values():
    test_args = [
        'program_name',
        '--min-price', '150000.50',
        '--max-price', '750000.75',
        '--broker-fee', '3.75',
        '--down-payment', '15.25'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.min_price == 150000.5
        assert args.max_price == 750000.75
        assert args.broker_fee == 3.75
        assert args.down_payment == 15.25


def test_parse_args_with_negative_values():
    test_args = [
        'program_name',
        '--min-price', '-100000',
        '--max-price', '-500000',
        '--bedrooms', '-3'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.min_price == -100000
        assert args.max_price == -500000
        assert args.bedrooms == -3


def test_parse_args_with_large_values():
    test_args = [
        'program_name',
        '--min-price', '1000000000',
        '--max-price', '9999999999'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.min_price == 1000000000
        assert args.max_price == 9999999999


def test_parse_args_with_comma_separated_keywords():
    test_args = [
        'program_name',
        '--keywords', 'parking,garden,pool,garage'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.keywords == ['parking', 'garden', 'pool', 'garage']


def test_parse_args_with_single_character_keywords():
    test_args = [
        'program_name',
        '--keywords', 'a,b,c'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.keywords == ['a', 'b', 'c']


def test_parse_args_with_special_character_keywords():
    test_args = [
        'program_name',
        '--keywords', 'parking_garden,pool&spa,house-near-beach'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.keywords == ['parking_garden', 'pool&spa', 'house-near-beach']


def test_parse_args_with_no_value_flags():
    test_args = [
        'program_name',
        '--location', 'Boston'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.location == 'Boston'
        assert args.min_price is None
        assert args.max_price is None
        assert args.bedrooms is None


def test_parse_args_with_zero_bedrooms():
    test_args = [
        'program_name',
        '--bedrooms', '0'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.bedrooms == 0


def test_parse_args_with_string_bedrooms():
    test_args = [
        'program_name',
        '--bedrooms', 'studio'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.bedrooms == 'studio'


def test_parse_args_with_mixed_case_property_type():
    test_args = [
        'program_name',
        '--property-type', 'ConDo'
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.property_type == 'ConDo'


def test_parse_args_with_empty_string_location():
    test_args = [
        'program_name',
        '--location', ''
    ]
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.location == ''


def test_parse_args_with_none_values():
    test_args = ['program_name']
    
    with patch('sys.argv', test_args):
        args = parse_args()
        assert args.location is None
        assert args.min_price is None
        assert args.max_price is None
        assert args.bedrooms is None
        assert args.property_type is None
        assert args.min_area is None
        assert args.max_area is None
        assert args.keywords is None
        assert args.broker_fee is None
        assert args.down_payment is None