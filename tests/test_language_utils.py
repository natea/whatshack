"""
Tests for language utilities in Township Connect.

These tests verify that the language utility functions work correctly,
including detecting languages from initial greetings and storing user preferences.
"""

import pytest
import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.language_utils import detect_initial_language

@pytest.mark.parametrize("text,expected_language", [
    ("Hi", "en"),
    ("Hello", "en"),
    ("Good morning", "en"),
    ("Molo", "xh"),
    ("Molweni", "xh"),
    ("Hallo", "af"),
    ("Goeie dag", "af"),
    ("Test", "en"),  # Default to English for non-greeting text
    ("", "en"),      # Empty text should default to English
    (None, "en"),    # None should default to English
])
@pytest.mark.unit
def test_detect_initial_language(text, expected_language):
    """Test that the detect_initial_language function correctly detects languages from greetings."""
    detected = detect_initial_language(text)
    assert detected == expected_language, f"Expected '{expected_language}' for '{text}', got '{detected}'"

@pytest.mark.unit
def test_detect_initial_language_case_insensitive():
    """Test that initial language detection is case-insensitive."""
    assert detect_initial_language("HI") == "en"
    assert detect_initial_language("mOlO") == "xh"
    assert detect_initial_language("HALLO") == "af"

@pytest.mark.integration
def test_user_language_storage_integration(mocker):
    """
    Test that when a new user sends their first message, their language preference is stored.
    
    This test mocks the Supabase client to verify the integration between language detection
    and user preference storage.
    """
    # Import here to avoid circular imports
    from src.core_handler import handle_incoming_message
    
    # Mock the Supabase client and functions
    mock_supabase = mocker.patch('src.core_handler.supabase_client')
    mock_get_user = mocker.patch('src.core_handler.get_user')
    mock_create_user = mocker.patch('src.core_handler.create_user')
    mock_log_message = mocker.patch('src.core_handler.log_message')
    mock_get_template = mocker.patch('src.core_handler.get_message_template')
    mock_publish = mocker.patch('src.core_handler.publish_to_redis_stream')
    
    # Setup for a new Xhosa-speaking user
    mock_get_user.return_value = None  # User doesn't exist yet
    mock_get_template.return_value = "POPIA Notice"
    
    # Create test message for a new user saying "Molo" (Xhosa greeting)
    test_message = {
        'sender_id': 'whatsapp:+27123456789',
        'text': 'Molo'
    }
    
    # Process the message
    handle_incoming_message(json.dumps(test_message))
    
    # Verify that create_user was called with the correct language
    mock_create_user.assert_called_once_with(
        mock_supabase, 'whatsapp:+27123456789', 'xh', popia_consent=False
    )

# Add specific test for the Supabase integration requirement
@pytest.mark.integration
def test_xhosa_user_language_storage(mocker):
    """
    Test that when a new user sends 'Molo' as their first message,
    their preferred_language is set to 'xh' in the Supabase users table.
    
    This test mocks the Supabase client to verify the integration.
    """
    import json
    
    # Mock the Supabase client and functions
    mock_supabase = mocker.patch('src.core_handler.supabase_client')
    mock_get_user = mocker.patch('src.core_handler.get_user')
    mock_create_user = mocker.patch('src.core_handler.create_user')
    mock_log_message = mocker.patch('src.core_handler.log_message')
    mock_get_template = mocker.patch('src.core_handler.get_message_template')
    mock_publish = mocker.patch('src.core_handler.publish_to_redis_stream')
    
    # Setup for a new Xhosa-speaking user
    mock_get_user.return_value = None  # User doesn't exist yet
    mock_get_template.return_value = "POPIA Notice"
    
    # Test user ID
    test_user_id = 'xhosa_test_user'
    
    # Import here to avoid circular imports
    from src.core_handler import handle_incoming_message
    
    # Create test message for a new user saying "Molo" (Xhosa greeting)
    test_message = {
        'sender_id': test_user_id,
        'text': 'Molo'
    }
    
    # Process the message
    handle_incoming_message(json.dumps(test_message))
    
    # Verify that create_user was called with the correct language
    mock_create_user.assert_called_once_with(
        mock_supabase, test_user_id, 'xh', popia_consent=False
    )