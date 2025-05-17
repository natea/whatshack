"""
Tests for user management functionality in Township Connect.

These tests verify that the user identification and creation functionality works correctly,
including creating new users and retrieving existing user data.
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock, call

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_handler import handle_incoming_message

@pytest.mark.unit
def test_new_user_creation():
    """Test that a new user is created when a message is received from an unknown sender."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.create_user') as mock_create_user, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.detect_initial_language') as mock_detect_language:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist
        mock_get_template.return_value = "POPIA NOTICE: This is a test notice."
        mock_detect_language.return_value = "en"  # Mock the language detection to return English
        
        # Create a test message
        test_message = {
            'sender_id': 'new_test_user_id',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Verify that get_user was called with the correct parameters
        mock_get_user.assert_called_once_with(mock_client, 'new_test_user_id')
        
        # Verify that create_user was called with the correct parameters
        mock_create_user.assert_called_once()
        
        # Verify the first two arguments (client and sender_id)
        args, kwargs = mock_create_user.call_args
        assert args[0] == mock_client
        assert args[1] == 'new_test_user_id'
        assert args[2] == "en"  # Verify the detected language is passed
        
        # Verify that the default value for popia_consent is False
        assert kwargs.get('popia_consent', None) is False

@pytest.mark.unit
def test_existing_user_retrieval():
    def test_existing_user_retrieval():
        """Test that existing user data is retrieved when a message is received from a known sender."""
        # Mock the Supabase client and functions
        with patch('src.core_handler.supabase_client') as mock_client, \
             patch('src.core_handler.get_user') as mock_get_user, \
             patch('src.core_handler.create_user') as mock_create_user, \
             patch('src.core_handler.get_message_template') as mock_get_template, \
             patch('src.core_handler.log_message') as mock_log_message, \
             patch('src.core_handler.logger') as mock_logger:
            
            # Setup mocks
            mock_user = {
                'whatsapp_id': 'existing_user_id',
                'preferred_language': 'xh',
                'popia_consent_given': True,
                'current_bundle': 'test_bundle'  # Add a bundle to avoid bundle selection prompt
            }
            mock_get_user.return_value = mock_user
            mock_get_template.return_value = "Welcome to Township Connect!"
            
            # Create a test message
            test_message = {
                'sender_id': 'existing_user_id',
                'text': 'Hello'
            }
            
            # Call the function
            result = handle_incoming_message(json.dumps(test_message))
            
            # Verify that get_user was called with the correct parameters
            mock_get_user.assert_called_once_with(mock_client, 'existing_user_id')
            
            # Verify that create_user was NOT called
            mock_create_user.assert_not_called()
            
            # Verify that the user's preferred language and POPIA consent status were retrieved
            # Check that the logger was called with the correct message
            mock_logger.info.assert_any_call(f"Retrieved existing user existing_user_id with language xh and POPIA consent: True")
            
            # Parse the result
            result_data = json.loads(result)
            
            # Verify the result
            assert 'reply_to' in result_data
            assert 'reply_text' in result_data
            assert result_data['reply_to'] == 'existing_user_id'
            
            # Since the user has already given POPIA consent, they should receive the welcome message
            assert "Welcome to Township Connect!" in result_data['reply_text']
@pytest.mark.unit
def test_user_language_retrieval():
    """Test that the user's preferred language is retrieved correctly."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.logger') as mock_logger:
        
        # Setup mocks for a user with Xhosa as preferred language
        mock_user = {
            'whatsapp_id': 'xhosa_user_id',
            'preferred_language': 'xh',
            'popia_consent_given': True,
            'current_bundle': 'test_bundle'  # Add a bundle to avoid bundle selection prompt
        }
        mock_get_user.return_value = mock_user
        
        # Create a test message
        test_message = {
            'sender_id': 'xhosa_user_id',
            'text': 'Molo'  # Hello in Xhosa
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Verify that get_user was called with the correct parameters
        mock_get_user.assert_called_once_with(mock_client, 'xhosa_user_id')
        
        # Verify that the user's preferred language was retrieved correctly
        mock_logger.info.assert_any_call("Retrieved existing user xhosa_user_id with language xh and POPIA consent: True")
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'xhosa_user_id'
        
        # Since the user has POPIA consent and a bundle, the message is echoed back
        assert "Echo: Molo" in result_data['reply_text']

@pytest.mark.unit
def test_popia_consent_retrieval():
    """Test that the user's POPIA consent status is retrieved correctly."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles, \
         patch('src.core_handler.generate_bundle_selection_prompt') as mock_generate_prompt:
        
        # Setup mocks for a user who has given POPIA consent but hasn't selected a bundle
        mock_user = {
            'whatsapp_id': 'consent_user_id',
            'preferred_language': 'en',
            'popia_consent_given': True,
            'current_bundle': None
        }
        mock_get_user.return_value = mock_user
        mock_get_bundles.return_value = [{'bundle_id': 'bundle1', 'bundle_name_en': 'Test Bundle'}]
        mock_generate_prompt.return_value = "Please select a bundle:"
        
        # Create a test message
        test_message = {
            'sender_id': 'consent_user_id',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Verify that get_user was called with the correct parameters
        mock_get_user.assert_called_once_with(mock_client, 'consent_user_id')
        
        # Verify that get_service_bundles was called (since user has given consent but hasn't selected a bundle)
        mock_get_bundles.assert_called_once_with(mock_client)
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'consent_user_id'
        assert "Please select a bundle:" in result_data['reply_text']

@pytest.mark.unit
def test_user_creation_verification_count():
    """Test that the user creation is verified with a SQL count query."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.create_user') as mock_create_user, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.detect_initial_language') as mock_detect_language, \
         patch('src.core_handler.logger') as mock_logger:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist
        mock_get_template.return_value = "POPIA NOTICE: This is a test notice."
        mock_detect_language.return_value = "en"  # Mock the language detection to return English
        
        # Mock the Supabase client to not be a MockSupabaseClient
        mock_client.__class__.__name__ = "SupabaseClient"
        
        # Mock the table.select.eq.execute method to return a count of 1
        mock_execute_result = MagicMock()
        mock_execute_result.data = [{"count": 1}]
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value = mock_execute_result
        mock_client.table.return_value = mock_table
        
        # Create a test message
        test_message = {
            'sender_id': 'new_test_user_id',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Verify that get_user was called with the correct parameters
        mock_get_user.assert_called_once_with(mock_client, 'new_test_user_id')
        
        # Verify that create_user was called with the correct parameters
        mock_create_user.assert_called_once()
        
        # Verify that the SQL count query was logged
        mock_logger.info.assert_any_call(f"Verification: SELECT COUNT(*) FROM users WHERE whatsapp_id = 'new_test_user_id' returned 1")