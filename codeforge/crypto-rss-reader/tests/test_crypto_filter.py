import pytest
from src.crypto_filter import is_crypto_related, filter_articles

def test_is_crypto_related_with_valid_crypto_article():
    article = {
        'title': 'Bitcoin Price Surges as Ethereum Announces New Features',
        'summary': 'The cryptocurrency market is experiencing a massive surge with Bitcoin reaching new highs'
    }
    assert is_crypto_related(article) == True

def test_is_crypto_related_with_non_crypto_article():
    article = {
        'title': 'Local Sports Team Wins Championship',
        'summary': 'The home team defeated their rivals in a thrilling match'
    }
    assert is_crypto_related(article) == False

def test_is_crypto_related_with_payment_terms_in_crypto_context():
    article = {
        'title': 'How to Buy Bitcoin',
        'summary': 'A guide to purchasing cryptocurrency using various payment methods including credit card and bank transfer'
    }
    assert is_crypto_related(article) == True

def test_is_crypto_related_with_payment_terms_no_crypto_context():
    article = {
        'title': 'New Payment Options for Online Shopping',
        'summary': 'Exploring modern payment methods for e-commerce'
    }
    assert is_crypto_related(article) == True

def test_is_crypto_related_invalid_input_type():
    assert is_crypto_related("not a dict") == False

def test_is_crypto_related_missing_fields():
    article = {
        'author': 'John Doe'
    }
    assert is_crypto_related(article) == False

def test_is_crypto_related_non_string_fields():
    article = {
        'title': 123,
        'summary': ['summary in a list']
    }
    assert is_crypto_related(article) == False

def test_is_crypto_related_case_insensitive():
    article = {
        'title': 'BITCOIN and ETHEREUM are booming',
        'summary': 'CRYPTO markets are rising'
    }
    assert is_crypto_related(article) == True

def test_filter_articles_valid_input():
    articles = [
        {'title': 'Bitcoin News', 'summary': 'Latest updates on cryptocurrency'},
        {'title': 'Sports Today', 'summary': 'Local team wins'},
        {'title': 'Ethereum Upgrade', 'summary': 'Major blockchain improvements'}
    ]
    result = filter_articles(articles)
    assert len(result) == 2
    assert result[0] == {'title': 'Bitcoin News', 'summary': 'Latest updates on cryptocurrency'}
    assert result[1] == {'title': 'Ethereum Upgrade', 'summary': 'Major blockchain improvements'}

def test_filter_articles_empty_list():
    assert filter_articles([]) == []

def test_filter_articles_invalid_input_type():
    assert filter_articles("not a list") == []

def test_filter_articles_with_invalid_article_format():
    articles = [
        {'title': 'Valid Crypto Article', 'summary': 'This is about Bitcoin'},
        'not a dict',
        {'title': 'Another Valid Article', 'summary': 'Ethereum news today'}
    ]
    result = filter_articles(articles)
    assert len(result) == 2
    assert result[0] == {'title': 'Valid Crypto Article', 'summary': 'This is about Bitcoin'}
    assert result[1] == {'title': 'Another Valid Article', 'summary': 'Ethereum news today'}

def test_filter_articles_none_input():
    assert filter_articles(None) == []

def test_is_crypto_related_with_crypto_exchange_names():
    article = {
        'title': 'Coinbase Announces New Features',
        'summary': 'Major crypto exchange updates its platform'
    }
    assert is_crypto_related(article) == True

def test_is_crypto_related_edge_case_empty_strings():
    article = {
        'title': '',
        'summary': ''
    }
    assert is_crypto_related(article) == False

def test_is_crypto_related_edge_case_none_values():
    article = {
        'title': None,
        'summary': None
    }
    assert is_crypto_related(article) == False

def test_is_crypto_related_with_trading_terms():
    article = {
        'title': 'How to Trade Cryptocurrency',
        'summary': 'A complete guide to trading Bitcoin and other digital assets'
    }
    assert is_crypto_related(article) == True

def test_is_crypto_related_with_defi_terms():
    article = {
        'title': 'Understanding DeFi and Smart Contracts',
        'summary': 'Decentralized finance is revolutionizing traditional finance'
    }
    assert is_crypto_related(article) == True

def test_filter_articles_mixed_content():
    articles = [
        {'title': '', 'summary': 'Regular content'},
        {'title': 'NFT Art Collection', 'summary': 'Digital art on the blockchain'},
        123,  # Invalid entry
        {'title': 'Stock Market Update', 'summary': 'Traditional markets rise today'},
        {'title': 'Ethereum Price Analysis', 'summary': 'Market analysis of ETH performance'}
    ]
    result = filter_articles(articles)
    assert len(result) == 2
    assert result[0] == {'title': 'NFT Art Collection', 'summary': 'Digital art on the blockchain'}
    assert result[1] == {'title': 'Ethereum Price Analysis', 'summary': 'Market analysis of ETH performance'}