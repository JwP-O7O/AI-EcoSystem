"""
GitHub Integration for Agent Zero

Provides GitHub repository operations:
- Create/manage repositories
- Create/update/close issues
- Create/merge pull requests
- Manage branches
- Get repository info
- Search code/repos/issues
- Create commits
- Manage releases
- Get user info

Setup:
1. Create Personal Access Token at github.com/settings/tokens
2. Select scopes: repo, user, admin:org
3. Configure token in integration config

Example:
    >>> from python.integrations import get_integration
    >>> github = get_integration("github")
    >>> github.create_issue(
    ...     repo="owner/repo",
    ...     title="Bug found",
    ...     body="Description here"
    ... )
"""

import logging
from typing import Dict, Any, Optional, List

from .base import BaseIntegration, RateLimitConfig

logger = logging.getLogger(__name__)


class GitHubIntegration(BaseIntegration):
    """GitHub API integration"""

    def __init__(self, name: str, config: Dict[str, Any]):
        # GitHub rate limits: 5000 req/hour for authenticated, 60 for unauthenticated
        # ~83 requests per minute
        rate_limit = RateLimitConfig(
            max_requests=80,
            window_seconds=60,
            burst_size=20
        )

        super().__init__(name, config, rate_limit=rate_limit)

        # Personal Access Token
        self.token = config.get("token") or config.get("api_key")

    def get_base_url(self) -> str:
        return "https://api.github.com"

    def get_auth_headers(self) -> Dict[str, str]:
        """Override to use GitHub's token format"""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        token = self.token or self.oauth.access_token

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    def test_connection(self) -> Dict[str, Any]:
        """Test GitHub API connection"""
        try:
            user = self.get_authenticated_user()
            return {
                "status": "success",
                "login": user.get("login"),
                "name": user.get("name"),
                "type": user.get("type")
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def get_authenticated_user(self) -> Dict[str, Any]:
        """
        Get authenticated user info

        Returns:
            Dict with user details

        Example:
            >>> user = github.get_authenticated_user()
            >>> print(user["login"])
        """
        return self._make_request("GET", "/user")

    def create_repository(
        self,
        name: str,
        description: Optional[str] = None,
        private: bool = False,
        auto_init: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new repository

        Args:
            name: Repository name
            description: Repository description
            private: Create private repository
            auto_init: Initialize with README

        Returns:
            Dict with repository details

        Example:
            >>> repo = github.create_repository(
            ...     name="my-project",
            ...     description="My awesome project",
            ...     auto_init=True
            ... )
            >>> print(repo["html_url"])
        """
        data = {
            "name": name,
            "private": private,
            "auto_init": auto_init
        }

        if description:
            data["description"] = description

        return self._make_request("POST", "/user/repos", json_data=data)

    def get_repository(self, repo: str) -> Dict[str, Any]:
        """
        Get repository info

        Args:
            repo: Repository in format "owner/repo"

        Returns:
            Dict with repository details

        Example:
            >>> repo = github.get_repository("torvalds/linux")
            >>> print(repo["stargazers_count"])
        """
        return self._make_request("GET", f"/repos/{repo}")

    def list_repositories(
        self,
        type: str = "all",
        sort: str = "updated",
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        List user repositories

        Args:
            type: all, owner, public, private, member
            sort: created, updated, pushed, full_name
            per_page: Results per page

        Returns:
            List of repository dicts

        Example:
            >>> repos = github.list_repositories(type="owner")
            >>> for repo in repos:
            ...     print(repo["name"])
        """
        params = {
            "type": type,
            "sort": sort,
            "per_page": per_page
        }

        return self._make_request("GET", "/user/repos", params=params)

    def create_issue(
        self,
        repo: str,
        title: str,
        body: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create an issue

        Args:
            repo: Repository in format "owner/repo"
            title: Issue title
            body: Issue description
            labels: List of label names
            assignees: List of usernames to assign

        Returns:
            Dict with issue details

        Example:
            >>> issue = github.create_issue(
            ...     repo="owner/repo",
            ...     title="Bug: Login fails",
            ...     body="Steps to reproduce...",
            ...     labels=["bug", "priority-high"]
            ... )
            >>> print(issue["html_url"])
        """
        data = {"title": title}

        if body:
            data["body"] = body
        if labels:
            data["labels"] = labels
        if assignees:
            data["assignees"] = assignees

        return self._make_request("POST", f"/repos/{repo}/issues", json_data=data)

    def update_issue(
        self,
        repo: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update an issue

        Args:
            repo: Repository in format "owner/repo"
            issue_number: Issue number
            title: New title
            body: New body
            state: open or closed
            labels: New labels

        Example:
            >>> github.update_issue(
            ...     repo="owner/repo",
            ...     issue_number=42,
            ...     state="closed"
            ... )
        """
        data = {}

        if title:
            data["title"] = title
        if body:
            data["body"] = body
        if state:
            data["state"] = state
        if labels:
            data["labels"] = labels

        return self._make_request(
            "PATCH",
            f"/repos/{repo}/issues/{issue_number}",
            json_data=data
        )

    def list_issues(
        self,
        repo: str,
        state: str = "open",
        labels: Optional[str] = None,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        List repository issues

        Args:
            repo: Repository in format "owner/repo"
            state: open, closed, all
            labels: Filter by labels (comma-separated)
            per_page: Results per page

        Returns:
            List of issue dicts

        Example:
            >>> issues = github.list_issues("owner/repo", state="open")
            >>> for issue in issues:
            ...     print(f"#{issue['number']}: {issue['title']}")
        """
        params = {
            "state": state,
            "per_page": per_page
        }

        if labels:
            params["labels"] = labels

        return self._make_request("GET", f"/repos/{repo}/issues", params=params)

    def create_pull_request(
        self,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: Optional[str] = None,
        draft: bool = False
    ) -> Dict[str, Any]:
        """
        Create a pull request

        Args:
            repo: Repository in format "owner/repo"
            title: PR title
            head: Branch with changes (e.g., "feature-branch")
            base: Branch to merge into (e.g., "main")
            body: PR description
            draft: Create as draft PR

        Returns:
            Dict with PR details

        Example:
            >>> pr = github.create_pull_request(
            ...     repo="owner/repo",
            ...     title="Add new feature",
            ...     head="feature-branch",
            ...     base="main",
            ...     body="This PR adds..."
            ... )
            >>> print(pr["html_url"])
        """
        data = {
            "title": title,
            "head": head,
            "base": base,
            "draft": draft
        }

        if body:
            data["body"] = body

        return self._make_request("POST", f"/repos/{repo}/pulls", json_data=data)

    def list_pull_requests(
        self,
        repo: str,
        state: str = "open",
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        List pull requests

        Args:
            repo: Repository in format "owner/repo"
            state: open, closed, all
            per_page: Results per page

        Returns:
            List of PR dicts

        Example:
            >>> prs = github.list_pull_requests("owner/repo")
            >>> for pr in prs:
            ...     print(f"#{pr['number']}: {pr['title']}")
        """
        params = {
            "state": state,
            "per_page": per_page
        }

        return self._make_request("GET", f"/repos/{repo}/pulls", params=params)

    def merge_pull_request(
        self,
        repo: str,
        pull_number: int,
        commit_message: Optional[str] = None,
        merge_method: str = "merge"
    ) -> Dict[str, Any]:
        """
        Merge a pull request

        Args:
            repo: Repository in format "owner/repo"
            pull_number: PR number
            commit_message: Merge commit message
            merge_method: merge, squash, or rebase

        Example:
            >>> github.merge_pull_request(
            ...     repo="owner/repo",
            ...     pull_number=42,
            ...     merge_method="squash"
            ... )
        """
        data = {"merge_method": merge_method}

        if commit_message:
            data["commit_message"] = commit_message

        return self._make_request(
            "PUT",
            f"/repos/{repo}/pulls/{pull_number}/merge",
            json_data=data
        )

    def create_branch(
        self,
        repo: str,
        branch: str,
        from_branch: str = "main"
    ) -> Dict[str, Any]:
        """
        Create a new branch

        Args:
            repo: Repository in format "owner/repo"
            branch: New branch name
            from_branch: Branch to create from

        Returns:
            Dict with reference details

        Example:
            >>> github.create_branch(
            ...     repo="owner/repo",
            ...     branch="feature-x",
            ...     from_branch="main"
            ... )
        """
        # Get SHA of from_branch
        ref_data = self._make_request("GET", f"/repos/{repo}/git/ref/heads/{from_branch}")
        sha = ref_data["object"]["sha"]

        # Create new branch
        data = {
            "ref": f"refs/heads/{branch}",
            "sha": sha
        }

        return self._make_request("POST", f"/repos/{repo}/git/refs", json_data=data)

    def search_code(
        self,
        query: str,
        per_page: int = 30
    ) -> Dict[str, Any]:
        """
        Search code

        Args:
            query: Search query (e.g., "addClass in:file language:js")
            per_page: Results per page

        Returns:
            Dict with items (list) and total_count

        Example:
            >>> results = github.search_code("TODO language:python")
            >>> for item in results["items"]:
            ...     print(f"{item['repository']['full_name']}: {item['path']}")
        """
        params = {
            "q": query,
            "per_page": per_page
        }

        return self._make_request("GET", "/search/code", params=params)

    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        per_page: int = 30
    ) -> Dict[str, Any]:
        """
        Search repositories

        Args:
            query: Search query (e.g., "machine learning language:python")
            sort: stars, forks, updated
            per_page: Results per page

        Returns:
            Dict with items (list) and total_count

        Example:
            >>> results = github.search_repositories(
            ...     "agent framework language:python",
            ...     sort="stars"
            ... )
            >>> for repo in results["items"]:
            ...     print(f"{repo['full_name']}: {repo['stargazers_count']} stars")
        """
        params = {
            "q": query,
            "sort": sort,
            "per_page": per_page
        }

        return self._make_request("GET", "/search/repositories", params=params)

    def create_release(
        self,
        repo: str,
        tag_name: str,
        name: str,
        body: Optional[str] = None,
        draft: bool = False,
        prerelease: bool = False
    ) -> Dict[str, Any]:
        """
        Create a release

        Args:
            repo: Repository in format "owner/repo"
            tag_name: Tag for the release
            name: Release name
            body: Release notes
            draft: Create as draft
            prerelease: Mark as prerelease

        Returns:
            Dict with release details

        Example:
            >>> release = github.create_release(
            ...     repo="owner/repo",
            ...     tag_name="v1.0.0",
            ...     name="Version 1.0.0",
            ...     body="# Changelog\\n- Feature 1\\n- Feature 2"
            ... )
        """
        data = {
            "tag_name": tag_name,
            "name": name,
            "draft": draft,
            "prerelease": prerelease
        }

        if body:
            data["body"] = body

        return self._make_request("POST", f"/repos/{repo}/releases", json_data=data)

    def get_file_content(
        self,
        repo: str,
        path: str,
        ref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get file content from repository

        Args:
            repo: Repository in format "owner/repo"
            path: File path
            ref: Branch, tag, or commit SHA

        Returns:
            Dict with file content (base64 encoded)

        Example:
            >>> file = github.get_file_content("owner/repo", "README.md")
            >>> import base64
            >>> content = base64.b64decode(file["content"]).decode()
        """
        params = {}
        if ref:
            params["ref"] = ref

        return self._make_request(
            "GET",
            f"/repos/{repo}/contents/{path}",
            params=params
        )
