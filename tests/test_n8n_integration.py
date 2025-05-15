"""
Tests for n8n integration with core handler.

These tests verify that the core message handling functionality works correctly
with the n8n workflow format for Twilio WhatsApp integration.
"""

import json
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, ANY

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_handler import handle_incoming_message

@pytest.fixture
def n8n_message_format():
    """Sample message in the format sent by n8n from Twilio."""
    return json.dumps({
        "message": {
            "from": "whatsapp:+27123456789",
            "to": "whatsapp:+14155238886",
            "body": "Hello Bot",
            "messageId": "SM123456789",
            "numMedia": "0",
            "timestamp": "2025-05-14T23:30:00.000Z"
        }
    })

@pytest.mark.unit
def test_handle_n8n_message_format(n8n_message_format):
    """Test that the handle_incoming_message function works with n8n message format."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_get_user.return_value = {'preferred_language': 'en', 'popia_consent_given': True}
        mock_get_template.return_value = "Welcome to Township Connect!"
        
        # Call the function
        result = handle_incoming_message(n8n_message_format)
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result format expected by n8n
        assert 'status' in result_data, f"Expected 'status' in {result_data}"
        assert result_data['status'] == 200
        assert 'response' in result_data
        assert 'message' in result_data['response']
        assert "Welcome to Township Connect!" in result_data['response']['message']

@pytest.mark.unit
def test_handle_n8n_message_echo_reply(n8n_message_format):
    """Test that the handle_incoming_message function returns an echo reply for n8n."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_get_user.return_value = {'preferred_language': 'en', 'popia_consent_given': True}
        mock_get_template.return_value = "Echo: Hello Bot"
        
        # Call the function
        result = handle_incoming_message(n8n_message_format)
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the echo reply
        assert 'status' in result_data, f"Expected 'status' in {result_data}"
        assert result_data['status'] == 200
        assert 'response' in result_data, f"Expected 'response' in {result_data}"
        assert 'message' in result_data['response']
        assert "Echo: Hello Bot" in result_data['response']['message']

@pytest.mark.unit
def test_handle_n8n_message_logging(n8n_message_format):
    """Test that messages from n8n are logged to Supabase."""
    # Mock the Supabase client and log_message function
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_get_user.return_value = {'preferred_language': 'en', 'popia_consent_given': True}
        mock_get_template.return_value = "Echo: Hello Bot"
        
        # Call the function
        result = handle_incoming_message(n8n_message_format)
        
        # Verify that log_message was called with the correct parameters
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+27123456789',
            'inbound',
            'Hello Bot',
            ANY  # We don't need to check the exact size
        )
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result format
        assert 'status' in result_data, f"Expected 'status' in {result_data}"
        assert result_data['status'] == 200
        
        # Verify that the outbound message was also logged
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+27123456789',
            'outbound',
            ANY,  # The exact response text
            ANY   # We don't need to check the exact size
        )

@pytest.mark.unit
def test_handle_n8n_message_error():
    """Test that the handle_incoming_message function handles errors with n8n format."""
    # Call the function with invalid JSON
    result = handle_incoming_message("This is not JSON")
    
    # Parse the result
    result_data = json.loads(result)
    
    # Verify the result format expected by n8n
    assert 'status' in result_data, f"Expected 'status' in {result_data}"
    assert result_data['status'] == 400
    assert 'error' in result_data, f"Expected 'error' in {result_data}"
    assert "couldn't process your message" in result_data['error']