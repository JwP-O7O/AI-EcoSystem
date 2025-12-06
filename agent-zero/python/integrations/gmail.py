"""
Gmail Integration for Agent Zero

Provides email operations through Gmail API:
- Send emails (with attachments)
- Read emails (with filters)
- Search emails
- Mark as read/unread
- Archive/delete emails
- Create drafts
- Get labels
- Manage threads

Setup:
1. Enable Gmail API in Google Cloud Console
2. Create OAuth 2.0 credentials
3. Configure scopes: gmail.send, gmail.readonly, gmail.modify
4. Save credentials in config file

Example:
    >>> from python.integrations import get_integration
    >>> gmail = get_integration("gmail")
    >>> gmail.send_email(
    ...     to="user@example.com",
    ...     subject="Hello",
    ...     body="Test email"
    ... )
"""

import base64
import logging
from typing import Dict, Any, Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from .base import BaseIntegration, RateLimitConfig

logger = logging.getLogger(__name__)


class GmailIntegration(BaseIntegration):
    """Gmail API integration"""

    def __init__(self, name: str, config: Dict[str, Any]):
        # Gmail API rate limits: 250 quota units per user per second
        rate_limit = RateLimitConfig(
            max_requests=100,
            window_seconds=60,
            burst_size=20
        )

        super().__init__(name, config, rate_limit=rate_limit)

        # Set OAuth URLs if not in config
        if not self.oauth.authorize_url:
            self.oauth.authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
        if not self.oauth.token_url:
            self.oauth.token_url = "https://oauth2.googleapis.com/token"

        # Default scopes
        if not self.oauth.scopes:
            self.oauth.scopes = [
                "https://www.googleapis.com/auth/gmail.send",
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.modify"
            ]

    def get_base_url(self) -> str:
        return "https://gmail.googleapis.com/gmail/v1"

    def test_connection(self) -> Dict[str, Any]:
        """Test Gmail API connection"""
        try:
            profile = self.get_profile()
            return {
                "status": "success",
                "email": profile.get("emailAddress"),
                "total_messages": profile.get("messagesTotal"),
                "threads_total": profile.get("threadsTotal")
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def get_profile(self) -> Dict[str, Any]:
        """
        Get user's Gmail profile

        Returns:
            Dict with emailAddress, messagesTotal, threadsTotal, historyId

        Example:
            >>> profile = gmail.get_profile()
            >>> print(profile["emailAddress"])
        """
        return self._make_request("GET", "/users/me/profile")

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        html: bool = False,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Send an email

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            html: Whether body is HTML
            attachments: List of dicts with 'filename' and 'content' (bytes)

        Returns:
            Dict with id, threadId, labelIds

        Example:
            >>> gmail.send_email(
            ...     to="user@example.com",
            ...     subject="Hello from Agent Zero",
            ...     body="<h1>Hello!</h1>",
            ...     html=True
            ... )
        """
        # Create message
        if attachments:
            message = MIMEMultipart()
        else:
            message = MIMEText(body, "html" if html else "plain")

        message["To"] = to
        message["Subject"] = subject

        if cc:
            message["Cc"] = cc
        if bcc:
            message["Bcc"] = bcc

        # Add body if multipart
        if attachments:
            body_part = MIMEText(body, "html" if html else "plain")
            message.attach(body_part)

            # Add attachments
            for attachment in attachments:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment["content"])
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={attachment['filename']}"
                )
                message.attach(part)

        # Encode message
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        return self._make_request(
            "POST",
            "/users/me/messages/send",
            json_data={"raw": raw}
        )

    def list_messages(
        self,
        query: Optional[str] = None,
        max_results: int = 10,
        label_ids: Optional[List[str]] = None,
        include_spam_trash: bool = False
    ) -> Dict[str, Any]:
        """
        List messages matching query

        Args:
            query: Gmail search query (e.g., "from:user@example.com is:unread")
            max_results: Maximum number of messages to return
            label_ids: Only return messages with all labels
            include_spam_trash: Include spam and trash

        Returns:
            Dict with messages (list) and resultSizeEstimate

        Example:
            >>> messages = gmail.list_messages(
            ...     query="is:unread",
            ...     max_results=5
            ... )
            >>> for msg in messages["messages"]:
            ...     print(msg["id"])
        """
        params = {
            "maxResults": max_results,
            "includeSpamTrash": include_spam_trash
        }

        if query:
            params["q"] = query

        if label_ids:
            params["labelIds"] = label_ids

        return self._make_request("GET", "/users/me/messages", params=params)

    def get_message(
        self,
        message_id: str,
        format: str = "full"
    ) -> Dict[str, Any]:
        """
        Get a specific message

        Args:
            message_id: Message ID
            format: Format to return (minimal, full, raw, metadata)

        Returns:
            Dict with full message details

        Example:
            >>> msg = gmail.get_message("12345")
            >>> print(msg["snippet"])
        """
        params = {"format": format}
        return self._make_request(
            "GET",
            f"/users/me/messages/{message_id}",
            params=params
        )

    def search_messages(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search messages and return full details

        Args:
            query: Gmail search query
            max_results: Maximum number of results

        Returns:
            List of message dicts with full details

        Example:
            >>> results = gmail.search_messages("from:boss@company.com urgent")
            >>> for msg in results:
            ...     print(msg["snippet"])
        """
        # List messages
        result = self.list_messages(query=query, max_results=max_results)

        # Get full details for each message
        messages = []
        for msg_ref in result.get("messages", []):
            try:
                msg = self.get_message(msg_ref["id"])
                messages.append(msg)
            except Exception as e:
                logger.error(f"Failed to get message {msg_ref['id']}: {e}")

        return messages

    def modify_message(
        self,
        message_id: str,
        add_labels: Optional[List[str]] = None,
        remove_labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Modify message labels

        Args:
            message_id: Message ID
            add_labels: Labels to add
            remove_labels: Labels to remove

        Returns:
            Updated message

        Example:
            >>> gmail.modify_message(
            ...     "12345",
            ...     add_labels=["IMPORTANT"],
            ...     remove_labels=["UNREAD"]
            ... )
        """
        body = {}

        if add_labels:
            body["addLabelIds"] = add_labels
        if remove_labels:
            body["removeLabelIds"] = remove_labels

        return self._make_request(
            "POST",
            f"/users/me/messages/{message_id}/modify",
            json_data=body
        )

    def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """
        Mark message as read

        Example:
            >>> gmail.mark_as_read("12345")
        """
        return self.modify_message(message_id, remove_labels=["UNREAD"])

    def mark_as_unread(self, message_id: str) -> Dict[str, Any]:
        """
        Mark message as unread

        Example:
            >>> gmail.mark_as_unread("12345")
        """
        return self.modify_message(message_id, add_labels=["UNREAD"])

    def archive_message(self, message_id: str) -> Dict[str, Any]:
        """
        Archive message (remove from INBOX)

        Example:
            >>> gmail.archive_message("12345")
        """
        return self.modify_message(message_id, remove_labels=["INBOX"])

    def trash_message(self, message_id: str) -> Dict[str, Any]:
        """
        Move message to trash

        Example:
            >>> gmail.trash_message("12345")
        """
        return self._make_request(
            "POST",
            f"/users/me/messages/{message_id}/trash"
        )

    def delete_message(self, message_id: str) -> Dict[str, Any]:
        """
        Permanently delete message

        Example:
            >>> gmail.delete_message("12345")
        """
        return self._make_request(
            "DELETE",
            f"/users/me/messages/{message_id}"
        )

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False
    ) -> Dict[str, Any]:
        """
        Create an email draft

        Args:
            to: Recipient
            subject: Subject
            body: Body
            html: Whether body is HTML

        Returns:
            Dict with draft id and message

        Example:
            >>> draft = gmail.create_draft(
            ...     to="user@example.com",
            ...     subject="Draft",
            ...     body="Draft content"
            ... )
        """
        message = MIMEText(body, "html" if html else "plain")
        message["To"] = to
        message["Subject"] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        return self._make_request(
            "POST",
            "/users/me/drafts",
            json_data={"message": {"raw": raw}}
        )

    def list_labels(self) -> Dict[str, Any]:
        """
        List all labels

        Returns:
            Dict with labels list

        Example:
            >>> labels = gmail.list_labels()
            >>> for label in labels["labels"]:
            ...     print(label["name"])
        """
        return self._make_request("GET", "/users/me/labels")

    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """
        Get email thread

        Args:
            thread_id: Thread ID

        Returns:
            Dict with thread messages

        Example:
            >>> thread = gmail.get_thread("12345")
            >>> print(f"Thread has {len(thread['messages'])} messages")
        """
        return self._make_request("GET", f"/users/me/threads/{thread_id}")

    def parse_message_body(self, message: Dict[str, Any]) -> str:
        """
        Extract plain text body from message

        Args:
            message: Message dict from get_message()

        Returns:
            Plain text body

        Example:
            >>> msg = gmail.get_message("12345")
            >>> body = gmail.parse_message_body(msg)
        """
        def get_body_from_part(part):
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8")

            if "parts" in part:
                for subpart in part["parts"]:
                    result = get_body_from_part(subpart)
                    if result:
                        return result

            return None

        payload = message.get("payload", {})
        return get_body_from_part(payload) or message.get("snippet", "")
