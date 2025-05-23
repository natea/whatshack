"""
Tests for POPIA notice presentation and consent logging functionality.

These tests verify that:
1. New users receive the POPIA notice
2. Users who haven't given consent receive the POPIA notice
3. "AGREE POPIA" messages update the user's consent status
4. POPIA notice dispatch is logged in the message_logs table
"""

import json
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, ANY

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_handler import handle_incoming_message
from src.db.supabase_client import update_user_popia_consent, log_message

@pytest.mark.unit
def test_new_user_receives_popia_notice():
    """Test that new users receive the POPIA notice."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.create_user') as mock_create_user, \
         patch('src.core_handler.get_content_file') as mock_get_content_file, \
         patch('src.core_handler.log_message') as mock_log_message:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist
        mock_create_user.return_value = {"data": [{"whatsapp_id": "test_user", "preferred_language": "en", "popia_consent_given": False}]}
        mock_get_content_file.return_value = "Welcome to Township Connect! To use our services, we need your consent under POPIA..."
        
        # Create a test message
        test_message = {
            'sender_id': 'test_user',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'test_user'
        assert "Welcome to Township Connect!" in result_data['reply_text']
        
        # Verify that the POPIA notice was logged
        mock_log_message.assert_any_call(
            mock_client,
            'test_user',
            'popia_notice_sent',
            ANY
        )

@pytest.mark.unit
def test_existing_user_without_consent_receives_popia_notice():
    """Test that existing users without POPIA consent receive the POPIA notice."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_content_file') as mock_get_content_file, \
         patch('src.core_handler.log_message') as mock_log_message:
        
        # Setup mocks
        mock_get_user.return_value = {"whatsapp_id": "test_user", "preferred_language": "en", "popia_consent_given": False}
        mock_get_content_file.return_value = "Welcome to Township Connect! To use our services, we need your consent under POPIA..."
        
        # Create a test message
        test_message = {
            'sender_id': 'test_user',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'test_user'
        assert "Welcome to Township Connect!" in result_data['reply_text']
        
        # Verify that the POPIA notice was logged
        mock_log_message.assert_any_call(
            mock_client,
            'test_user',
            'popia_notice_sent',
            ANY
        )

@pytest.mark.unit
def test_agree_popia_updates_consent():
    """Test that 'AGREE POPIA' messages update the user's consent status."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.update_user_popia_consent') as mock_update_consent, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.log_message') as mock_log_message:
        
        # Setup mocks
        mock_get_user.return_value = {"whatsapp_id": "test_user_agreeing", "preferred_language": "en", "popia_consent_given": False}
        mock_get_template.return_value = "Welcome to Township Connect!"
        
        # Create a test message with "AGREE POPIA"
        test_message = {
            'sender_id': 'test_user_agreeing',
            'text': 'AGREE POPIA'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'test_user_agreeing'
        assert "Thank you for your consent" in result_data['reply_text']
        
        # Verify that update_user_popia_consent was called with the correct parameters
        mock_update_consent.assert_called_with(mock_client, 'test_user_agreeing', True)
        
        # Verify that the consent was logged
        mock_log_message.assert_any_call(
            mock_client,
            'test_user_agreeing',
            'popia_consent_recorded',
            'User agreed to POPIA'
        )

@pytest.mark.unit
def test_popia_notice_logging():
    """Test that POPIA notice dispatch is logged in the message_logs table."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_content_file') as mock_get_content_file, \
         patch('src.core_handler.log_message') as mock_log_message:
        
        # Setup mocks
        mock_get_user.return_value = {"whatsapp_id": "test_user_popia_notice_sent", "preferred_language": "en", "popia_consent_given": False}
        mock_get_content_file.return_value = "Welcome to Township Connect! To use our services, we need your consent under POPIA..."
        
        # Create a test message
        test_message = {
            'sender_id': 'test_user_popia_notice_sent',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Verify that the POPIA notice was logged with the specific message type
        mock_log_message.assert_any_call(
            mock_client,
            'test_user_popia_notice_sent',
            'popia_notice_sent',
            f'POPIA notice sent in en'
        )
        
        # Verify that the actual outbound message was logged
        mock_log_message.assert_any_call(
            mock_client,
            'test_user_popia_notice_sent',
            'outbound',
            "Welcome to Township Connect! To use our services, we need your consent under POPIA...",
            ANY  # We don't need to check the exact size
        )

# @pytest.mark.skip(reason="Integration test requires proper Supabase setup with RLS policies and SERVICE_KEY") # Unskip
@pytest.mark.integration
def test_supabase_popia_consent_update_and_logging(): # Renamed for clarity
    """Integration test for updating POPIA consent and logging notice dispatch in Supabase."""
    # This test requires a real Supabase connection with SUPABASE_SERVICE_KEY configured
    
    from src.db.supabase_client import get_service_client, create_user, get_user, update_user_popia_consent, log_message, delete_user_data
    import os
    
    # Check if required environment variables are set
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_service_key = os.environ.get("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_service_key:
        pytest.skip(
            "Skipping integration test: SUPABASE_URL and/or SUPABASE_SERVICE_KEY environment variables not set. "
            "Set these variables in your environment or create a tests/.env.test file."
        )
    
    try:
        # Get a Supabase client using the service key to bypass RLS for testing
        client = get_service_client()
        
        test_user_id = "test_popia_integration_user"
        test_message_content = "POPIA notice sent to user during test"
        # Ensure user does not exist or clean up from previous failed run
        delete_user_data(client, test_user_id)

        # 1. Create a test user with popia_consent_given = False
        create_user_response = create_user(client, test_user_id, "en", False)
        assert create_user_response.get("error") is None, f"Failed to create user: {create_user_response.get('error')}"
        created_user = get_user(client, test_user_id)
        assert created_user is not None
        assert created_user.get("popia_consent_given") is False # get_user returns a dict, so .get() is fine here

        # 2. Update the user's POPIA consent to True
        update_response = update_user_popia_consent(client, test_user_id, True)
        assert update_response.get("error") is None, f"Failed to update consent: {update_response.get('error')}"
        
        # 3. Verify popia_consent_given is True
        updated_user = get_user(client, test_user_id) # get_user returns a dict
        assert updated_user is not None
        assert updated_user.get("popia_consent_given") is True, "POPIA consent was not updated to True in the users table."

        # 4. Log a POPIA notice dispatch message for this user
        # In a real scenario, core_handler would do this. We simulate it here for direct DB verification.
        # The actual message_type logged by core_handler for POPIA notice is 'popia_notice_sent'
        log_response = log_message(client, test_user_id, "outbound", test_message_content, data_size_kb=0.1)
        assert log_response.get("error") is None, f"Failed to log message: {log_response.get('error')}"
        
        # 5. Verify the POPIA notice dispatch was logged in message_logs
        # We need to select from message_logs where user_whatsapp_id = test_user_id and message_content matches
        query_response = client.table("message_logs").select("*").eq("user_whatsapp_id", test_user_id).eq("message_content", test_message_content).order("timestamp", desc=True).limit(1).execute()
        
        # Safely check for error attribute on the direct APIResponse
        query_error = getattr(query_response, 'error', None)
        error_message_detail = query_error.message if query_error and hasattr(query_error, 'message') else str(query_error)
        assert query_error is None, f"Error querying message_logs: {error_message_detail}"
        
        assert query_response.data, f"No message logs found for user {test_user_id} with content '{test_message_content}'. Response error: {error_message_detail}"
        assert len(query_response.data) > 0, "Message log for POPIA notice not found."
        
        logged_message = query_response.data[0] # query_response.data is a list of dicts
        assert logged_message.get("user_whatsapp_id") == test_user_id
        assert logged_message.get("direction") == "outbound"
        assert logged_message.get("message_content") == test_message_content, "Logged message content does not match."

        # Clean up
        delete_user_data(client, test_user_id)
        
    except ValueError as e:
        pytest.fail(f"Supabase client initialization failed: {str(e)}")
    except Exception as e:
        pytest.fail(f"Integration test failed: {str(e)}")