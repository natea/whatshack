#!/usr/bin/env python3
"""
Utility script to check Redis Stream for Township Connect.

This script connects to the Redis instance and reads messages from the
'incoming_whatsapp_messages' stream. It can be used to verify that messages
are being published to the stream correctly.

Usage:
    python check_redis_stream.py [--count N] [--block MS] [--clear]

Options:
    --count N    Number of messages to read (default: 10)
    --block MS   Block for MS milliseconds if no messages (default: 1000)
    --clear      Clear the stream after reading (default: False)
"""

import os
import sys
import json
import argparse
import redis
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

def setup_argparse() -> argparse.Namespace:
    """Set up command line argument parsing."""
    parser = argparse.ArgumentParser(description='Check Redis Stream for Township Connect')
    parser.add_argument('--count', type=int, default=10, help='Number of messages to read (default: 10)')
    parser.add_argument('--block', type=int, default=1000, help='Block for MS milliseconds if no messages (default: 1000)')
    parser.add_argument('--clear', action='store_true', help='Clear the stream after reading')
    return parser.parse_args()

def get_redis_client() -> Optional[redis.Redis]:
    """
    Get a Redis client using environment variables.
    
    Returns:
        A Redis client or None if connection fails
    """
    # Try to connect using Upstash Redis specific variables first
    redis_host = os.getenv("UPSTASH_REDIS_HOST")
    redis_port = os.getenv("UPSTASH_REDIS_PORT")
    redis_password = os.getenv("UPSTASH_REDIS_PASSWORD")
    
    if redis_host and redis_port and redis_password:
        try:
            # Construct Redis URL with TLS for Upstash
            redis_url = f"rediss://:{redis_password}@{redis_host}:{redis_port}"
            client = redis.from_url(redis_url)
            # Test connection
            client.ping()
            print(f"Connected to Upstash Redis at {redis_host}:{redis_port}")
            return client
        except Exception as e:
            print(f"Error connecting to Upstash Redis: {str(e)}")
            # Fall through to try legacy REDIS_URL
    
    # Fall back to legacy REDIS_URL if Upstash variables are not set or connection failed
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        print("Error: Neither Upstash Redis variables nor REDIS_URL environment variable are set.")
        print("Please set either:")
        print("1. UPSTASH_REDIS_HOST, UPSTASH_REDIS_PORT, and UPSTASH_REDIS_PASSWORD")
        print("   Example: export UPSTASH_REDIS_HOST=your-redis.upstash.io")
        print("            export UPSTASH_REDIS_PORT=12345")
        print("            export UPSTASH_REDIS_PASSWORD=your-password")
        print("OR")
        print("2. REDIS_URL to the Redis connection string")
        print("   Example: export REDIS_URL=redis://username:password@host:port")
        return None
    
    try:
        # Ensure TLS is used for Upstash Redis by converting redis:// to rediss://
        if redis_url.startswith("redis://") and "upstash.io" in redis_url:
            redis_url = redis_url.replace("redis://", "rediss://", 1)
            print("Converting Redis URL to use TLS (rediss://)")
        
        client = redis.from_url(redis_url)
        # Test connection
        client.ping()
        print(f"Connected to Redis at {redis_url.split('@')[-1]}")
        return client
    except Exception as e:
        print(f"Error connecting to Redis: {str(e)}")
        return None

def read_stream(client: redis.Redis, stream_name: str, count: int, block: int) -> List[Tuple[bytes, Dict[bytes, bytes]]]:
    """
    Read messages from a Redis stream.
    
    Args:
        client: Redis client
        stream_name: Name of the stream to read from
        count: Maximum number of messages to read
        block: Time to block in milliseconds if no messages
        
    Returns:
        List of (message_id, message_data) tuples
    """
    try:
        # Check if stream exists
        if not client.exists(stream_name):
            print(f"Stream '{stream_name}' does not exist.")
            return []
        
        # Get the stream length
        stream_length = client.xlen(stream_name)
        print(f"Stream '{stream_name}' has {stream_length} messages.")
        
        if stream_length == 0:
            print(f"Waiting for up to {block}ms for new messages...")
        
        # Read the most recent messages from the stream
        if stream_length > 0:
            # Use xrevrange to get the most recent messages
            messages = client.xrevrange(stream_name, '+', '-', count=count)
            if messages:
                print(f"Read {len(messages)} messages from the stream.")
                # Return in a format compatible with the rest of the code
                return messages
            else:
                print("No messages received.")
                return []
        else:
            # If stream is empty, try to wait for new messages
            if block > 0:
                print(f"Waiting for up to {block}ms for new messages...")
                messages = client.xread({stream_name: '$'}, count=count, block=block)
                if messages and len(messages) > 0:
                    stream_messages = messages[0][1]
                    print(f"Read {len(stream_messages)} messages from the stream.")
                    return stream_messages
            
            print("No messages found in stream.")
            return []
    except Exception as e:
        print(f"Error reading from stream: {str(e)}")
        return []

def clear_stream(client: redis.Redis, stream_name: str) -> bool:
    """
    Clear all messages from a Redis stream.
    
    Args:
        client: Redis client
        stream_name: Name of the stream to clear
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Delete the stream
        client.delete(stream_name)
        print(f"Stream '{stream_name}' cleared.")
        return True
    except Exception as e:
        print(f"Error clearing stream: {str(e)}")
        return False

def format_message(message_id: bytes, message_data: Dict[bytes, bytes]) -> str:
    """
    Format a message for display.
    
    Args:
        message_id: The message ID
        message_data: The message data
        
    Returns:
        A formatted string representation of the message
    """
    # Convert message ID to string
    id_str = message_id.decode('utf-8')
    
    # Extract timestamp from message ID
    timestamp_ms = int(id_str.split('-')[0])
    timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
    
    # Extract and parse the message data
    data = message_data.get(b'data', b'{}').decode('utf-8')
    try:
        parsed_data = json.loads(data)
        # Pretty-print the JSON data
        formatted_data = json.dumps(parsed_data, indent=2)
    except json.JSONDecodeError:
        formatted_data = data
    
    return f"Message ID: {id_str}\nTimestamp: {timestamp}\nData:\n{formatted_data}\n"

def main():
    """Main function."""
    args = setup_argparse()
    
    # Get Redis client
    client = get_redis_client()
    if not client:
        sys.exit(1)
    
    # Always use 'incoming_whatsapp_messages' as the stream name
    stream_name = 'incoming_whatsapp_messages'
    
    # Read from the stream
    messages = read_stream(client, stream_name, args.count, args.block)
    
    # Display the messages
    if messages:
        print("\n--- Messages ---")
        for i, (message_id, message_data) in enumerate(messages, 1):
            print(f"\n[{i}/{len(messages)}]")
            print(format_message(message_id, message_data))
    
    # Clear the stream if requested
    if args.clear and messages:
        clear_stream(client, stream_name)

if __name__ == "__main__":
    main()