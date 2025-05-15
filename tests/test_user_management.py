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
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist
        mock_get_template.return_value = "POPIA NOTICE: This is a test notice."
        
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
        # The detected language might vary, so we just check that create_user was called
        mock_create_user.assert_called_once()
        
        # Verify the first two arguments (client and sender_id)
        args, _ = mock_create_user.call_args
        assert args[0] == mock_client
        assert args[1] == 'new_test_user_id'
        
        # Verify that the default values for preferred_language and popia_consent are correct
        # The third argument is the detected language, which we can't predict exactly
        # The fourth argument should be False for popia_consent
        _, kwargs = mock_create_user.call_args
        assert kwargs.get('popia_consent', False) is False

@pytest.mark.unit
def test_existing_user_retrieval():
    """Test that existing user data is retrieved when a message is received from a known sender."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.create_user') as mock_create_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_user = {
            'whatsapp_id': 'existing_user_id',
            'preferred_language': 'xh',
            'popia_consent_given': True
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
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks for a user with Xhosa as preferred language
        mock_user = {
            'whatsapp_id': 'xhosa_user_id',
            'preferred_language': 'xh',
            'popia_consent_given': True,
            'current_bundle': 'test_bundle'  # Add a bundle to avoid bundle selection prompt
        }
        mock_get_user.return_value = mock_user
        mock_get_template.return_value = "Wamkelekile kwiTownship Connect!"  # Xhosa welcome message
        
        # Create a test message
        test_message = {
            'sender_id': 'xhosa_user_id',
            'text': 'Molo'  # Hello in Xhosa
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Verify that get_user was called with the correct parameters
        mock_get_user.assert_called_once_with(mock_client, 'xhosa_user_id')
        
        # Verify that the correct template was requested (Xhosa welcome message)
        mock_get_template.assert_any_call("welcome_xh.txt")
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'xhosa_user_id'
        assert "Wamkelekile kwiTownship Connect!" in result_data['reply_text']

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