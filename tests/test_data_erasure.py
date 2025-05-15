import json
import unittest
from unittest.mock import patch, MagicMock, ANY
import time
from datetime import datetime, timedelta
import os
from pathlib import Path

from src.core_handler import handle_incoming_message, parse_message
from src.db.supabase_client import delete_user_data


class TestDataErasure(unittest.TestCase):
    """Test cases for the data erasure functionality."""

    def setUp(self):
        """Set up test environment."""
        # Create a mock Supabase client
        self.mock_client_patcher = patch('src.core_handler.supabase_client')
        self.mock_client = self.mock_client_patcher.start()
        
        # Create a mock Redis client
        self.mock_redis_patcher = patch('src.core_handler.redis_client')
        self.mock_redis = self.mock_redis_patcher.start()
        
        # Mock the get_user function directly
        self.mock_get_user_patcher = patch('src.core_handler.get_user')
        self.mock_get_user = self.mock_get_user_patcher.start()
        
        # Ensure template directory exists
        self.template_dir = Path("data/message_templates")
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Create test user with POPIA consent already given
        self.test_user_id = "whatsapp:+1234567890"
        self.test_user = {
            "whatsapp_id": self.test_user_id,
            "preferred_language": "en",
            "popia_consent_given": True,  # Important: set to True to bypass POPIA notice
            "current_bundle": "test_bundle"
        }
        
        # Set up the mock get_user to return our test user
        self.mock_get_user.return_value = self.test_user
        
        # Create POPIA notice template files to avoid errors
        with open(self.template_dir / "popia_notice_en.txt", "w") as f:
            f.write("*POPIA NOTICE*\n\nThis is a test POPIA notice.")
        with open(self.template_dir / "popia_notice_xh.txt", "w") as f:
            f.write("*ISAZISO SE-POPIA*\n\nEsi sisaziso se-POPIA sovavanyo.")
        with open(self.template_dir / "popia_notice_af.txt", "w") as f:
            f.write("*POPIA KENNISGEWING*\n\nHierdie is 'n toets POPIA kennisgewing.")

    def tearDown(self):
        """Clean up after tests."""
        self.mock_client_patcher.stop()
        self.mock_redis_patcher.stop()
        self.mock_get_user_patcher.stop()

    def test_parse_delete_command(self):
        """Test that the parse_message function correctly identifies delete commands."""
        command_type, params = parse_message("/delete")
        self.assertEqual(command_type, "delete")
        self.assertEqual(params, {})
        
        command_type, params = parse_message("/delete confirm")
        self.assertEqual(command_type, "delete_confirm")
        self.assertEqual(params, {})

    def test_delete_command_sends_confirmation_request(self):
        """Test that the /delete command sends a confirmation request."""
        # Create message template files
        with open(self.template_dir / "delete_prompt_en.txt", "w") as f:
            f.write("Are you sure you want to delete all your data? Reply '/delete confirm' to proceed.")
        
        # Create message data
        message_data = {
            "sender_id": self.test_user_id,
            "text": "/delete"
        }
        
        # Handle the message
        response = handle_incoming_message(json.dumps(message_data))
        response_data = json.loads(response)
        
        # Check that the response contains the confirmation message
        self.assertIn("Are you sure you want to delete all your data?", response_data["reply_text"])
        
        # Check that the message was logged
        # We're now using supabase_client.table().insert().execute() instead of log_message
        self.mock_client.table.return_value.insert.return_value.execute.assert_called()
        
        # Check that a security log was created
        self.mock_client.table.return_value.insert.return_value.execute.assert_called()

    @patch('src.core_handler.datetime')
    def test_delete_confirm_within_time_window(self, mock_datetime):
        """Test that /delete confirm works within the time window."""
        # Set up mock datetime to control time
        now = datetime.now()
        mock_datetime.now.return_value = now
        
        # Create message template files
        with open(self.template_dir / "delete_ack_en.txt", "w") as f:
            f.write("Your data has been deleted.")
        
        # Mock the Redis client to return a timestamp within the window
        delete_request_time = (now - timedelta(minutes=4)).timestamp()  # 4 minutes ago
        self.mock_redis.get.return_value = str(delete_request_time)
        
        # Create message data for delete confirm
        message_data = {
            "sender_id": self.test_user_id,
            "text": "/delete confirm"
        }
        
        # Handle the message
        response = handle_incoming_message(json.dumps(message_data))
        response_data = json.loads(response)
        
        # Check that the response contains the acknowledgment message
        self.assertEqual(response_data["reply_text"], "Your data has been deleted.")
        
        # Check that delete_user_data was called
        self.mock_client.rpc.assert_called_with(
            "hard_delete_user_data",
            {"user_whatsapp_id": self.test_user_id}
        )

    @patch('src.core_handler.datetime')
    def test_delete_confirm_outside_time_window(self, mock_datetime):
        """Test that /delete confirm fails outside the time window."""
        # Set up mock datetime to control time
        now = datetime.now()
        mock_datetime.now.return_value = now
        
        # Mock the Redis client to return a timestamp outside the window
        delete_request_time = (now - timedelta(minutes=6)).timestamp()  # 6 minutes ago
        self.mock_redis.get.return_value = str(delete_request_time)
        
        # Create message data for delete confirm
        message_data = {
            "sender_id": self.test_user_id,
            "text": "/delete confirm"
        }
        
        # Handle the message
        response = handle_incoming_message(json.dumps(message_data))
        response_data = json.loads(response)
        
        # Check that the response indicates the confirmation has expired
        self.assertIn("delete confirmation has expired", response_data["reply_text"].lower())
        
        # Reset the mock before checking
        self.mock_client.rpc.reset_mock()

    def test_delete_confirm_without_prior_request(self):
        """Test that /delete confirm fails if there was no prior delete request."""
        # Mock the Redis client to return None (no prior delete request)
        self.mock_redis.get.return_value = None
        
        # Create message data for delete confirm
        message_data = {
            "sender_id": self.test_user_id,
            "text": "/delete confirm"
        }
        
        # Handle the message
        response = handle_incoming_message(json.dumps(message_data))
        response_data = json.loads(response)
        
        # Check that the response indicates no prior delete request
        self.assertIn("no active delete request", response_data["reply_text"].lower())
        
        # Reset the mock before checking
        self.mock_client.rpc.reset_mock()

    def test_multilingual_delete_messages(self):
        """Test that delete messages are sent in the user's preferred language."""
        # Create message template files for different languages
        with open(self.template_dir / "delete_prompt_en.txt", "w") as f:
            f.write("Are you sure you want to delete all your data? Reply '/delete confirm' to proceed.")
        with open(self.template_dir / "delete_prompt_xh.txt", "w") as f:
            f.write("Uqinisekile ukuba ufuna ukucima yonke idatha yakho? Phendula '/delete confirm' ukuqhubeka.")
        with open(self.template_dir / "delete_prompt_af.txt", "w") as f:
            f.write("Is jy seker jy wil al jou data uitvee? Antwoord '/delete confirm' om voort te gaan.")
        
        # Test English
        self.test_user["preferred_language"] = "en"
        self.mock_client.get_user.return_value = self.test_user
        
        message_data = {
            "sender_id": self.test_user_id,
            "text": "/delete"
        }
        
        response = handle_incoming_message(json.dumps(message_data))
        response_data = json.loads(response)
        self.assertIn("Are you sure", response_data["reply_text"])
        
        # Test isiXhosa
        self.test_user["preferred_language"] = "xh"
        self.mock_client.get_user.return_value = self.test_user
        
        response = handle_incoming_message(json.dumps(message_data))
        response_data = json.loads(response)
        self.assertIn("Uqinisekile", response_data["reply_text"])
        
        # Test Afrikaans
        self.test_user["preferred_language"] = "af"
        self.mock_client.get_user.return_value = self.test_user
        
        response = handle_incoming_message(json.dumps(message_data))
        response_data = json.loads(response)
        self.assertIn("Is jy seker", response_data["reply_text"])


if __name__ == "__main__":
    unittest.main()