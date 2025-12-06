"""
Trello Integration for Agent Zero

Provides Trello board operations:
- Create/manage boards
- Create/update/move cards
- Manage lists
- Add comments and attachments
- Assign members
- Add labels and checklists
- Search cards
- Get board activities

Setup:
1. Get API key from trello.com/app-key
2. Generate token (click the Token link on app-key page)
3. Configure api_key and token in integration config

Example:
    >>> from python.integrations import get_integration
    >>> trello = get_integration("trello")
    >>> trello.create_card(
    ...     list_id="list_id_here",
    ...     name="New Task",
    ...     desc="Task description"
    ... )
"""

import logging
from typing import Dict, Any, Optional, List

from .base import BaseIntegration, RateLimitConfig

logger = logging.getLogger(__name__)


class TrelloIntegration(BaseIntegration):
    """Trello API integration"""

    def __init__(self, name: str, config: Dict[str, Any]):
        # Trello rate limits: 100 requests per 10 seconds per token
        # Conservative estimate: 300 per minute
        rate_limit = RateLimitConfig(
            max_requests=100,
            window_seconds=60,
            burst_size=20
        )

        super().__init__(name, config, rate_limit=rate_limit)

        # Trello uses API key + token
        self.token = config.get("token")

    def get_base_url(self) -> str:
        return "https://api.trello.com/1"

    def get_auth_headers(self) -> Dict[str, str]:
        """Trello uses query params for auth, not headers"""
        return {}

    def _make_request(self, method: str, url: str, params: Optional[Dict] = None, **kwargs):
        """Override to add auth to query params"""
        if params is None:
            params = {}

        # Add authentication to query params
        if self.api_key:
            params["key"] = self.api_key
        if self.token:
            params["token"] = self.token

        return super()._make_request(method, url, params=params, **kwargs)

    def test_connection(self) -> Dict[str, Any]:
        """Test Trello API connection"""
        try:
            member = self.get_member("me")
            return {
                "status": "success",
                "username": member.get("username"),
                "fullName": member.get("fullName"),
                "id": member.get("id")
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def get_member(self, member_id: str = "me") -> Dict[str, Any]:
        """
        Get member info

        Args:
            member_id: Member ID or "me" for authenticated user

        Returns:
            Dict with member details

        Example:
            >>> member = trello.get_member("me")
            >>> print(member["username"])
        """
        return self._make_request("GET", f"/members/{member_id}")

    def list_boards(
        self,
        member_id: str = "me",
        filter: str = "open"
    ) -> List[Dict[str, Any]]:
        """
        List member's boards

        Args:
            member_id: Member ID or "me"
            filter: all, closed, members, open, organization, public, starred

        Returns:
            List of board dicts

        Example:
            >>> boards = trello.list_boards()
            >>> for board in boards:
            ...     print(f"{board['name']}: {board['id']}")
        """
        params = {"filter": filter}
        return self._make_request("GET", f"/members/{member_id}/boards", params=params)

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        Get board details

        Args:
            board_id: Board ID

        Returns:
            Dict with board details

        Example:
            >>> board = trello.get_board("board-id-here")
            >>> print(board["name"])
        """
        return self._make_request("GET", f"/boards/{board_id}")

    def create_board(
        self,
        name: str,
        desc: Optional[str] = None,
        default_lists: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new board

        Args:
            name: Board name
            desc: Board description
            default_lists: Create default lists (To Do, Doing, Done)

        Returns:
            Dict with created board

        Example:
            >>> board = trello.create_board(
            ...     name="Project X",
            ...     desc="Project management board"
            ... )
        """
        params = {
            "name": name,
            "defaultLists": default_lists
        }

        if desc:
            params["desc"] = desc

        return self._make_request("POST", "/boards", params=params)

    def list_lists(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Get lists on a board

        Args:
            board_id: Board ID

        Returns:
            List of list dicts

        Example:
            >>> lists = trello.list_lists("board-id")
            >>> for lst in lists:
            ...     print(f"{lst['name']}: {lst['id']}")
        """
        return self._make_request("GET", f"/boards/{board_id}/lists")

    def create_list(
        self,
        board_id: str,
        name: str,
        pos: str = "bottom"
    ) -> Dict[str, Any]:
        """
        Create a list on a board

        Args:
            board_id: Board ID
            name: List name
            pos: Position (top, bottom, or numeric)

        Returns:
            Dict with created list

        Example:
            >>> lst = trello.create_list(
            ...     board_id="board-id",
            ...     name="In Review"
            ... )
        """
        params = {
            "name": name,
            "idBoard": board_id,
            "pos": pos
        }

        return self._make_request("POST", "/lists", params=params)

    def get_cards_in_list(self, list_id: str) -> List[Dict[str, Any]]:
        """
        Get cards in a list

        Args:
            list_id: List ID

        Returns:
            List of card dicts

        Example:
            >>> cards = trello.get_cards_in_list("list-id")
            >>> for card in cards:
            ...     print(f"{card['name']}: {card['id']}")
        """
        return self._make_request("GET", f"/lists/{list_id}/cards")

    def create_card(
        self,
        list_id: str,
        name: str,
        desc: Optional[str] = None,
        pos: str = "bottom",
        due: Optional[str] = None,
        labels: Optional[List[str]] = None,
        members: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a card

        Args:
            list_id: List ID
            name: Card name
            desc: Card description
            pos: Position (top, bottom, or numeric)
            due: Due date (ISO 8601 format)
            labels: List of label IDs
            members: List of member IDs

        Returns:
            Dict with created card

        Example:
            >>> card = trello.create_card(
            ...     list_id="list-id",
            ...     name="Implement feature X",
            ...     desc="Details about the feature",
            ...     due="2024-12-31"
            ... )
        """
        params = {
            "name": name,
            "idList": list_id,
            "pos": pos
        }

        if desc:
            params["desc"] = desc
        if due:
            params["due"] = due
        if labels:
            params["idLabels"] = ",".join(labels)
        if members:
            params["idMembers"] = ",".join(members)

        return self._make_request("POST", "/cards", params=params)

    def get_card(self, card_id: str) -> Dict[str, Any]:
        """
        Get card details

        Args:
            card_id: Card ID

        Returns:
            Dict with card details

        Example:
            >>> card = trello.get_card("card-id")
            >>> print(card["name"])
        """
        return self._make_request("GET", f"/cards/{card_id}")

    def update_card(
        self,
        card_id: str,
        name: Optional[str] = None,
        desc: Optional[str] = None,
        list_id: Optional[str] = None,
        due: Optional[str] = None,
        closed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update a card

        Args:
            card_id: Card ID
            name: New name
            desc: New description
            list_id: Move to different list
            due: New due date
            closed: Archive card

        Returns:
            Dict with updated card

        Example:
            >>> # Move card to different list
            >>> trello.update_card(
            ...     card_id="card-id",
            ...     list_id="new-list-id"
            ... )
            >>> # Archive card
            >>> trello.update_card(card_id="card-id", closed=True)
        """
        params = {}

        if name is not None:
            params["name"] = name
        if desc is not None:
            params["desc"] = desc
        if list_id is not None:
            params["idList"] = list_id
        if due is not None:
            params["due"] = due
        if closed is not None:
            params["closed"] = closed

        return self._make_request("PUT", f"/cards/{card_id}", params=params)

    def delete_card(self, card_id: str) -> Dict[str, Any]:
        """
        Delete a card permanently

        Args:
            card_id: Card ID

        Example:
            >>> trello.delete_card("card-id")
        """
        return self._make_request("DELETE", f"/cards/{card_id}")

    def add_comment(
        self,
        card_id: str,
        text: str
    ) -> Dict[str, Any]:
        """
        Add comment to a card

        Args:
            card_id: Card ID
            text: Comment text

        Returns:
            Dict with created comment

        Example:
            >>> trello.add_comment(
            ...     card_id="card-id",
            ...     text="This looks good!"
            ... )
        """
        params = {"text": text}
        return self._make_request("POST", f"/cards/{card_id}/actions/comments", params=params)

    def add_checklist(
        self,
        card_id: str,
        name: str,
        items: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Add checklist to a card

        Args:
            card_id: Card ID
            name: Checklist name
            items: List of checklist item names

        Returns:
            Dict with created checklist

        Example:
            >>> trello.add_checklist(
            ...     card_id="card-id",
            ...     name="Prerequisites",
            ...     items=["Review code", "Run tests", "Update docs"]
            ... )
        """
        params = {
            "name": name,
            "idCard": card_id
        }

        result = self._make_request("POST", "/checklists", params=params)

        # Add items if provided
        if items:
            checklist_id = result["id"]
            for item_name in items:
                self.add_checklist_item(checklist_id, item_name)

        return result

    def add_checklist_item(
        self,
        checklist_id: str,
        name: str,
        checked: bool = False
    ) -> Dict[str, Any]:
        """
        Add item to checklist

        Args:
            checklist_id: Checklist ID
            name: Item name
            checked: Item checked state

        Example:
            >>> trello.add_checklist_item(
            ...     checklist_id="checklist-id",
            ...     name="Write unit tests"
            ... )
        """
        params = {
            "name": name,
            "checked": checked
        }

        return self._make_request(
            "POST",
            f"/checklists/{checklist_id}/checkItems",
            params=params
        )

    def add_label_to_card(
        self,
        card_id: str,
        label_id: str
    ) -> Dict[str, Any]:
        """
        Add label to card

        Args:
            card_id: Card ID
            label_id: Label ID

        Example:
            >>> trello.add_label_to_card("card-id", "label-id")
        """
        params = {"value": label_id}
        return self._make_request("POST", f"/cards/{card_id}/idLabels", params=params)

    def add_member_to_card(
        self,
        card_id: str,
        member_id: str
    ) -> Dict[str, Any]:
        """
        Assign member to card

        Args:
            card_id: Card ID
            member_id: Member ID

        Example:
            >>> trello.add_member_to_card("card-id", "member-id")
        """
        params = {"value": member_id}
        return self._make_request("POST", f"/cards/{card_id}/idMembers", params=params)

    def search(
        self,
        query: str,
        model_types: str = "cards",
        board_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search Trello

        Args:
            query: Search query
            model_types: What to search (cards, boards, organizations, members)
            board_ids: Limit search to specific boards

        Returns:
            Dict with search results

        Example:
            >>> results = trello.search("urgent bug")
            >>> for card in results.get("cards", []):
            ...     print(f"{card['name']} on {card['board']['name']}")
        """
        params = {
            "query": query,
            "modelTypes": model_types,
            "card_fields": "name,desc,due,idList,idBoard",
            "cards_limit": 50
        }

        if board_ids:
            params["idBoards"] = ",".join(board_ids)

        return self._make_request("GET", "/search", params=params)

    def get_board_labels(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Get labels on a board

        Args:
            board_id: Board ID

        Returns:
            List of label dicts

        Example:
            >>> labels = trello.get_board_labels("board-id")
            >>> for label in labels:
            ...     print(f"{label['name']}: {label['color']}")
        """
        return self._make_request("GET", f"/boards/{board_id}/labels")

    def create_label(
        self,
        board_id: str,
        name: str,
        color: str = "blue"
    ) -> Dict[str, Any]:
        """
        Create a label on a board

        Args:
            board_id: Board ID
            name: Label name
            color: Label color (blue, green, orange, red, purple, etc.)

        Returns:
            Dict with created label

        Example:
            >>> label = trello.create_label(
            ...     board_id="board-id",
            ...     name="High Priority",
            ...     color="red"
            ... )
        """
        params = {
            "name": name,
            "color": color,
            "idBoard": board_id
        }

        return self._make_request("POST", "/labels", params=params)
