"""
Tests for POPIA consent functionality in Township Connect.

These tests verify that the POPIA consent functionality works correctly,
including POPIA notice presentation and updating user consent status in the database.
This follows the London School of TDD approach, focusing on mocking collaborators
and verifying interactions and observable outcomes.
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_handler import handle_incoming_message, get_message_template
from src.core_handler import TEMPLATE_DIR

# Test Case IDs from Test Plan
# TC_POP_001: Verify popia_notice_en.txt exists and is not empty
# TC_POP_002: Verify popia_notice_xh.txt exists
# TC_POP_003: Verify popia_notice_af.txt exists

@pytest.mark.unit
def test_popia_notice_files_exist():
    """
    Test that POPIA notice files exist in the correct directory.
    
    This test verifies AI-Verifiable End Result #1:
    A plain text file popia_notice_en.txt (and placeholders popia_notice_xh.txt,
    popia_notice_af.txt) exists in the data/message_templates directory,
    containing the POPIA notice.
    """
    # Check that the English POPIA notice exists and is not empty
    en_notice_path = TEMPLATE_DIR / "popia_notice_en.txt"
    assert en_notice_path.exists(), "English POPIA notice file does not exist"
    
    with open(en_notice_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert content.strip(), "English POPIA notice file is empty"
    
    # Check that the Xhosa POPIA notice exists
    xh_notice_path = TEMPLATE_DIR / "popia_notice_xh.txt"
    assert xh_notice_path.exists(), "Xhosa POPIA notice file does not exist"
    
    # Check that the Afrikaans POPIA notice exists
    af_notice_path = TEMPLATE_DIR / "popia_notice_af.txt"
    assert af_notice_path.exists(), "Afrikaans POPIA notice file does not exist"

@pytest.mark.unit
def test_popia_notice_presentation_new_user():
    """
    Test that POPIA notice is sent to new users before any other reply.
    
    This test verifies AI-Verifiable End Result #2:
    If a user is newly created (or popia_consent_given is FALSE), the system
    prepares to send the content of popia_notice_en.txt as a WhatsApp reply
    before any other functional reply.
    """
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.create_user') as mock_create_user, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.detect_language') as mock_detect_language, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist yet
        mock_detect_language.return_value = 'en'
        mock_popia_notice = "*POPIA NOTICE*\n\nTownship Connect collects and processes your data..."
        mock_get_template.return_value = mock_popia_notice
        
        # Create a test message from a new user
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result contains the POPIA notice
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert result_data['reply_text'] == mock_popia_notice
        
        # Verify the user was created with popia_consent=False
        mock_create_user.assert_called_once()
        mock_create_user.assert_called_with(mock_client, 'whatsapp:+27123456789', 'en', popia_consent=False)
        
        # Verify the POPIA notice was logged
        mock_log_message.assert_called_with(mock_client, 'whatsapp:+27123456789', 'outbound', mock_popia_notice, mock_log_message.call_args[0][4])

@pytest.mark.unit
def test_popia_notice_presentation_existing_user_no_consent():
    """
    Test that POPIA notice is sent to existing users who haven't given consent.
    
    This test verifies AI-Verifiable End Result #2:
    If popia_consent_given is FALSE for an existing user, the system prepares to send
    the content of popia_notice_en.txt as a WhatsApp reply before any other functional reply.
    """
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mocks - User exists but hasn't given POPIA consent
        mock_user = {
            'preferred_language': 'en',
            'popia_consent_given': False,
            'current_bundle': None
        }
        mock_get_user.return_value = mock_user
        
        # Mock the POPIA notice template
        mock_popia_notice = "*POPIA NOTICE*\n\nTownship Connect collects and processes your data..."
        mock_get_template.return_value = mock_popia_notice
        
        # Create a test message
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result contains the POPIA notice
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert result_data['reply_text'] == mock_popia_notice
        
        # Verify the POPIA notice was logged
        mock_log_message.assert_called_with(mock_client, 'whatsapp:+27123456789', 'outbound', mock_popia_notice, mock_log_message.call_args[0][4])

@pytest.mark.unit
def test_popia_notice_not_sent_to_consenting_user():
    """
    Test that POPIA notice is not sent to users who have already given consent.
    
    This test verifies that users who have already given POPIA consent receive
    normal responses instead of the POPIA notice.
    """
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mocks - User exists and has given POPIA consent
        mock_user = {
            'preferred_language': 'en',
            'popia_consent_given': True,
            'current_bundle': 'test_bundle'
        }
        mock_get_user.return_value = mock_user
        
        # Mock the welcome template
        mock_welcome = "Welcome to Township Connect!"
        mock_get_template.return_value = mock_welcome
        
        # Create a test message
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result contains the welcome message, not the POPIA notice
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert result_data['reply_text'] == mock_welcome
        
        # Verify the welcome message was logged, not the POPIA notice
        mock_log_message.assert_called_with(mock_client, 'whatsapp:+27123456789', 'outbound', mock_welcome, mock_log_message.call_args[0][4])

@pytest.mark.unit
def test_popia_consent_update():
    """
    Test that POPIA consent is updated when a user agrees.
    
    This test verifies AI-Verifiable End Result #3:
    If the user's message is "AGREE POPIA", the popia_consent_given field
    for that user in Supabase is updated to TRUE.
    """
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.update_user_popia_consent') as mock_update_consent, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mocks
        mock_user = {'preferred_language': 'en', 'popia_consent_given': False}
        mock_get_user.return_value = mock_user
        mock_get_template.return_value = "Welcome to Township Connect!"
        
        # Create a test message for POPIA agreement
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
        
        # Verify the update_user_popia_consent function was called correctly
        mock_update_consent.assert_called_once()
        mock_update_consent.assert_called_with(mock_client, 'whatsapp:+27123456789', True)

@pytest.mark.unit
def test_popia_notice_logging():
    """
    Test that POPIA notice sending is logged in the message_logs table.
    
    This test verifies AI-Verifiable End Result #4:
    The fact that the POPIA notice was sent is logged in message_logs for the user.
    """
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.create_user') as mock_create_user, \
         patch('src.core_handler.log_message') as mock_log_message, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.detect_language') as mock_detect_language, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mocks
        mock_get_user.return_value = None  # User doesn't exist yet
        mock_detect_language.return_value = 'en'
        mock_popia_notice = "*POPIA NOTICE*\n\nTownship Connect collects and processes your data..."
        mock_get_template.return_value = mock_popia_notice
        
        # Create a test message from a new user
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'
        }
        
        # Call the function
        handle_incoming_message(json.dumps(test_message))
        
        # Verify the POPIA notice was logged with the correct parameters
        mock_log_message.assert_any_call(
            mock_client,
            'whatsapp:+27123456789',
            'outbound',
            mock_popia_notice,
            mock_log_message.call_args[0][4]  # Size in KB
        )

@pytest.mark.unit
def test_popia_consent_already_given():
    """
    Test that POPIA consent message is handled correctly when consent is already given.
    
    This test verifies that the system responds appropriately when a user who has
    already given consent sends "AGREE POPIA" again.
    """
    # Test the generate_response function directly for POPIA agreement
    from src.core_handler import generate_response
    
    # Call the function with popia_agree command type
    response = generate_response("popia_agree", {}, "whatsapp:+27123456789", "en")
    
    # Verify the response contains the consent acknowledgment
    assert "Thank you for your consent" in response