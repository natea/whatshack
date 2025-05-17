"""
Tests for Redis integration in Township Connect.

These tests verify that the Redis integration works correctly,
including publishing messages to the Redis stream and reading them back.
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_handler import handle_incoming_message

@pytest.mark.unit
def test_handle_incoming_message_publishes_to_redis():
    """Test that handle_incoming_message publishes the raw message to Redis."""
    # Mock the Redis client and Supabase client
    with patch('src.core_handler.redis_client') as mock_redis, \
         patch('src.core_handler.supabase_client') as mock_supabase, \
         patch('src.core_handler.publish_to_redis_stream') as mock_publish:
        
        # Setup mocks
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = {'data': []}
        mock_publish.return_value = True
        
        # Create test message data
        message_data = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'
        }
        message_json = json.dumps(message_data)
        
        # Call the function
        handle_incoming_message(message_json)
        
        # Verify that publish_to_redis_stream was called with the raw message string
        mock_publish.assert_called_once_with(message_json)

@pytest.mark.integration
def test_redis_stream_end_to_end():
    """
    Test the end-to-end Redis stream functionality.
    
    This test requires a running Redis instance and will:
    1. Send a message through handle_incoming_message
    2. Verify it's published to the Redis stream
    3. Use check_redis_stream.py to read the message back
    4. Verify the content matches
    
    Note: This test is marked as integration and will be skipped unless
    explicitly run with pytest -m integration
    """
    import subprocess
    import tempfile
    import time
    import os
    from src.core_handler import redis_client
    
    # Skip if REDIS_URL is not set or Redis client is not initialized
    if not os.getenv("REDIS_URL"):
        pytest.skip("REDIS_URL environment variable not set")
    
    if not redis_client:
        pytest.skip("Redis client not initialized. Check REDIS_URL format and Redis server availability.")
    
    # Create a unique test message
    test_id = int(time.time())
    test_message = {
        'sender_id': f'test-{test_id}',
        'text': f'Integration test message {test_id}'
    }
    test_message_json = json.dumps(test_message)
    
    # Send the message through handle_incoming_message
    with patch('src.core_handler.supabase_client') as mock_supabase:
        # Setup mock
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = {'data': []}
        
        # Call the function
        handle_incoming_message(test_message_json)
    
    # Wait a moment for the message to be processed
    time.sleep(1)
    
    # Use check_redis_stream.py to read the message back
    with tempfile.NamedTemporaryFile(mode='w+') as temp_file:
        # Run the script and capture output
        result = subprocess.run(
            ['python', 'scripts/check_redis_stream.py', '--count', '50'],
            capture_output=True,
            text=True
        )
        
        # Check if the script ran successfully
        assert result.returncode == 0, f"check_redis_stream.py failed: {result.stderr}"
        
        # Check if our test message is in the output
        output = result.stdout
        assert f'test-{test_id}' in output, "Test message not found in Redis stream"
        assert f'Integration test message {test_id}' in output, "Test message content not found in Redis stream"