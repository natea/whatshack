"""
Tests for core handler functionality in Township Connect.

These tests verify that the core message handling functionality works correctly,
including parsing messages, generating responses, and handling errors.
"""

import json
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, ANY
from unittest import mock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.core_handler
from src.core_handler import (
    handle_incoming_message, parse_message, generate_response,
    get_message_template
)

@pytest.mark.unit
def test_handle_incoming_message_basic(sample_message_json):
    """Test that the handle_incoming_message function works for basic messages."""
    # Call the function
    result = handle_incoming_message(sample_message_json)
    
    # Parse the result
    result_data = json.loads(result)
    
    # Verify the result
    assert 'reply_to' in result_data
    assert 'reply_text' in result_data
    assert result_data['reply_to'] == 'whatsapp:+27123456789'
    # New users get POPIA notice first
    assert 'POPIA NOTICE' in result_data['reply_text']
    
    # Test with an existing user who has already given POPIA consent
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mock user
        mock_user = {'preferred_language': 'en', 'popia_consent_given': True}
        mock_get_user.return_value = mock_user
        mock_get_template.return_value = "Welcome to Township Connect!"
        
        # Call the function
        result = handle_incoming_message(sample_message_json)
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        # Existing users with POPIA consent get welcome message
        assert 'Welcome to Township Connect' in result_data['reply_text']

@pytest.mark.unit
def test_handle_incoming_message_empty():
    """Test that the handle_incoming_message function handles empty messages."""
    # Create an empty message
    empty_message = {
        'sender_id': 'whatsapp:+27123456789',
        'text': ''
    }
    
    # Call the function
    result = handle_incoming_message(json.dumps(empty_message))
    
    # Parse the result
    result_data = json.loads(result)
    
    # Verify the result
    assert 'reply_to' in result_data
    assert 'reply_text' in result_data
    assert result_data['reply_to'] == 'whatsapp:+27123456789'
    # New users get POPIA notice first, even for empty messages
    assert 'POPIA NOTICE' in result_data['reply_text']

@pytest.mark.unit
def test_handle_incoming_message_invalid_json():
    """Test that the handle_incoming_message function handles invalid JSON."""
    # Call the function with invalid JSON
    result = handle_incoming_message("This is not JSON")
    
    # Parse the result
    result_data = json.loads(result)
    
    # Verify the result
    assert 'reply_to' in result_data
    assert 'reply_text' in result_data
    assert result_data['reply_to'] == 'unknown'
    assert "Sorry" in result_data['reply_text']

@pytest.mark.unit
def test_parse_message():
    """Test that the parse_message function correctly parses messages."""
    # Test a simple echo message
    command_type, params = parse_message("Hello")
    assert command_type == "echo"
    assert params["text"] == "Hello"
    
    # Test a language command
    command_type, params = parse_message("/lang xh")
    assert command_type == "language"
    assert params["language"] == "xh"
    
    # Test the delete command
    command_type, params = parse_message("/delete")
    assert command_type == "delete"
    assert params == {}
    
    # Test the delete confirmation command
    command_type, params = parse_message("/delete confirm")
    assert command_type == "delete_confirm"
    assert params == {}
    
    # Test with leading/trailing whitespace
    command_type, params = parse_message("  Hello  ")
    assert command_type == "echo"
    # The parse_message function now strips whitespace
    assert params["text"] == "Hello"

@pytest.mark.parametrize("message_text,expected_response", [
    ("Hello", "Welcome to Township Connect"),
    ("Test", "Welcome to Township Connect"),
    ("123", "Welcome to Township Connect"),
    ("!@#$%^", "Welcome to Township Connect"),
])
@pytest.mark.unit
def test_handle_incoming_message_various_texts(message_text, expected_response):
    """Test that the handle_incoming_message function works for various message texts."""
    # Create a test message
    test_message = {
        'sender_id': 'whatsapp:+27123456789',
        'text': message_text
    }
    
    # Call the function
    result = handle_incoming_message(json.dumps(test_message))
    
    # Parse the result
    result_data = json.loads(result)
    
    # Verify the result
    assert 'reply_to' in result_data
    assert 'reply_text' in result_data
    assert result_data['reply_to'] == 'whatsapp:+27123456789'
    # New users get POPIA notice first
    assert 'POPIA NOTICE' in result_data['reply_text']

@pytest.mark.parametrize("command,expected_response,language", [
    ("/lang en", "Language set to English", "xh"),
    ("/lang xh", "Ulwimi lusetelwe kwiXhosa", "en"),
    ("/lang af", "Taal ingestel op Afrikaans", "en"),
    ("/delete", "Are you sure you want to delete all your data", "en"),
    ("/delete confirm", "Your data has been deleted", "en"),
])
@pytest.mark.unit
def test_handle_incoming_message_commands(command, expected_response, language):
    """Test that the handle_incoming_message function handles various commands correctly."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user:
        
        # Setup mock user
        mock_user = {'preferred_language': language}
        mock_get_user.return_value = mock_user
        
        # Create a test message
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': command
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert expected_response in result_data['reply_text']

@pytest.mark.unit
def test_generate_response():
    """Test that the generate_response function generates correct responses."""
    # Mock the message template function
    with patch('src.core_handler.get_message_template') as mock_get_template:
        mock_get_template.return_value = "Welcome to Township Connect!"
        
        # Test echo response (should return welcome template)
        response = generate_response("echo", {"text": "Hello"}, "whatsapp:+27123456789", "en")
        assert "Welcome to Township Connect!" in response
        mock_get_template.assert_called_with("welcome_en.txt")
        
        # Test language response
        response = generate_response("language", {"language": "xh"}, "whatsapp:+27123456789", "en")
        assert "Ulwimi lusetelwe kwiXhosa" in response
        
        # Test delete response
        response = generate_response("delete", {}, "whatsapp:+27123456789", "en")
        assert "Are you sure you want to delete all your data" in response
        
        # Test delete confirmation response
        response = generate_response("delete_confirm", {}, "whatsapp:+27123456789", "en")
        assert "Your data has been deleted" in response
        
        # Test POPIA agreement response
        response = generate_response("popia_agree", {}, "whatsapp:+27123456789", "en")
        assert "Thank you for your consent" in response
        assert "Welcome to Township Connect!" in response
        
        # Test unknown command
        response = generate_response("unknown", {}, "whatsapp:+27123456789", "en")
        assert "Unknown command: unknown" in response

@pytest.mark.unit
def test_get_message_template():
    """Test that the get_message_template function loads templates correctly."""
    # Create a temporary template file for testing
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the original template directory
        original_template_dir = src.core_handler.TEMPLATE_DIR
        
        try:
            # Set the template directory to the temporary directory
            src.core_handler.TEMPLATE_DIR = Path(temp_dir)
            
            # Create a test template file
            test_template_path = Path(temp_dir) / "test_template.txt"
            with open(test_template_path, 'w', encoding='utf-8') as f:
                f.write("This is a test template.")
            
            # Test loading an existing template
            template_content = get_message_template("test_template.txt")
            assert template_content == "This is a test template."
            
            # Test loading a non-existent template
            template_content = get_message_template("non_existent.txt")
            assert "not found" in template_content
            
        finally:
            # Restore the original template directory
            src.core_handler.TEMPLATE_DIR = original_template_dir

@pytest.mark.unit
def test_new_user_popia_notice():
    """Test that new users receive a POPIA notice."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist
        mock_get_template.return_value = "POPIA NOTICE: This is a test notice."
        
        # Create a test message
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert "POPIA NOTICE" in result_data['reply_text']
        mock_get_template.assert_called_with("popia_notice_en.txt")

@pytest.mark.unit
def test_popia_agreement():
    """Test that POPIA agreement is handled correctly."""
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_get_user.return_value = {'preferred_language': 'en'}  # User exists
        mock_get_template.return_value = "Welcome to Township Connect!"
        
        # Create a test message
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'AGREE POPIA'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert "Thank you for your consent" in result_data['reply_text']
        assert "Welcome to Township Connect!" in result_data['reply_text']

@pytest.mark.unit
def test_message_logging_to_supabase():
    """Test that messages are logged to Supabase."""
    # Mock the Supabase client and log_message function
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_get_user.return_value = {'preferred_language': 'en', 'popia_consent_given': True}
        mock_get_template.return_value = "Welcome to Township Connect!"
        
        # Create a test message
        test_message = {
            'sender_id': 'whatsapp:+12345',
            'text': 'Test Message'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Verify that log_message was called with the correct parameters
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+12345',
            'inbound',
            'Test Message',
            ANY  # We don't need to check the exact size
        )
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result format
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+12345'
        assert "Welcome to Township Connect!" in result_data['reply_text']
        
        # Verify that the outbound message was also logged
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+12345',
            'outbound',
            ANY,  # The exact response text
            ANY   # We don't need to check the exact size
        )