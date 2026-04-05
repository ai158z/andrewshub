import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.main import setup_logging, process_feeds, main

def test_setup_logging_configures_handlers():
    with patch('logging.basicConfig') as mock_config:
        setup_logging()
        mock_config.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
@patch('src.main.update_last_run_timestamp')
@patch('src.main.config_get_feed_urls')
@patch('src.main.db_get_feed_urls')
def test_process_feeds_with_config_feeds(mock_db_get, mock_config_get, mock_update_ts, mock_init_db, 
                                       mock_send_alert, mock_is_relevant, mock_save, mock_filter, mock_fetch):
    mock_config_get.return_value = ['http://test.com/feed']
    mock_db_get.return_value = []
    mock_fetch.return_value = [{'title': 'Test Article', 'content': 'Test content'}]
    mock_filter.return_value = [{'title': 'Test Article', 'content': 'Test content'}]
    mock_is_relevant.return_value = True
    mock_send_alert.return_value = True
    
    config = {'feeds': ['http://test.com/feed']}
    process_feeds(config)
    
    mock_init_db.assert_called_once()
    mock_fetch.assert_called_once()
    mock_filter.assert_called_once()
    mock_save.assert_called_once()
    mock_send_alert.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_no_feeds(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = []
    mock_filter.return_value = []
    mock_is_payment.return_value = False
    
    config = {}
    process_feeds(config)
    
    mock_init_db.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_empty_feeds(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = []
    mock_filter.return_value = []
    mock_is_payment.return_value = False
    
    config = {'feeds': []}
    process_feeds(config)
    
    mock_init_db.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
@patch('src.main.config_get_feed_urls')
@patch('src.main.db_get_feed_urls')
def test_process_feeds_uses_config_feeds(mock_db_get, mock_config_get, mock_init_db, mock_send_alert, 
                                       mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_config_get.return_value = ['http://config-feed.com']
    mock_db_get.return_value = []
    mock_fetch.return_value = [{'title': 'Test', 'content': 'Test content'}]
    mock_filter.return_value = [{'title': 'Test', 'content': 'Test content'}]
    mock_is_payment.return_value = False
    
    config = {}
    process_feeds(config)
    
    mock_config_get.assert_called_once()
    mock_fetch.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
@patch('src.main.config_get_feed_urls')
@patch('src.main.db_get_feed_urls')
def test_process_feeds_uses_db_feeds_when_config_empty(mock_db_get, mock_config_get, mock_init_db, mock_send_alert, 
                                                      mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_config_get.return_value = None
    mock_db_get.return_value = ['http://db-feed.com']
    mock_fetch.return_value = [{'title': 'Test', 'content': 'Test content'}]
    mock_filter.return_value = [{'title': 'Test', 'content': 'Test content'}]
    mock_is_payment.return_value = False
    
    config = {}
    process_feeds(config)
    
    mock_db_get.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_no_feeds_warning(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch, caplog):
    mock_fetch.return_value = []
    mock_filter.return_value = []
    mock_is_payment.return_value = False
    
    config = {'feeds': []}
    process_feeds(config)
    
    # Check warning was logged about no feeds
    assert any("No feed URLs found" in record.message for record in caplog.records)

@patch('src.main.load_config')
@patch('src.main.process_feeds')
@patch('src.main.update_last_run_timestamp')
def test_main_success(mock_update_ts, mock_process_feeds, mock_load_config, caplog):
    mock_load_config.return_value = {'feeds': ['http://test.com']}
    
    with patch('sys.argv', ['main.py', '--config', 'test_config.yaml']):
        main()
    
    mock_process_feeds.assert_called_once()
    mock_update_ts.assert_called_once()

@patch('src.main.load_config')
@patch('src.main.process_feeds')
@patch('src.main.update_last_run_timestamp')
def test_main_with_config_arg(mock_update_ts, mock_process_feeds, mock_load_config):
    mock_load_config.return_value = {'feeds': ['http://test.com']}
    
    with patch('sys.argv', ['main.py', '--config', 'custom_config.yaml']):
        main()
    
    mock_load_config.assert_called_once()

@patch('src.main.load_config')
@patch('src.main.process_feeds')
@patch('src.main.update_last_run_timestamp')
def test_main_logs_error_on_exception(mock_update_ts, mock_process_feeds, mock_load_config, caplog):
    mock_load_config.side_effect = Exception("Config load failed")
    
    with pytest.raises(SystemExit):
        with patch('sys.argv', ['main.py']):
            main()
    
    assert "An error occurred: Config load failed" in caplog.text

@patch('src.main.load_config')
@patch('src.main.process_feeds')
@patch('src.main.update_last_run_timestamp')
def test_main_exits_on_error(mock_update_ts, mock_process_feeds, mock_load_config, capsys):
    mock_load_config.side_effect = Exception("Test error")
    
    with pytest.raises(SystemExit):
        with patch('sys.argv', ['main.py']):
            main()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_moonpay_alert_sent(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = [{'title': 'Payment Article', 'content': 'Payment content'}]
    mock_filter.return_value = [{'title': 'Payment Article', 'content': 'Payment content'}]
    mock_is_payment.return_value = True
    mock_send_alert.return_value = True
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    mock_send_alert.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_moonpay_alert_failure(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch, caplog):
    mock_fetch.return_value = [{'title': 'Payment Article', 'content': 'Payment content'}]
    mock_filter.return_value = [{'title': 'Payment Article', 'content': 'Payment content'}]
    mock_is_payment.return_value = True
    mock_send_alert.return_value = False
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    assert any("Failed to send MoonPay alert" in record.message for record in caplog.records)

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_no_moonpay_alert(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = [{'title': 'Regular Article', 'content': 'Regular content'}]
    mock_filter.return_value = [{'title': 'Regular Article', 'content': 'Regular content'}]
    mock_is_payment.return_value = False
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    mock_send_alert.assert_not_called()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_saves_articles(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    articles = [{'title': 'Test Article', 'content': 'Test content'}]
    mock_fetch.return_value = articles
    mock_filter.return_value = articles
    mock_is_payment.return_value = False
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    mock_save.assert_called_once_with(articles, 'sqlite:///data.db')

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_filters_articles(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    articles = [{'title': 'BTC Article', 'content': 'Bitcoin content'}]
    mock_fetch.return_value = articles
    mock_filter.return_value = articles
    mock_is_payment.return_value = False
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    mock_filter.assert_called_once_with(articles)

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_empty_config_feeds(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = []
    mock_filter.return_value = []
    mock_is_payment.return_value = False
    
    config = {}
    process_feeds(config)
    
    mock_init_db.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_empty_db_feeds(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = []
    mock_filter.return_value = []
    mock_is_payment.return_value = False
    
    config = {}
    with patch('src.main.config_get_feed_urls') as mock_config_get, \
         patch('src.main.db_get_feed_urls') as mock_db_get:
        mock_config_get.return_value = None
        mock_db_get.return_value = None
        process_feeds(config)
        mock_db_get.assert_called_once()

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_fetch_all_feeds_called(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = [{'title': 'Fetched Article', 'content': 'Content'}]
    mock_filter.return_value = [{'title': 'Fetched Article', 'content': 'Content'}]
    mock_is_payment.return_value = False
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    mock_fetch.assert_called_once_with(['http://test.com'])

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_save_articles_called(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    articles = [{'title': 'Test', 'content': 'Test content'}]
    mock_fetch.return_value = articles
    mock_filter.return_value = articles
    mock_is_payment.return_value = False
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    mock_save.assert_called_once_with(articles, 'sqlite:///data.db')

@patch('src.main.fetch_all_feeds')
@patch('src.main.filter_articles')
@patch('src.main.save_articles')
@patch('src.main.is_payment_relevant')
@patch('src.main.send_alert')
@patch('src.main.initialize_db')
def test_process_feeds_no_articles(mock_init_db, mock_send_alert, mock_is_payment, mock_save, mock_filter, mock_fetch):
    mock_fetch.return_value = []
    mock_filter.return_value = []
    mock_is_payment.return_value = False
    
    config = {'feeds': ['http://test.com']}
    process_feeds(config)
    
    mock_send_alert.assert_not_called()