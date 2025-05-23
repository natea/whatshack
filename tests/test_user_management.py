"""
Tests for user management functionality in Township Connect.

These tests verify that the user identification and creation functionality works correctly,
including checking if a user exists, creating new users, and retrieving user details.
"""

import json
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, ANY
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_handler import handle_incoming_message
from src.db.supabase_client import get_user, create_user

@pytest.mark.unit
def test_new_user_creation(sample_message_json):
    """Test that a new user is created when a message is received from an unknown sender_id."""
    # Mock the Supabase client and related functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.create_user') as mock_create_user, \
         patch('src.core_handler.get_content_file') as mock_get_content_file, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist
        mock_get_content_file.return_value = "Content file not found"
        mock_get_template.return_value = "POPIA NOTICE: This is a test notice."
        
        # Parse the sample message to get the sender_id
        message_data = json.loads(sample_message_json)
        sender_id = message_data.get('sender_id', '')
        
        # Call the function
        handle_incoming_message(sample_message_json)
        
        # Verify that create_user was called with the correct parameters
        mock_create_user.assert_called_once()
        args, kwargs = mock_create_user.call_args
        
        # Check that the client and sender_id were passed correctly
        assert args[0] == mock_client  # First arg should be the client
        assert args[1] == sender_id    # Second arg should be the sender_id
        
        # Check that default language was detected and passed
        assert len(args) >= 3
        assert args[2] in ['en', 'xh', 'af']  # Third arg should be the detected language
        
        # Check that POPIA consent was set to False by default
        assert kwargs.get('popia_consent') is False or (len(args) >= 4 and args[3] is False)

@pytest.mark.unit
def test_existing_user_retrieval(sample_message_json):
    """Test that existing user details are retrieved when a message is received from a known sender_id."""
    # Mock the Supabase client and related functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mock user with specific language and POPIA consent
        mock_user = {
            'preferred_language': 'xh',
            'popia_consent_given': True,
            'current_bundle': 'test_bundle'  # Add a bundle to avoid bundle selection prompt
        }
        mock_get_user.return_value = mock_user
        
        # Parse the sample message to get the sender_id
        message_data = json.loads(sample_message_json)
        sender_id = message_data.get('sender_id', '')
        
        # Call the function
        handle_incoming_message(sample_message_json)
        
        # Verify that get_user was called with the correct parameters
        mock_get_user.assert_called_once_with(mock_client, sender_id)
        
        # Verify that the user's language and POPIA consent were retrieved
        # This is implicit in the fact that we're using the mock_user values in the function

@pytest.mark.unit
def test_user_creation_with_supabase_client():
    """Test the create_user function directly to ensure it sets all required fields."""
    # Create a mock Supabase client
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_insert = MagicMock()
    mock_execute = MagicMock()
    
    mock_client.table.return_value = mock_table
    mock_table.insert.return_value = mock_insert
    mock_insert.execute.return_value = {"data": [{"whatsapp_id": "test_user"}], "error": None}
    
    # Call create_user
    whatsapp_id = "whatsapp:+27123456789"
    preferred_language = "en"
    popia_consent = False
    
    result = create_user(mock_client, whatsapp_id, preferred_language, popia_consent)
    
    # Verify the client interactions
    mock_client.table.assert_called_once_with("users")
    mock_table.insert.assert_called_once()
    
    # Get the user data that was passed to insert
    insert_args, _ = mock_table.insert.call_args
    user_data = insert_args[0]
    
    # Verify all required fields are present
    assert user_data["whatsapp_id"] == whatsapp_id
    assert user_data["preferred_language"] == preferred_language
    assert user_data["popia_consent_given"] == popia_consent
    assert "created_at" in user_data
    assert "last_active_at" in user_data

@pytest.mark.unit
def test_user_creation_with_different_languages(sample_language_messages):
    """Test that users are created with the correct detected language based on their initial message."""
    for language, message_text in sample_language_messages.items():
        # Create a test message with the language-specific greeting
        test_message = {
            'sender_id': f'whatsapp:+27{language}12345',  # Use language in the ID to make each test unique
            'text': message_text
        }
        
        # Mock the Supabase client and related functions
        with patch('src.core_handler.supabase_client') as mock_client, \
             patch('src.core_handler.get_user') as mock_get_user, \
             patch('src.core_handler.create_user') as mock_create_user, \
             patch('src.core_handler.get_content_file') as mock_get_content_file, \
             patch('src.core_handler.get_message_template') as mock_get_template, \
             patch('src.core_handler.publish_to_redis_stream') as mock_publish:
            
            # Setup mocks
            mock_get_user.return_value = None  # User doesn't exist
            mock_get_content_file.return_value = "Content file not found"
            mock_get_template.return_value = "POPIA NOTICE: This is a test notice."
            
            # Call the function
            handle_incoming_message(json.dumps(test_message))
            
            # Verify that create_user was called with the correct language
            mock_create_user.assert_called_once()
            args, _ = mock_create_user.call_args
            
            # The detected language should match the expected language
            assert args[2] == language

@pytest.mark.unit
def test_user_last_active_timestamp_update():
    """Test that the last_active_at timestamp is updated when a user is created."""
    # Create a mock Supabase client
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_insert = MagicMock()
    mock_execute = MagicMock()
    
    mock_client.table.return_value = mock_table
    mock_table.insert.return_value = mock_insert
    mock_insert.execute.return_value = {"data": [{"whatsapp_id": "test_user"}], "error": None}
    
    # Call create_user
    whatsapp_id = "whatsapp:+27123456789"
    
    # Get the current time before calling create_user
    from datetime import datetime
    before_time = datetime.now()
    
    result = create_user(mock_client, whatsapp_id)
    
    # Get the current time after calling create_user
    after_time = datetime.now()
    
    # Get the user data that was passed to insert
    insert_args, _ = mock_table.insert.call_args
    user_data = insert_args[0]
    
    # Parse the timestamps from the user data
    from datetime import datetime
    created_at = datetime.fromisoformat(user_data["created_at"].replace('Z', '+00:00'))
    last_active_at = datetime.fromisoformat(user_data["last_active_at"].replace('Z', '+00:00'))
    
    # Verify the timestamps are between before_time and after_time
    # Note: This is a simplified check and might fail if the test runs very slowly
    assert before_time <= created_at <= after_time
    assert before_time <= last_active_at <= after_time
    
    # Verify created_at and last_active_at are very close for a new user
    # They might be microseconds apart due to the way they're generated
    time_difference = abs((created_at - last_active_at).total_seconds())
    assert time_difference < 0.1  # Less than 100 milliseconds difference