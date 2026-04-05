import pytest
from unittest.mock import Mock, patch, MagicMock
from github import GithubException
from src.services.github_service import GitHubService
import logging

# Test initialization with valid token
def test_github_service_initialization():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        assert service.github_token == 'fake_token'

# Test initialization without token raises error
def test_github_service_no_token_raises_error():
    with patch('os.getenv', return_value=None):
        with pytest.raises(ValueError, match="GitHub token is required"):
            GitHubService()

# Test token validation success
def test_validate_token_success():
    mock_user = Mock()
    mock_user.login = "testuser"
    
    with patch('os.getenv', return_value='fake_token'):
        with patch.object(GithubService, '_validate_token') as mock_validate:
            service = GitHubService()
            service.github = Mock()
            service.github.get_user.return_value = mock_user
            service._validate_token()
            mock_validate.assert_called_once()

# Test token validation failure
def test_validate_token_invalid():
    with patch('os.getenv', return_value='fake_token'):
        with patch('github.Github') as mock_github:
            mock_github_instance = mock_github.return_value
            mock_github_instance.get_user.side_effect = GithubException(Mock(), 401, {})
            with pytest.raises(ValueError, match="Invalid GitHub token"):
                service = GitHubService()
                service.github = mock_github_instance
                service._validate_token()

# Test get_repository success
def test_get_repository_success():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        mock_repo = Mock()
        service.github.get_repo.return_value = mock_repo
        
        repo = service.get_repository("owner", "repo")
        assert repo == mock_repo

# Test get_file_content success
def test_get_file_content_success():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        # Mock the internal GitHub API calls
        mock_repo = Mock()
        mock_content = Mock()
        mock_content.decoded_content.decode.return_value = "file content"
        service.github.get_repo.return_value.get_contents.return_value = mock_content
        
        content = service.get_file_content("https://github.com/owner/repo", "path/file.txt")
        assert content == "file content"

# Test get_file_content_http_url_parsing():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        result = service.parse_repo_url("https://github.com/owner/repo.git")
        assert result == ("owner", "repo")

# Test invalid repository URL format
def test_parse_repo_url_invalid():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        with pytest.raises(ValueError, match="Invalid repository URL format"):
            service.parse_repo_url("invalid-url")

# Test get_pull_request_files
def test_get_pull_request_files():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_pr = Mock()
        mock_file = Mock()
        mock_file.filename = "test.py"
        mock_file.status = "modified"
        mock_file.additions = 1
        mock_file.deletions = 0
        mock_file.changes = 1
        mock_file.patch = "@@ -1,2 +1,2 @@"
        
        mock_pr.get_files.return_value = [mock_file]
        service.github.get_repo.return_value.get_pull.return_value = mock_pr
        
        files = service.get_pull_request_files("owner", "repo", 123)
        assert len(files) == 1
        assert files[0]["filename"] == "test.py"

# Test get_branches
def test_get_branches():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_branch = Mock()
        mock_branch.name = "main"
        service.github.get_repo.return_value.get_branches.return_value = [mock_branch]
        
        branches = service.get_branches("owner", "repo")
        assert branches == ["main"]

# Test get_commits
def test_get_commits():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_commit = Mock()
        mock_commit.sha = "abc123"
        mock_commit.commit.message = "test commit"
        mock_commit.author.login = "testuser"
        mock_commit.commit.author.date.isoformat.return_value = "2023-01-01T00:00:00"
        mock_commit.html_url = "http://example.com"
        
        service.github.get_repo.return_value.get_commits.return_value = [mock_commit]
        
        commits = service.get_commits("owner", "repo")
        assert len(commits) == 1
        assert commits[0]["sha"] == "abc123"

# Test error when token is invalid during initialization
def test_github_service_init_with_invalid_token():
    with patch('os.getenv', return_value='fake_token'):
        with patch('github.Github') as mock_github:
            # Configure the mock to raise GithubException when get_user is called
            mock_github_instance = Mock()
            mock_github_instance.get_user.side_effect = GithubException(Mock(), 401, {})
            mock_github.return_value = mock_github_instance
            
            with pytest.raises(ValueError, match="Invalid GitHub token"):
                GitHubService()

# Test get_file_content with directory path
def test_get_file_content_directory():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_content = Mock()
        mock_content.decoded_content.decode.return_value = "file content"
        service.github.get_repo.return_value.get_contents.return_value = [mock_content]
        
        content = service.get_file_content("https://github.com/owner/repo", "path/")
        assert content == "file content"

# Test get_file_content file not found
def test_get_file_content_not_found():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        service.github.get_repo.return_value.get_contents.side_effect = Exception("Not found")
        
        content = service.get_file_content("https://github.com/owner/repo", "nonexistent.txt")
        assert content is None

# Test parse_repo_url with git SSH format
def test_parse_repo_url_ssh():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        result = service.parse_repo_url("git@github.com:owner/repo.git")
        assert result == ("owner", "repo")

# Test get_repository_issues
def test_get_repository_issues():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_issue = Mock()
        mock_issue.id = 1
        mock_issue.number = 123
        mock_issue.title = "Test issue"
        mock_issue.state = "open"
        mock_issue.body = "Issue body"
        mock_issue.created_at = "2023-01-01T00:00:00"
        mock_issue.updated_at = "2023-01-01T00:00:00"
        mock_issue.closed_at = None
        mock_issue.user.login = "testuser"
        mock_issue.get_labels.return_value = []
        mock_issue.assignees = []
        
        service.github.get_repo.return_value.get_issues.return_value = [mock_issue]
        
        issues = service.get_repository_issues("owner", "repo")
        assert len(issues) == 1
        assert issues[0]["title"] == "Test issue"

# Test get_repository_contributors
def test_get_repository_contributors():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_contributor = Mock()
        mock_contributor.login = "testuser"
        mock_contributor.contributions = 10
        mock_contributor.avatar_url = "http://example.com"
        
        service.github.get_repo.return_value.get_contributors.return_value = [mock_contributor]
        
        contributors = service.get_repository_contributors("owner", "repo")
        assert len(contributors) == 1
        assert contributors[0]["login"] == "testuser"

# Test get_repository_languages
def test_get_repository_languages():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        service.github.get_repo.return_value.get_languages.return_value = {"Python": 1000, "JavaScript": 2000}
        
        languages = service.get_repository_languages("owner", "repo")
        assert languages == {"Python": 1000, "JavaScript": 2000}

# Test get_repository_tags
def test_get_repository_tags():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_tag = Mock()
        mock_tag.name = "v1.0"
        mock_tag.commit.sha = "abc123"
        mock_tag.commit.url = "http://example.com"
        mock_tag.zipball_url = "http://zipball.com"
        mock_tag.tarball_url = "http://tarball.com"
        
        service.github.get_repo.return_value.get_tags.return_value = [mock_tag]
        
        tags = service.get_repository_tags("owner", "repo")
        assert len(tags) == 1
        assert tags[0]["name"] == "v1.0"

# Test get_repository_releases
def test_get_repository_releases():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_release = Mock()
        mock_release.id = 1
        mock_release.tag_name = "v1.0"
        mock_release.name = "Release 1"
        mock_release.body = "Release notes"
        mock_release.draft = False
        mock_release.prerelease = False
        mock_release.created_at = "2023-01-01T00:00:00"
        mock_release.published_at = "2023-01-01T00:00:00"
        mock_release.author.login = "testuser"
        
        service.github.get_repo.return_value.get_releases.return_value = [mock_release]
        
        releases = service.get_repository_releases("owner", "repo")
        assert len(releases) == 1
        assert releases[0]["tag_name"] == "v1.0"

# Test get_repository_stats
def test_get_repository_stats():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_repo = Mock()
        mock_repo.stargazers_count = 100
        mock_repo.watchers_count = 50
        mock_repo.forks_count = 25
        mock_repo.subscribers_count = 10
        mock_repo.open_issues = 5
        mock_repo.forks = 25
        mock_repo.network_count = 30
        
        service.github.get_repo.return_value = mock_repo
        
        stats = service.get_repository_stats("owner", "repo")
        assert stats["stars"] == 100
        assert stats["watchers"] == 50

# Test get_repository_commits_stats
def test_get_repository_commits_stats():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_stat = Mock()
        mock_stat.week = "2023-01-01T00:00:00"
        mock_stat.total = 42
        mock_stat.days = [1, 2, 3, 4, 5, 6, 7]
        
        service.github.get_repo.return_value.get_stats_commit_activity.return_value = [mock_stat]
        
        stats = service.get_repository_commits_stats("owner", "repo")
        assert len(stats) == 1
        assert stats[0]["total"] == 42

# Test get_repository_code_frequency
def test_get_repository_code_frequency():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_stat = Mock()
        mock_stat.week = 1640995200  # 2022-01-01
        mock_stat.additions = 42
        mock_stat.deletions = 15
        
        service.github.get_repo.return_value.get_stats_code_frequency.return_value = [mock_stat]
        
        freq = service.get_repository_code_frequency("owner", "repo")
        assert freq == [[1640995200, 42, 15]]

# Test get_repository_participation
def test_get_repository_participation():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_stats = Mock()
        mock_stats.all = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
        mock_stats.owner = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
        
        service.github.get_repo.return_value.get_stats_participation.return_value = mock_stats
        
        participation = service.get_repository_participation("owner", "repo")
        assert "all" in participation
        assert "owner" in participation

# Test get_repository_punch_card
def test_get_repository_punch_card():
    with patch('os.getenv', return_value='fake_token'):
        service = GitHubService()
        service.github = Mock()
        
        mock_stat = Mock()
        mock_stat.day = 1
        mock_stat.hour = 2
        mock_stat.commits = 5
        
        service.github.get_repo.return_value.get_stats_punch_card.return_value = [mock_stat]
        
        punch_card = service.get_repository_punch_card("owner", "repo")
        assert punch_card == [[1, 2, 5]]