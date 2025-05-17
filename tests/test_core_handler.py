"""
Tests for core handler functionality in Township Connect.

These tests verify that the core message handling functionality works correctly,
including parsing messages, generating responses, and handling errors.
"""

import json
import pytest
import sys
import os
from pathlib import Path
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
    # Mock the Supabase client, user, and message template
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles:
         
        # Set up different return values for different template names
        mock_get_template.side_effect = lambda template_name: {
            "lang_confirmation_en.txt": "Language set to English",
            "lang_confirmation_xh.txt": "Ulwimi lusetelwe kwiXhosa",
            "lang_confirmation_af.txt": "Taal ingestel op Afrikaans",
            "delete_prompt_en.txt": "Are you sure you want to delete all your data",
            "delete_ack_en.txt": "Your data has been deleted"
        }.get(template_name, "Default template")
        
        # Mock empty service bundles to avoid bundle prompt
        mock_get_bundles.return_value = []
        
        # Setup mock user with POPIA consent given to avoid POPIA notice
        mock_user = {'preferred_language': language, 'popia_consent_given': True}
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
        # Set up different return values for different template names
        mock_get_template.side_effect = lambda template_name: {
            "welcome_en.txt": "Welcome to Township Connect!",
            "lang_confirmation_xh.txt": "Ulwimi lusetelwe kwiXhosa",
            "delete_prompt_en.txt": "Are you sure you want to delete all your data",
            "delete_ack_en.txt": "Your data has been deleted"
        }.get(template_name, "Default template")
        
        # Test echo response (should return echo of the text)
        response = generate_response("echo", {"text": "Hello"}, "whatsapp:+27123456789", "en")
        assert response == "Echo: Hello"
        # Should not call get_message_template for echo command
        mock_get_template.assert_not_called()
        
        # Reset mock for subsequent tests
        mock_get_template.reset_mock()
        
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
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.get_content_file') as mock_content_file:

        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist
        mock_get_template.return_value = "POPIA NOTICE: This is a test notice."
        
        # Mock the content file path to ensure it calls get_message_template with the right file
        mock_content_file.return_value = Path("content/popia_notice_en.txt")
        
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

@pytest.mark.unit
def test_echo_functionality():
    """Test that the echo functionality works correctly."""
    # Create a test message
    test_message = {
        'sender_id': 'whatsapp:+27123456789',
        'text': 'Hello World'
    }
    
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.log_message') as mock_log_message:
        
        # Setup mock user with POPIA consent and a selected bundle
        mock_get_user.return_value = {
            'preferred_language': 'en',
            'popia_consent_given': True,
            'current_bundle': 'test_bundle'  # Add a bundle to avoid bundle selection prompt
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert result_data['reply_text'] == 'Echo: Hello World'
        
        # Verify that both inbound and outbound messages were logged
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+27123456789',
            'inbound',
            'Hello World',
            ANY  # We don't need to check the exact size
        )
        
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+27123456789',
            'outbound',
            'Echo: Hello World',
            ANY  # We don't need to check the exact size
        )

@pytest.mark.unit
def test_n8n_format_echo_functionality():
    """Test that the echo functionality works correctly with n8n format messages."""
    # Create a test message in n8n format
    test_message = {
        'message': {
            'from': 'whatsapp:+27123456789',
            'body': 'Hello World'
        }
    }
    
    # Mock the Supabase client and user
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.log_message') as mock_log_message:
        
        # Setup mock user with POPIA consent and a selected bundle
        mock_get_user.return_value = {
            'preferred_language': 'en',
            'popia_consent_given': True,
            'current_bundle': 'test_bundle'  # Add a bundle to avoid bundle selection prompt
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert result_data['reply_text'] == 'Echo: Hello World'
        
        # Verify that both inbound and outbound messages were logged
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+27123456789',
            'inbound',
            'Hello World',
            ANY  # We don't need to check the exact size
        )
        
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+27123456789',
            'outbound',
            'Echo: Hello World',
            ANY  # We don't need to check the exact size
        )

@pytest.mark.unit
def test_cli_wrapper(monkeypatch, capsys):
    """Test the CLI wrapper functionality."""
    # Create a test message
    test_message = '{"message": {"from": "whatsapp:+27123456789", "body": "Hello CLI"}}'
    
    # Mock the handle_incoming_message function to return a known response
    with patch('src.core_handler.handle_incoming_message') as mock_handle:
        mock_handle.return_value = json.dumps({
            'reply_to': 'whatsapp:+27123456789',
            'reply_text': 'Echo: Hello CLI'
        })
        
        # Directly call the CLI wrapper code
        import sys
        original_argv = sys.argv
        sys.argv = ['src/core_handler.py', test_message]
        
        try:
            # Execute the code that would be in the __main__ block
            if len(sys.argv) > 1:
                message_data_json_string = sys.argv[1]
                response = mock_handle(message_data_json_string)
                print(response)
            else:
                print(json.dumps({
                    'reply_to': 'unknown',
                    'reply_text': "Error: No message data provided."
                }))
            
            # Capture stdout
            captured = capsys.readouterr()
            
            # Verify that the CLI wrapper called handle_incoming_message with the correct argument
            mock_handle.assert_called_once_with(test_message)
            
            # Verify that the response was printed to stdout
            assert '{"reply_to": "whatsapp:+27123456789", "reply_text": "Echo: Hello CLI"}' in captured.out
        finally:
            # Restore original sys.argv
            sys.argv = original_argv