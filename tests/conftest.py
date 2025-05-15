"""
Pytest configuration and fixtures for Township Connect WhatsApp Assistant tests.
"""

import json
import os
import sys
import pytest
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_message() -> Dict[str, Any]:
    """
    Fixture that provides a sample WhatsApp message.
    
    Returns:
        A dictionary containing a sample message
    """
    return {
        'sender_id': 'whatsapp:+27123456789',
        'text': 'Hello',
        'timestamp': '2025-05-14T18:30:00Z',
        'message_id': 'wamid.abcd1234',
        'profile_name': 'Test User'
    }

@pytest.fixture
def sample_message_json(sample_message) -> str:
    """
    Fixture that provides a sample WhatsApp message as a JSON string.
    
    Returns:
        A JSON string containing a sample message
    """
    return json.dumps(sample_message)

@pytest.fixture
def sample_language_messages() -> Dict[str, str]:
    """
    Fixture that provides sample messages in different languages.
    
    Returns:
        A dictionary mapping language codes to sample messages
    """
    return {
        'en': 'Hello',
        'xh': 'Molo',
        'af': 'Hallo'
    }

@pytest.fixture
def mock_supabase_client(monkeypatch):
    """
    Fixture that provides a mock Supabase client for testing.
    
    This avoids making actual API calls during tests.
    """
    class MockSupabaseClient:
        def __init__(self):
            self.stored_data = []
            
        def table(self, table_name):
            self.current_table = table_name
            return self
            
        def insert(self, data):
            self.stored_data.append(data)
            return self
            
        def execute(self):
            return {"data": self.stored_data, "error": None}
    
    mock_client = MockSupabaseClient()
    
    # TODO: Update this when we have the actual Supabase client module
    # monkeypatch.setattr('src.db.supabase_client.get_client', lambda: mock_client)
    
    return mock_client