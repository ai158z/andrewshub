import pytest
from unittest.mock import patch
from src.cli_parser import parse_args
import sys


def test_parse_args_with_valid_location():
    test_args = ["--location", "New York"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.location == "New York"


def test_parse_args_with_valid_coordinates():
    test_args = ["--latitude", "40.7128", "--longitude", "-74.0060", "--radius", "10"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.latitude == 40.7128
        assert args.longitude == -74.0060
        assert args.radius == 10


def test_parse_args_with_missing_coordinate():
    test_args = ["--latitude", "40.7128", "--radius", "10"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_valid_price_range():
    test_args = ["--min-price", "100000", "--max-price", "500000"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.min_price == 100000
        assert args.max_price == 500000


def test_parse_args_with_invalid_price_range():
    test_args = ["--min-price", "500000", "--max-price", "100000"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_property_details():
    test_args = ["--beds", "3", "--baths", "2.5", "--property-type", "house"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.beds == 3
        assert args.baths == 2.5
        assert args.property_type == "house"


def test_parse_args_with_financial_filters():
    test_args = ["--down-payment", "50000", "--interest-rate", "3.5", "--loan-term", "30"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.down_payment == 50000
        assert args.interest_rate == 3.5
        assert args.loan_term == 30


def test_parse_args_with_conflicting_down_payment():
    test_args = ["--down-payment", "50000", "--down-payment-percent", "20"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_additional_filters():
    test_args = ["--hoa-max", "300", "--year-built-min", "1990", "--parking-spaces", "2"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.hoa_max == 300
        assert args.year_built_min == 1990
        assert args.parking_spaces == 2


def test_parse_args_with_sort_options():
    test_args = ["--sort-by", "price", "--sort-order", "desc", "--limit", "10"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.sort_by == "price"
        assert args.sort_order == "desc"
        assert args.limit == 10


def test_parse_args_with_default_sort_order():
    test_args = ["--sort-by", "beds"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.sort_order == "asc"


def test_parse_args_with_output_format():
    test_args = ["--output-format", "json"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.output_format == "json"


def test_parse_args_with_verbose_flag():
    test_args = ["--verbose"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.verbose is True


def test_parse_args_with_no_args():
    test_args = []
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        args = parse_args()
        assert args.location is None
        assert args.min_price is None
        assert args.max_price is None
        assert args.verbose is False


def test_parse_args_with_invalid_property_type():
    test_args = ["--property-type", "invalid"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_invalid_loan_term():
    test_args = ["--loan-term", "25"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_negative_values():
    test_args = ["--min-price", "-1000"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_invalid_percentage():
    test_args = ["--interest-rate", "150"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_invalid_float_conversion():
    test_args = ["--latitude", "not_a_number"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_with_invalid_integer_conversion():
    test_args = ["--beds", "not_a_number"]
    with patch.object(sys, 'argv', ['property-search'] + test_args):
        with pytest.raises(SystemExit):
            parse_args()