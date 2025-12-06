"""
Notion Integration for Agent Zero

Provides Notion workspace operations:
- Create/update pages
- Query databases
- Create database entries
- Search content
- Get page/database properties
- Add blocks to pages
- Retrieve page content
- Manage page hierarchy

Setup:
1. Create integration at notion.so/my-integrations
2. Get Internal Integration Token
3. Share pages/databases with integration
4. Configure token in integration config

Example:
    >>> from python.integrations import get_integration
    >>> notion = get_integration("notion")
    >>> notion.create_page(
    ...     parent_id="database_id",
    ...     title="New Page",
    ...     properties={"Status": "In Progress"}
    ... )
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from .base import BaseIntegration, RateLimitConfig

logger = logging.getLogger(__name__)


class NotionIntegration(BaseIntegration):
    """Notion API integration"""

    def __init__(self, name: str, config: Dict[str, Any]):
        # Notion rate limits: 3 requests per second average
        rate_limit = RateLimitConfig(
            max_requests=180,
            window_seconds=60,
            burst_size=10
        )

        super().__init__(name, config, rate_limit=rate_limit)

    def get_base_url(self) -> str:
        return "https://api.notion.com/v1"

    def get_auth_headers(self) -> Dict[str, str]:
        """Override to use Notion's auth format"""
        headers = {
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

        token = self.api_key or self.oauth.access_token

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    def test_connection(self) -> Dict[str, Any]:
        """Test Notion API connection"""
        try:
            # Search for any page to test connection
            result = self.search(query="", page_size=1)
            return {
                "status": "success",
                "accessible_pages": len(result.get("results", []))
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def search(
        self,
        query: str = "",
        filter_type: Optional[str] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Search pages and databases

        Args:
            query: Search query
            filter_type: page or database
            page_size: Number of results

        Returns:
            Dict with results list

        Example:
            >>> results = notion.search("Project Plan")
            >>> for page in results["results"]:
            ...     print(page["id"])
        """
        data = {
            "page_size": page_size
        }

        if query:
            data["query"] = query

        if filter_type:
            data["filter"] = {"property": "object", "value": filter_type}

        return self._make_request("POST", "/search", json_data=data)

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Get page details

        Args:
            page_id: Page ID (with or without hyphens)

        Returns:
            Dict with page properties and metadata

        Example:
            >>> page = notion.get_page("12345678-1234-1234-1234-123456789012")
            >>> print(page["properties"]["title"])
        """
        # Remove hyphens if present
        page_id = page_id.replace("-", "")
        return self._make_request("GET", f"/pages/{page_id}")

    def create_page(
        self,
        parent_id: str,
        title: str,
        properties: Optional[Dict[str, Any]] = None,
        children: Optional[List[Dict]] = None,
        parent_type: str = "database_id"
    ) -> Dict[str, Any]:
        """
        Create a new page

        Args:
            parent_id: Parent database or page ID
            title: Page title
            properties: Additional properties for database pages
            children: Initial page blocks
            parent_type: database_id or page_id

        Returns:
            Dict with created page details

        Example:
            >>> page = notion.create_page(
            ...     parent_id="database-id-here",
            ...     title="New Task",
            ...     properties={"Status": {"select": {"name": "To Do"}}}
            ... )
        """
        parent_id = parent_id.replace("-", "")

        data = {
            "parent": {parent_type: parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        }

        # Add additional properties
        if properties:
            for key, value in properties.items():
                if key != "title":
                    data["properties"][key] = value

        # Add children blocks
        if children:
            data["children"] = children

        return self._make_request("POST", "/pages", json_data=data)

    def update_page(
        self,
        page_id: str,
        properties: Dict[str, Any],
        archived: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update page properties

        Args:
            page_id: Page ID
            properties: Properties to update
            archived: Archive/unarchive page

        Returns:
            Dict with updated page

        Example:
            >>> notion.update_page(
            ...     page_id="page-id-here",
            ...     properties={"Status": {"select": {"name": "Done"}}}
            ... )
        """
        page_id = page_id.replace("-", "")

        data = {"properties": properties}

        if archived is not None:
            data["archived"] = archived

        return self._make_request("PATCH", f"/pages/{page_id}", json_data=data)

    def get_database(self, database_id: str) -> Dict[str, Any]:
        """
        Get database details

        Args:
            database_id: Database ID

        Returns:
            Dict with database schema and properties

        Example:
            >>> db = notion.get_database("database-id-here")
            >>> for prop_name, prop_data in db["properties"].items():
            ...     print(f"{prop_name}: {prop_data['type']}")
        """
        database_id = database_id.replace("-", "")
        return self._make_request("GET", f"/databases/{database_id}")

    def query_database(
        self,
        database_id: str,
        filter_conditions: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Query database entries

        Args:
            database_id: Database ID
            filter_conditions: Filter object
            sorts: List of sort objects
            page_size: Number of results

        Returns:
            Dict with results list

        Example:
            >>> # Query with filter
            >>> results = notion.query_database(
            ...     database_id="db-id",
            ...     filter_conditions={
            ...         "property": "Status",
            ...         "select": {"equals": "In Progress"}
            ...     }
            ... )
            >>> # Query with sort
            >>> results = notion.query_database(
            ...     database_id="db-id",
            ...     sorts=[{"property": "Created", "direction": "descending"}]
            ... )
        """
        database_id = database_id.replace("-", "")

        data = {"page_size": page_size}

        if filter_conditions:
            data["filter"] = filter_conditions

        if sorts:
            data["sorts"] = sorts

        return self._make_request("POST", f"/databases/{database_id}/query", json_data=data)

    def create_database(
        self,
        parent_id: str,
        title: str,
        properties: Dict[str, Dict],
        parent_type: str = "page_id"
    ) -> Dict[str, Any]:
        """
        Create a new database

        Args:
            parent_id: Parent page ID
            title: Database title
            properties: Database schema (property definitions)
            parent_type: page_id

        Returns:
            Dict with created database

        Example:
            >>> db = notion.create_database(
            ...     parent_id="page-id",
            ...     title="Tasks",
            ...     properties={
            ...         "Name": {"title": {}},
            ...         "Status": {"select": {"options": [
            ...             {"name": "To Do"},
            ...             {"name": "In Progress"},
            ...             {"name": "Done"}
            ...         ]}}
            ...     }
            ... )
        """
        parent_id = parent_id.replace("-", "")

        data = {
            "parent": {parent_type: parent_id},
            "title": [{"text": {"content": title}}],
            "properties": properties
        }

        return self._make_request("POST", "/databases", json_data=data)

    def append_blocks(
        self,
        block_id: str,
        children: List[Dict]
    ) -> Dict[str, Any]:
        """
        Append blocks to a page or block

        Args:
            block_id: Page or block ID
            children: List of block objects

        Returns:
            Dict with appended blocks

        Example:
            >>> notion.append_blocks(
            ...     block_id="page-id",
            ...     children=[
            ...         {
            ...             "object": "block",
            ...             "type": "paragraph",
            ...             "paragraph": {
            ...                 "rich_text": [{"text": {"content": "Hello!"}}]
            ...             }
            ...         }
            ...     ]
            ... )
        """
        block_id = block_id.replace("-", "")

        data = {"children": children}

        return self._make_request(
            "PATCH",
            f"/blocks/{block_id}/children",
            json_data=data
        )

    def get_block_children(
        self,
        block_id: str,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Get child blocks of a page or block

        Args:
            block_id: Page or block ID
            page_size: Number of results

        Returns:
            Dict with results (list of blocks)

        Example:
            >>> blocks = notion.get_block_children("page-id")
            >>> for block in blocks["results"]:
            ...     print(f"{block['type']}: {block.get('id')}")
        """
        block_id = block_id.replace("-", "")

        params = {"page_size": page_size}

        return self._make_request(
            "GET",
            f"/blocks/{block_id}/children",
            params=params
        )

    def create_comment(
        self,
        page_id: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Create a comment on a page

        Args:
            page_id: Page ID
            content: Comment text

        Returns:
            Dict with created comment

        Example:
            >>> notion.create_comment(
            ...     page_id="page-id",
            ...     content="Great work on this!"
            ... )
        """
        page_id = page_id.replace("-", "")

        data = {
            "parent": {"page_id": page_id},
            "rich_text": [{"text": {"content": content}}]
        }

        return self._make_request("POST", "/comments", json_data=data)

    def get_users(self, page_size: int = 100) -> Dict[str, Any]:
        """
        List all users in workspace

        Args:
            page_size: Number of results

        Returns:
            Dict with results (list of users)

        Example:
            >>> users = notion.get_users()
            >>> for user in users["results"]:
            ...     print(user["name"])
        """
        params = {"page_size": page_size}
        return self._make_request("GET", "/users", params=params)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user details

        Args:
            user_id: User ID

        Returns:
            Dict with user details

        Example:
            >>> user = notion.get_user("user-id")
            >>> print(user["name"])
        """
        user_id = user_id.replace("-", "")
        return self._make_request("GET", f"/users/{user_id}")

    # Helper methods for creating blocks

    def create_heading_block(self, text: str, level: int = 1) -> Dict:
        """Create heading block (level 1-3)"""
        heading_type = f"heading_{level}"
        return {
            "object": "block",
            "type": heading_type,
            heading_type: {
                "rich_text": [{"text": {"content": text}}]
            }
        }

    def create_paragraph_block(self, text: str) -> Dict:
        """Create paragraph block"""
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": text}}]
            }
        }

    def create_todo_block(self, text: str, checked: bool = False) -> Dict:
        """Create to-do block"""
        return {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"text": {"content": text}}],
                "checked": checked
            }
        }

    def create_code_block(self, code: str, language: str = "python") -> Dict:
        """Create code block"""
        return {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"text": {"content": code}}],
                "language": language
            }
        }
