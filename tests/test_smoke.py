"""
Smoke tests for Township Connect WhatsApp Assistant.

These tests verify that the basic functionality of the application is working.
"""

import json
import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.smoke
def test_import_main():
    """Test that the main module can be imported."""
    from src import main
    assert main is not None

@pytest.mark.smoke
def test_import_core_handler():
    """Test that the core_handler module can be imported."""
    from src.core_handler import handle_incoming_message
    assert handle_incoming_message is not None

@pytest.mark.smoke
def test_handle_incoming_message():
    """Test that the handle_incoming_message function works correctly."""
    from src.core_handler import handle_incoming_message
    
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
    assert 'Welcome to Township Connect' in result_data['reply_text']