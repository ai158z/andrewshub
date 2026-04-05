import os
import logging
from typing import Optional, Dict, List, Tuple
from github import Github, GithubException
from github.Repository import Repository as GithubRepository

# Configure logging
logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub service with authentication.
        
        Args:
            github_token: GitHub personal access_token for authentication
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError(
                "GitHub token is required. Set GITHUB_TOKEN environment variable."
            )
        self.github = Github(self.github_token)
        self._validate_token()

    def _validate_token(self) -> None:
        """Validate the GitHub token by making a simple API call."""
        try:
            # Test the token by getting the authenticated user
            user = self.github.get_user()
            logger.info(f"GitHub token validated for user: {user.login}")
        except GithubException as e:
            logger.error(f"Invalid GitHub token: {str(e)}")
            raise ValueError("Invalid GitHub token") from e

    def get_repository(self, owner: str, repo: str) -> GithubRepository:
        try:
            repository = self.github.get_repo(f"{owner}/{repo}")
            return repository
        except GithubException as e:
            logger.error(f"Failed to access repository {owner}/{repo}: {str(e)}")
            raise

    def get_file_content(self, repo_url: str, file_path: str):
        try:
            # Parse owner and repository name from URL
            if repo_url.startswith("https://github.com/"):
                repo_path = repo_url.replace("https://github.com/", "").strip("/")
                if repo_path.endswith(".git"):
                    repo_path = repo_path[:-4]
            elif repo_url.startswith("git@github.com:"):
                repo_path = repo_url.replace("git@github.com:", "").replace(".git", "")
            else:
                raise ValueError("Invalid repository URL format")

            owner, repo_name = repo_path.split("/", 1)

            repository = self.github.get_repo(f"{owner}/{repo_name}")
            contents = repository.get_contents(file_path)
            return contents.decoded_content.decode('utf-8') if hasattr(contents, 'decoded_content') else contents
        except Exception as e:
            logger.error(f"Error fetching file {file_path} from {repo_url}: {str(e)}")
            return None

    def get_pull_request_files(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """Get files changed in a pull request"""
        try:
            repo_obj = self.github.get_repo(f"{owner}/{repo}")
            pr = repo_obj.get_pull(pr_number)
            files = pr.get_files()
            return [{
                "filename": f.filename,
                "status": f.status,
                "additions": f.additions,
                "deletions": f.deletions,
                "changes": f.changes,
                "patch": f.patch
            } for f in files]
        except Exception as e:
            logger.error(f"Error fetching PR files for {owner}/{repo}/pull/{pr_number}: {str(e)}")
            return []

    def parse_repo_url(self, repo_url: str) -> Tuple[str, str]:
        """Parse repository URL to extract owner and repository name"""
        if repo_url.startswith("https://github.com/"):
            repo_path = repo_url.replace("https://github.com/", "").strip("/")
            if repo_path.endswith(".git"):
                repo_path = repo_path[:-4]
        elif repo_url.startswith("git@github.com:"):
            repo_path = repo_url.replace("git@github.com:", "").replace(".git", "")
        else:
            raise ValueError("Invalid repository URL format")
            
        return tuple(repo_path.split("/", 1))

    def get_branches(self, owner: str, repo_name: str) -> List[str]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            branches = repo.get_branches()
            return [branch.name for branch in branches]
        except Exception as e:
            logger.error(f"Error fetching branches for {owner}/{repo_name}: {str(e)}")
            raise

    def get_commits(self, owner: str, repo_name: str, 
                   branch: str = "main") -> List[Dict]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            if branch:
                commits = repo.get_commits(sha=branch)
            else:
                commits = repo.get_commits()
                
            commit_list = []
            for commit in commits[:30]:  # Limit to recent commits
                commit_list.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.author.login if commit.author else "Unknown",
                    "date": commit.commit.author.date.isoformat() if commit.commit.author and commit.commit.author.date else "",
                    "url": commit.html_url
                })
            return commit_list
        except Exception as e:
            logger.error(f"Error fetching commits for {owner}/{repo_name}: {str(e)}")
            raise

    def get_recent_activity(self, owner: str, repo_name: str) -> Dict:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Get recent commits
            recent_commits = []
            for commit in repo.get_commits()[:10]:
                recent_commits.append({
                    "sha": commit.sha,
                    "message": commit.commit.message[:50] + "..." if len(commit.commit.message) > 50 else commit.commit.message,
                    "author": commit.author.login if commit.author else "Unknown",
                    "date": commit.commit.author.date
                })
                
            # Get recent issues
            recent_issues = []
            for issue in repo.get_issues(state='open')[:20]:
                recent_issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "created_at": issue.created_at,
                    "user": issue.user.login if issue.user else "Unknown"
                })
                
            return {
                "recent_commits": recent_commits,
                "recent_issues": recent_issues
            }
        except Exception as e:
            logger.error(f"Error fetching activity for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repo_details(self, owner: str, repo_name: str) -> Dict:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            return {
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "created_at": repo.created_at,
                "updated_at": repo.updated_at,
                "size": repo.size,
                "stars": repo.stargazers_count,
                "watchers": repo.watchers_count,
                "forks": repo.forks_count
            }
        except Exception as e:
            logger.error(f"Error fetching repo details for {owner}/{repo_name}: {str(e)}")
            raise

    def get_file_tree(self, owner: str, repo_name: str, 
                     branch: str = "main") -> List[Dict]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            branch_ref = repo.get_branch(branch)
            tree = repo.get_git_tree(branch_ref.commit.commit.tree.sha, recursive=True)
            return [{
                "path": t.path,
                "type": "blob" if t.type == "blob" else "tree",
                "sha": t.sha
            } for t in tree.tree]
        except Exception as e:
            logger.error(f"Error fetching file tree for {owner}/{repo_name}: {str(e)}")
            raise

    def get_file_content_by_sha(self, owner: str, repo_name: str, file_sha: str) -> str:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            content = repo.get_git_blob(file_sha)
            return content.content
        except Exception as e:
            logger.error(f"Error fetching content for {file_sha} in {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_issues(self, owner: str, repo_name: str, 
                            state: str = "open") -> List[Dict]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            issues = repo.get_issues(state=state)
            return [{
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "state": issue.state,
                "body": issue.body,
                "created_at": issue.created_at,
                "updated_at": issue.updated_at,
                "closed_at": issue.closed_at,
                "author": issue.user.login if issue.user else None,
                "labels": [label.name for label in issue.get_labels()],
                "assignees": [assignee.login for assignee in issue.assignees]
            } for issue in issues]
        except Exception as e:
            logger.error(f"Error fetching issues for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_contributors(self, owner: str, repo_name: str) -> List[Dict]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            contributors = repo.get_contributors()
            return [{
                "login": contributor.login,
                "contributions": contributor.contributions,
                "avatar_url": contributor.avatar_url
            } for contributor in contributors]
        except Exception as e:
            logger.error(f"Error fetching contributors for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_languages(self, owner: str, repo_name: str) -> Dict:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            return repo.get_languages()
        except Exception as e:
            logger.error(f"Error fetching languages for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_tags(self, owner: str, repo_name: str) -> List[Dict]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            tags = repo.get_tags()
            return [{
                "name": tag.name,
                "commit": {
                    "sha": tag.commit.sha,
                    "url": tag.commit.url
                },
                "zipball_url": tag.zipball_url,
                "tarball_url": tag.tarball_url
            } for tag in tags]
        except Exception as e:
            logger.error(f"Error fetching tags for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_releases(self, owner: str, repo_name: str) -> List[Dict]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            releases = repo.get_releases()
            return [{
                "id": release.id,
                "tag_name": release.tag_name,
                "name": release.name,
                "body": release.body,
                "draft": release.draft,
                "prerelease": release.prerelease,
                "created_at": release.created_at,
                "published_at": release.published_at,
                "author": release.author.login if release.author else None
            } for release in releases]
        except Exception as e:
            logger.error(f"Error fetching releases for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_stats(self, owner: str, repo_name: str) -> Dict:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            return {
                "stars": repo.stargazers_count,
                "watchers": repo.watchers_count,
                "forks": repo.forks_count,
                "subscribers": repo.subscribers_count,
                "network": {
                    "forks": repo.forks,
                    "network_count": repo.network_count
                }
            }
        except Exception as e:
            logger.error(f"Error fetching stats for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_commits_stats(self, owner: str, repo_name: str) -> List[Dict]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            stats = repo.get_stats_commit_activity()
            return [{
                "week": stat.week,
                "total": stat.total,
                "days": stat.days
            } for stat in stats]
        except Exception as e:
            logger.error(f"Error fetching commit stats for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_code_frequency(self, owner: str, repo_name: str) -> List[List[int]]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            stats = repo.get_stats_code_frequency()
            return [[stat.week, stat.additions, stat.deletions] for stat in stats]
        except Exception as e:
            logger.error(f"Error fetching code frequency for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_punch_card(self, owner: str, repo_name: str) -> List[List[int]]:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            stats = repo.get_stats_punch_card()
            return [[stat.day, stat.hour, stat.commits] for stat in stats]
        except Exception as e:
            logger.error(f"Error fetching punch card for {owner}/{repo_name}: {str(e)}")
            raise

    def get_repository_participation(self, owner: str, repo_name: str) -> Dict:
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            stats = repo.get_stats_participation()
            return {
                "all": stats.all,
                "owner": stats.owner
            }
        except Exception as e:
            logger.error(f"Error fetching participation for {owner}/{repo_name}: {str(e)}")
            raise