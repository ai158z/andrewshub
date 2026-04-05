import pytest
from unittest.mock import patch, MagicMock
from src.cli import main

def test_main_with_valid_url_and_feed(mock_click, mock_logging):
    with patch("src.cli.is_valid_url", return_value=True) as mock_valid_url:
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>") as mock_fetch:
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[])) as mock_parse:
                with patch("src.cli.click.echo") as mock_echo:
                    main(  # type: ignore
                        url="http://example.com/rss",
                        timeout=10,
                        summary_ratio=0.3,
                        max_entries=10,
                        no_summary=False
                    )
                    mock_valid_url.assert_called_once_with("http://example.com/rss")
                    mock_fetch.assert_called_once_with("http://example.com/rss", 10)
                    mock_parse.assert_called_once()
                    mock_echo.assert_any_call("Feed Title: Test Feed")

def test_main_with_invalid_url(mock_click, mock_logging):
    with patch("src.cli.is_valid_url", return_value=False) as mock_valid_url:
        with patch("src.cli.click.echo") as mock_echo:
            main(  # type: ignore
                url="invalid-url",
                timeout=10,
                summary_ratio=0.3,
                max_entries=10,
                no_summary=False
            )
            mock_valid_url.assert_called_once_with("invalid-url")
            mock_echo.assert_not_called()

def test_main_fetch_feed_failure(mock_click, mock_logging):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value=None) as mock_fetch:
            with patch("src.cli.click.echo") as mock_echo:
                main(  # type: ignore
                    url="http://example.com/rss",
                    timeout=10,
                    summary_ratio=0.3,
                    max_entries=10,
                    no_summary=False
                )
                mock_fetch.assert_called_once_with("http://example.com/rss", 10)
                mock_echo.assert_not_called()

def test_main_no_summary_flag(mock_click):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>"):
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[
                MagicMock(title="Entry 1", published="2023-01-01", link="http://example.com/entry1", content="Content 1", description=None)
            ])):
                with patch("src.cli.summarize_text") as mock_summarize:
                    with patch("src.cli.click.echo") as mock_echo:
                        main(  # type: ignore
                            url="http://example.com/rss",
                            timeout=10,
                            summary_ratio=0.3,
                            max_entries=10,
                            no_summary=True
                        )
                        mock_summarize.assert_not_called()
                        mock_echo.assert_any_call("Content: Content 1")

def test_main_with_summary(mock_click):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>"):
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[
                MagicMock(title="Entry 1", published="2023-01-01", link="http://example.com/entry1", content="Content 1", description=None)
            ])):
                with patch("src.cli.summarize_text", return_value="Summarized content") as mock_summarize:
                    with patch("src.cli.click.echo") as mock_echo:
                        main(  # type: ignore
                            url="http://example.com/rss",
                            timeout=10,
                            summary_ratio=0.3,
                            max_entries=10,
                            no_summary=False
                        )
                        mock_summarize.assert_called_once_with("Content 1", 0.3)
                        mock_echo.assert_any_call("Summary: Summarized content")

def test_main_max_entries_limit(mock_click):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>"):
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[
                MagicMock(title="Entry 1", published="2023-01-01", link="http://example.com/entry1", content="Content 1", description=None),
                MagicMock(title="Entry 2", published="2023-01-02", link="http://example.com/entry2", content="Content 2", description=None)
            ])):
                with patch("src.cli.click.echo") as mock_echo:
                    main(  # type: ignore
                        url="http://example.com/rss",
                        timeout=10,
                        summary_ratio=0.3,
                        max_entries=1,
                        no_summary=False
                    )
                    # Verify only one entry is processed
                    calls = [call for call in mock_echo.call_args_list if "Entry #" in str(call)]
                    assert len(calls) == 1

def test_main_exception_handling(mock_click, mock_logging):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", side_effect=Exception("Network error")):
            with patch("src.cli.click.echo") as mock_echo:
                with pytest.raises(Exception, match="Network error"):
                    main(  # type: ignore
                        url="http://example.com/rss",
                        timeout=10,
                        summary_ratio=0.3,
                        max_entries=10,
                        no_summary=False
                    )
                    mock_echo.assert_any_call("An error occurred: Network error")

def test_main_empty_feed(mock_click):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>"):
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[])):
                with patch("src.cli.click.echo") as mock_echo:
                    main(  # type: ignore
                        url="http://example.com/rss",
                        timeout=10,
                        summary_ratio=0.3,
                        max_entries=10,
                        no_summary=False
                    )
                    mock_echo.assert_any_call("Feed Title: Test Feed")
                    mock_echo.assert_any_call("Feed Description: A test feed")

def test_main_feed_with_no_content_uses_description(mock_click):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>"):
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[
                MagicMock(title="Entry 1", published="2023-01-01", link="http://example.com/entry1", content=None, description="Description content")
            ])):
                with patch("src.cli.summarize_text", return_value="Summarized description") as mock_summarize:
                    with patch("src.cli.click.echo") as mock_echo:
                        main(  # type: ignore
                            url="http://example.com/rss",
                            timeout=10,
                            summary_ratio=0.3,
                            max_entries=10,
                            no_summary=False
                        )
                        mock_summarize.assert_called_once_with("Description content", 0.3)
                        mock_echo.assert_any_call("Summary: Summarized description")

def test_main_feed_no_content_no_description(mock_click):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>"):
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[
                MagicMock(title="Entry 1", published="2023-01-01", link="http://example.com/entry1", content=None, description=None)
            ])):
                with patch("src.cli.summarize_text", return_value="No content available") as mock_summarize:
                    with patch("src.cli.click.echo") as mock_echo:
                        main(  # type: ignore
                            url="http://example.com/rss",
                            timeout=10,
                            summary_ratio=0.3,
                            max_entries=10,
                            no_summary=False
                        )
                        mock_summarize.assert_called_once_with("No content available", 0.3)
                        mock_echo.assert_any_call("Summary: No content available")

def test_main_feed_entry_content_and_description_none(mock_click):
    with patch("src.cli.is_valid_url", return_value=True):
        with patch("src.cli.fetch_feed", return_value="<xml>feed content</xml>"):
            with patch("src.cli.parse_feed", return_value=MagicMock(title="Test Feed", description="A test feed", entries=[
                MagicMock(title="Entry 1", published="2023-01-01", link="http://example.com/entry1", content=None, description=None)
            ])):
                with patch("src.cli.summarize_text", return_value="No content available"):
                    with patch("src.cli.click.echo") as mock_echo:
                        main(  # type: ignore
                            url="http://example.com/rss",
                            timeout=10,
                            summary_ratio=0.3,
                            max_entries=10,
                            no_summary=False
                        )
                        mock_echo.assert_any_call("Summary: No content available")

@pytest.fixture
def mock_click():
    with patch("src.cli.click.prompt", return_value="http://example.com/rss") as mock_prompt:
        yield mock_prompt

@pytest.fixture
def mock_logging():
    with patch("src.cli.logging") as mock_log:
        yield mock_log

# Mock external dependencies for all tests
@pytest.fixture(autouse=True)
def mock_external_dependencies():
    with patch("src.cli.is_valid_url"), \
         patch("src.cli.fetch_feed"), \
         patch("src.cli.parse_feed"), \
         patch("src.cli.summarize_text"), \
         patch("src.cli.sanitize_text"):
        yield