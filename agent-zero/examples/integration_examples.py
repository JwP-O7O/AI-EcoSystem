"""
Integration Framework Examples

Demonstrates how to use the Integration Framework with all available integrations.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.helpers.integration_framework import IntegrationFramework


def setup_framework():
    """Initialize and setup the framework"""
    print("=== Setting up Integration Framework ===\n")

    framework = IntegrationFramework()
    framework.setup()

    print(f"Available integrations: {framework.list_available()}\n")

    return framework


def gmail_example(framework):
    """Gmail integration examples"""
    print("\n=== Gmail Integration Examples ===\n")

    gmail = framework.get("gmail")

    if not gmail or not gmail.is_authenticated():
        print("Gmail not configured. Skipping...")
        return

    try:
        # Get profile
        profile = gmail.get_profile()
        print(f"Connected as: {profile['emailAddress']}")
        print(f"Total messages: {profile['messagesTotal']}\n")

        # Send email
        print("Sending email...")
        result = gmail.send_email(
            to="test@example.com",
            subject="Test from Agent Zero",
            body="This is a test email sent via the Integration Framework!",
            html=False
        )
        print(f"Email sent: {result['id']}\n")

        # Search unread emails
        print("Searching unread emails...")
        messages = gmail.search_messages("is:unread", max_results=5)
        print(f"Found {len(messages)} unread messages")
        for msg in messages[:3]:
            print(f"  - {msg['snippet'][:50]}...")
        print()

    except Exception as e:
        print(f"Error: {e}\n")


def slack_example(framework):
    """Slack integration examples"""
    print("\n=== Slack Integration Examples ===\n")

    slack = framework.get("slack")

    if not slack or not slack.is_authenticated():
        print("Slack not configured. Skipping...")
        return

    try:
        # Get bot info
        info = slack.auth_test()
        print(f"Connected as: {info['user']} in {info['team']}\n")

        # List channels
        print("Listing channels...")
        channels = slack.list_channels()
        print(f"Found {len(channels['channels'])} channels")
        for channel in channels['channels'][:5]:
            print(f"  - #{channel['name']}")
        print()

        # Send message
        print("Sending message...")
        result = slack.send_message(
            channel="#general",
            text="Hello from Agent Zero Integration Framework!"
        )
        print(f"Message sent: {result['ts']}\n")

        # Send rich message
        print("Sending rich message with blocks...")
        slack.send_message(
            channel="#general",
            text="Status Update",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Integration Framework Test*\nAll systems operational! :white_check_mark:"
                    }
                }
            ]
        )
        print("Rich message sent\n")

    except Exception as e:
        print(f"Error: {e}\n")


def github_example(framework):
    """GitHub integration examples"""
    print("\n=== GitHub Integration Examples ===\n")

    github = framework.get("github")

    if not github or not github.is_authenticated():
        print("GitHub not configured. Skipping...")
        return

    try:
        # Get user info
        user = github.get_authenticated_user()
        print(f"Connected as: {user['login']} ({user['name']})\n")

        # List repositories
        print("Listing repositories...")
        repos = github.list_repositories(type="owner", per_page=5)
        print(f"Your repositories:")
        for repo in repos[:5]:
            print(f"  - {repo['name']}: {repo['stargazers_count']} stars")
        print()

        # Search repositories
        print("Searching for Python agent frameworks...")
        results = github.search_repositories(
            query="agent framework language:python",
            sort="stars",
            per_page=5
        )
        print(f"Top results:")
        for repo in results['items'][:5]:
            print(f"  - {repo['full_name']}: {repo['stargazers_count']} stars")
        print()

        # Example: Create issue (commented out to avoid actual creation)
        # print("Creating issue...")
        # issue = github.create_issue(
        #     repo="owner/repo",
        #     title="Test Issue from Integration Framework",
        #     body="This is a test issue created automatically.",
        #     labels=["test"]
        # )
        # print(f"Issue created: {issue['html_url']}\n")

    except Exception as e:
        print(f"Error: {e}\n")


def notion_example(framework):
    """Notion integration examples"""
    print("\n=== Notion Integration Examples ===\n")

    notion = framework.get("notion")

    if not notion or not notion.is_authenticated():
        print("Notion not configured. Skipping...")
        return

    try:
        # Search for pages
        print("Searching for pages...")
        results = notion.search(query="", page_size=5)
        print(f"Found {len(results['results'])} accessible pages/databases")
        for item in results['results'][:5]:
            item_type = item['object']
            print(f"  - {item_type}: {item.get('id')[:8]}...")
        print()

        # Example: Create page (commented out to avoid actual creation)
        # print("Creating page...")
        # page = notion.create_page(
        #     parent_id="database-id-here",
        #     title="Test Page from Integration Framework",
        #     properties={
        #         "Status": {"select": {"name": "In Progress"}}
        #     }
        # )
        # print(f"Page created: {page['id']}\n")

        # # Add content to page
        # notion.append_blocks(
        #     block_id=page["id"],
        #     children=[
        #         notion.create_heading_block("Introduction", level=1),
        #         notion.create_paragraph_block("This page was created automatically!"),
        #         notion.create_todo_block("Task 1", checked=False),
        #         notion.create_code_block("print('Hello World')", language="python")
        #     ]
        # )
        # print("Content added to page\n")

    except Exception as e:
        print(f"Error: {e}\n")


def trello_example(framework):
    """Trello integration examples"""
    print("\n=== Trello Integration Examples ===\n")

    trello = framework.get("trello")

    if not trello or not trello.is_authenticated():
        print("Trello not configured. Skipping...")
        return

    try:
        # Get member info
        member = trello.get_member("me")
        print(f"Connected as: {member['username']} ({member['fullName']})\n")

        # List boards
        print("Listing boards...")
        boards = trello.list_boards()
        print(f"Your boards:")
        for board in boards[:5]:
            print(f"  - {board['name']}")
        print()

        if boards:
            # Get lists from first board
            board_id = boards[0]['id']
            print(f"Lists in '{boards[0]['name']}':")
            lists = trello.list_lists(board_id)
            for lst in lists:
                print(f"  - {lst['name']}")
            print()

            # Get cards from first list
            if lists:
                list_id = lists[0]['id']
                print(f"Cards in '{lists[0]['name']}':")
                cards = trello.get_cards_in_list(list_id)
                for card in cards[:5]:
                    print(f"  - {card['name']}")
                print()

        # Example: Create card (commented out to avoid actual creation)
        # if boards and lists:
        #     print("Creating card...")
        #     card = trello.create_card(
        #         list_id=lists[0]['id'],
        #         name="Test Card from Integration Framework",
        #         desc="This card was created automatically for testing."
        #     )
        #     print(f"Card created: {card['id']}\n")

        #     # Add checklist
        #     trello.add_checklist(
        #         card_id=card['id'],
        #         name="Tasks",
        #         items=["Task 1", "Task 2", "Task 3"]
        #     )
        #     print("Checklist added\n")

    except Exception as e:
        print(f"Error: {e}\n")


def test_all_integrations(framework):
    """Test all configured integrations"""
    print("\n=== Testing All Integrations ===\n")

    results = framework.test_all()

    for name, result in results.items():
        status = result.get('status', 'unknown')
        print(f"{name}: {status}")
        if status == "success":
            # Print additional info
            for key, value in result.items():
                if key != 'status':
                    print(f"  {key}: {value}")
        elif status == "error":
            print(f"  Error: {result.get('error', 'Unknown error')}")
        print()


def show_statistics(framework):
    """Show statistics for all integrations"""
    print("\n=== Integration Statistics ===\n")

    stats = framework.get_stats()

    for name, stat in stats.items():
        print(f"{name}:")
        print(f"  Total requests: {stat['total_requests']}")
        print(f"  Successful: {stat['successful_requests']}")
        print(f"  Failed: {stat['failed_requests']}")
        print(f"  Success rate: {stat['success_rate']}")
        print(f"  Rate limited: {stat['rate_limited']}")
        print(f"  Retries: {stat['retries']}")
        print(f"  Enabled: {stat['enabled']}")
        print(f"  Authenticated: {stat['authenticated']}")
        print()


def show_integration_info(framework):
    """Show information about all integrations"""
    print("\n=== Integration Information ===\n")

    for name in framework.list_available():
        info = framework.get_integration_info(name)
        print(f"{info['name']}:")
        print(f"  {info['description']}")
        print(f"\n  Capabilities:")
        for cap in info['capabilities']:
            print(f"    - {cap}")
        print(f"\n  Setup:")
        for step in info['setup_instructions']:
            print(f"    {step}")
        print()


def main():
    """Main example runner"""
    print("=" * 60)
    print("Integration Framework Examples")
    print("=" * 60)

    # Setup framework
    framework = setup_framework()

    # Show integration info
    show_integration_info(framework)

    # Test all integrations
    test_all_integrations(framework)

    # Run examples for each integration
    # Note: These will only run if integrations are properly configured

    gmail_example(framework)
    slack_example(framework)
    github_example(framework)
    notion_example(framework)
    trello_example(framework)

    # Show statistics
    show_statistics(framework)

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
