"""
Slack Integration for Agent Zero

Provides Slack workspace operations:
- Send messages (to channels and users)
- Read channel history
- Search messages
- Upload files
- Manage channels (create, join, leave)
- Get user info
- React to messages
- Update/delete messages
- Get workspace info

Setup:
1. Create Slack App in api.slack.com/apps
2. Add Bot Token Scopes (chat:write, channels:read, etc.)
3. Install app to workspace
4. Use Bot User OAuth Token

Example:
    >>> from python.integrations import get_integration
    >>> slack = get_integration("slack")
    >>> slack.send_message(
    ...     channel="#general",
    ...     text="Hello from Agent Zero!"
    ... )
"""

import logging
from typing import Dict, Any, Optional, List

from .base import BaseIntegration, RateLimitConfig

logger = logging.getLogger(__name__)


class SlackIntegration(BaseIntegration):
    """Slack API integration"""

    def __init__(self, name: str, config: Dict[str, Any]):
        # Slack rate limits: Tier 1 = 1 req/min, Tier 2 = 20/min, Tier 3 = 50/min
        # Using conservative limits
        rate_limit = RateLimitConfig(
            max_requests=20,
            window_seconds=60,
            burst_size=5
        )

        super().__init__(name, config, rate_limit=rate_limit)

        # Slack uses Bot Token instead of OAuth for bots
        self.bot_token = config.get("bot_token")

    def get_base_url(self) -> str:
        return "https://slack.com/api"

    def get_auth_headers(self) -> Dict[str, str]:
        """Override to use Slack's Bearer token format"""
        headers = {}
        token = self.bot_token or self.oauth.access_token or self.api_key

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    def test_connection(self) -> Dict[str, Any]:
        """Test Slack API connection"""
        try:
            result = self.auth_test()
            return {
                "status": "success",
                "team": result.get("team"),
                "user": result.get("user"),
                "team_id": result.get("team_id"),
                "user_id": result.get("user_id")
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _check_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Check Slack API response for errors"""
        if not response.get("ok"):
            error = response.get("error", "Unknown error")
            raise RuntimeError(f"Slack API error: {error}")
        return response

    def auth_test(self) -> Dict[str, Any]:
        """
        Test authentication and get bot info

        Returns:
            Dict with team, user, team_id, user_id

        Example:
            >>> info = slack.auth_test()
            >>> print(info["team"])
        """
        response = self._make_request("POST", "/auth.test")
        return self._check_response(response)

    def send_message(
        self,
        channel: str,
        text: str,
        thread_ts: Optional[str] = None,
        blocks: Optional[List[Dict]] = None,
        attachments: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to a channel or user

        Args:
            channel: Channel ID or name (e.g., "#general" or "C1234567890")
            text: Message text (fallback for blocks)
            thread_ts: Thread timestamp to reply to
            blocks: Block Kit blocks for rich formatting
            attachments: Legacy attachments

        Returns:
            Dict with channel, ts (timestamp), message

        Example:
            >>> slack.send_message(
            ...     channel="#general",
            ...     text="Hello World!"
            ... )
            >>> # Rich formatting with blocks
            >>> slack.send_message(
            ...     channel="#general",
            ...     text="Hello",
            ...     blocks=[
            ...         {
            ...             "type": "section",
            ...             "text": {"type": "mrkdwn", "text": "*Bold* text"}
            ...         }
            ...     ]
            ... )
        """
        data = {
            "channel": channel,
            "text": text
        }

        if thread_ts:
            data["thread_ts"] = thread_ts

        if blocks:
            data["blocks"] = blocks

        if attachments:
            data["attachments"] = attachments

        response = self._make_request("POST", "/chat.postMessage", json_data=data)
        return self._check_response(response)

    def update_message(
        self,
        channel: str,
        ts: str,
        text: str,
        blocks: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Update a message

        Args:
            channel: Channel ID
            ts: Message timestamp
            text: New text
            blocks: New blocks

        Example:
            >>> slack.update_message(
            ...     channel="C1234567890",
            ...     ts="1234567890.123456",
            ...     text="Updated message"
            ... )
        """
        data = {
            "channel": channel,
            "ts": ts,
            "text": text
        }

        if blocks:
            data["blocks"] = blocks

        response = self._make_request("POST", "/chat.update", json_data=data)
        return self._check_response(response)

    def delete_message(self, channel: str, ts: str) -> Dict[str, Any]:
        """
        Delete a message

        Args:
            channel: Channel ID
            ts: Message timestamp

        Example:
            >>> slack.delete_message("C1234567890", "1234567890.123456")
        """
        data = {
            "channel": channel,
            "ts": ts
        }

        response = self._make_request("POST", "/chat.delete", json_data=data)
        return self._check_response(response)

    def get_conversation_history(
        self,
        channel: str,
        limit: int = 100,
        oldest: Optional[str] = None,
        latest: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get channel message history

        Args:
            channel: Channel ID
            limit: Number of messages to return (max 1000)
            oldest: Only messages after this timestamp
            latest: Only messages before this timestamp

        Returns:
            Dict with messages (list) and has_more

        Example:
            >>> history = slack.get_conversation_history("#general", limit=10)
            >>> for msg in history["messages"]:
            ...     print(msg["text"])
        """
        params = {
            "channel": channel,
            "limit": limit
        }

        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest

        response = self._make_request("GET", "/conversations.history", params=params)
        return self._check_response(response)

    def list_channels(
        self,
        exclude_archived: bool = True,
        types: str = "public_channel"
    ) -> Dict[str, Any]:
        """
        List channels

        Args:
            exclude_archived: Exclude archived channels
            types: Channel types (public_channel, private_channel, mpim, im)

        Returns:
            Dict with channels list

        Example:
            >>> channels = slack.list_channels()
            >>> for channel in channels["channels"]:
            ...     print(channel["name"])
        """
        params = {
            "exclude_archived": exclude_archived,
            "types": types
        }

        response = self._make_request("GET", "/conversations.list", params=params)
        return self._check_response(response)

    def create_channel(
        self,
        name: str,
        is_private: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new channel

        Args:
            name: Channel name
            is_private: Create private channel

        Returns:
            Dict with channel details

        Example:
            >>> channel = slack.create_channel("agent-zero-logs")
            >>> print(channel["channel"]["id"])
        """
        data = {
            "name": name,
            "is_private": is_private
        }

        response = self._make_request("POST", "/conversations.create", json_data=data)
        return self._check_response(response)

    def join_channel(self, channel: str) -> Dict[str, Any]:
        """
        Join a channel

        Args:
            channel: Channel ID

        Example:
            >>> slack.join_channel("C1234567890")
        """
        data = {"channel": channel}
        response = self._make_request("POST", "/conversations.join", json_data=data)
        return self._check_response(response)

    def leave_channel(self, channel: str) -> Dict[str, Any]:
        """
        Leave a channel

        Args:
            channel: Channel ID

        Example:
            >>> slack.leave_channel("C1234567890")
        """
        data = {"channel": channel}
        response = self._make_request("POST", "/conversations.leave", json_data=data)
        return self._check_response(response)

    def add_reaction(
        self,
        channel: str,
        timestamp: str,
        name: str
    ) -> Dict[str, Any]:
        """
        Add emoji reaction to message

        Args:
            channel: Channel ID
            timestamp: Message timestamp
            name: Emoji name (without ::)

        Example:
            >>> slack.add_reaction(
            ...     channel="C1234567890",
            ...     timestamp="1234567890.123456",
            ...     name="thumbsup"
            ... )
        """
        data = {
            "channel": channel,
            "timestamp": timestamp,
            "name": name
        }

        response = self._make_request("POST", "/reactions.add", json_data=data)
        return self._check_response(response)

    def upload_file(
        self,
        channels: str,
        content: str,
        filename: str,
        title: Optional[str] = None,
        initial_comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file

        Args:
            channels: Comma-separated channel IDs
            content: File content (text)
            filename: Filename
            title: File title
            initial_comment: Comment to add

        Returns:
            Dict with file details

        Example:
            >>> slack.upload_file(
            ...     channels="C1234567890",
            ...     content="Log data here",
            ...     filename="log.txt",
            ...     title="Application Logs"
            ... )
        """
        data = {
            "channels": channels,
            "content": content,
            "filename": filename
        }

        if title:
            data["title"] = title
        if initial_comment:
            data["initial_comment"] = initial_comment

        response = self._make_request("POST", "/files.upload", json_data=data)
        return self._check_response(response)

    def search_messages(
        self,
        query: str,
        count: int = 20,
        sort: str = "score"
    ) -> Dict[str, Any]:
        """
        Search messages

        Args:
            query: Search query
            count: Number of results
            sort: Sort by score or timestamp

        Returns:
            Dict with messages and pagination info

        Example:
            >>> results = slack.search_messages("important deadline")
            >>> for msg in results["messages"]["matches"]:
            ...     print(msg["text"])
        """
        params = {
            "query": query,
            "count": count,
            "sort": sort
        }

        response = self._make_request("GET", "/search.messages", params=params)
        return self._check_response(response)

    def get_user_info(self, user: str) -> Dict[str, Any]:
        """
        Get user information

        Args:
            user: User ID

        Returns:
            Dict with user details

        Example:
            >>> user = slack.get_user_info("U1234567890")
            >>> print(user["user"]["real_name"])
        """
        params = {"user": user}
        response = self._make_request("GET", "/users.info", params=params)
        return self._check_response(response)

    def list_users(self, limit: int = 100) -> Dict[str, Any]:
        """
        List workspace users

        Args:
            limit: Number of users to return

        Returns:
            Dict with members list

        Example:
            >>> users = slack.list_users()
            >>> for user in users["members"]:
            ...     print(user["name"])
        """
        params = {"limit": limit}
        response = self._make_request("GET", "/users.list", params=params)
        return self._check_response(response)

    def get_permalink(self, channel: str, message_ts: str) -> str:
        """
        Get permanent link to a message

        Args:
            channel: Channel ID
            message_ts: Message timestamp

        Returns:
            Permalink URL

        Example:
            >>> url = slack.get_permalink("C1234567890", "1234567890.123456")
        """
        params = {
            "channel": channel,
            "message_ts": message_ts
        }

        response = self._make_request("GET", "/chat.getPermalink", params=params)
        result = self._check_response(response)
        return result.get("permalink", "")
