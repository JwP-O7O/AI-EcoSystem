import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add agent-zero to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "agent-zero")))

class TestChatInterfaceOverride(unittest.TestCase):

    # We patch the module directly.
    # When agent-zero is in path, we import `python.cli.chat_interface`.
    # `python` is a namespace package or just a folder.

    # Let's try patching relative to how we import it inside the test method.

    @patch('python.cli.chat_interface.AgentContext')
    @patch('python.cli.chat_interface.initialize')
    @patch('python.cli.chat_interface.console')
    @patch('python.cli.chat_interface.models')
    def test_start_chat_with_model_override(self, mock_models, mock_console, mock_initialize, mock_agent_context):
        from python.cli.chat_interface import start_chat
        import asyncio

        # Setup mocks
        mock_config = MagicMock()
        mock_initialize.return_value = mock_config

        mock_openai_chat = MagicMock()
        mock_models.get_openai_chat.return_value = mock_openai_chat

        # We need to break the infinite loop in start_chat
        mock_console.input.return_value = 'exit'

        # Run start_chat
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Call with override
        loop.run_until_complete(start_chat(model="openai/gpt-4o-test"))

        # Verify get_openai_chat was called
        mock_models.get_openai_chat.assert_called_with(model_name="gpt-4o-test", temperature=0)

        # Verify config was updated
        self.assertEqual(mock_config.chat_model, mock_openai_chat)
        self.assertEqual(mock_config.utility_model, mock_openai_chat)

        # Verify AgentContext was initialized with config
        mock_agent_context.assert_called_with(mock_config)

    @patch('python.cli.chat_interface.AgentContext')
    @patch('python.cli.chat_interface.initialize')
    @patch('python.cli.chat_interface.console')
    @patch('python.cli.chat_interface.models')
    def test_start_chat_without_model_override(self, mock_models, mock_console, mock_initialize, mock_agent_context):
        from python.cli.chat_interface import start_chat
        import asyncio

        # Setup mocks
        mock_config = MagicMock()
        mock_config.chat_model = "original_model"
        mock_initialize.return_value = mock_config

        mock_console.input.return_value = 'exit'

        # Run start_chat
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(start_chat(model=None))

        # Verify models functions NOT called
        mock_models.get_openai_chat.assert_not_called()

        # Verify config was NOT updated (remains "original_model")
        self.assertEqual(mock_config.chat_model, "original_model")

        # Verify AgentContext was initialized with config
        mock_agent_context.assert_called_with(mock_config)

if __name__ == '__main__':
    unittest.main()
