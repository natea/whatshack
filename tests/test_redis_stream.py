"""
Tests for Redis stream publishing functionality in Township Connect.

These tests verify that the Redis stream publishing functionality works correctly,
including publishing messages to the Redis stream.
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_handler import publish_to_redis_stream

@pytest.mark.unit
def test_publish_to_redis_stream():
    """Test that the publish_to_redis_stream function works correctly."""
    # Mock the Redis client
    with patch('src.core_handler.redis_client') as mock_redis:
        # Setup mock
        mock_redis.xadd.return_value = "1-0"
        
        # Create test message data as JSON string
        message_data = json.dumps({
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello',
            'timestamp': '2025-05-14T18:30:00Z'
        })
        
        # Call the function
        result = publish_to_redis_stream(message_data)
        
        # Verify the result
        assert result is True
        
        # Verify the Redis client was called correctly
        mock_redis.xadd.assert_called_once()
        args, kwargs = mock_redis.xadd.call_args
        assert args[0] == 'incoming_whatsapp_messages'  # Stream name
        assert isinstance(args[1], dict)  # Message data
        assert 'data' in args[1]  # Message data should be in 'data' field
        
        # Verify the message data was passed through correctly
        assert args[1]['data'] == message_data
        
        # Verify the message content
        message_content = json.loads(args[1]['data'])
        assert message_content['sender_id'] == 'whatsapp:+27123456789'
        assert message_content['text'] == 'Hello'

@pytest.mark.unit
def test_publish_to_redis_stream_error_handling():
    """Test that the publish_to_redis_stream function handles errors correctly."""
    # Mock the Redis client to raise an exception
    with patch('src.core_handler.redis_client') as mock_redis:
        # Setup mock to raise an exception
        mock_redis.xadd.side_effect = Exception("Redis connection error")
        
        # Create test message data as JSON string
        message_data = json.dumps({
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'
        })
        
        # Call the function
        result = publish_to_redis_stream(message_data)
        
        # Verify the result indicates failure
        assert result is False