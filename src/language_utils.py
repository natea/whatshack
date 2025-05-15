"""
Language Utilities Module for Township Connect WhatsApp Assistant.

This module provides functions for language detection and management,
including detecting the language from user messages and storing user language preferences.
"""

import logging
import re
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Define language detection patterns
LANGUAGE_PATTERNS = {
    'en': [
        r'\b(?:hello|hi|hey|good morning|good day|good evening)\b',
    ],
    'xh': [
        r'\b(?:molo|molweni|mholweni)\b',
    ],
    'af': [
        r'\b(?:hallo|goeie dag|goeie môre|goeie more)\b',
    ]
}

# Compile the patterns for efficiency
COMPILED_PATTERNS = {
    lang: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for lang, patterns in LANGUAGE_PATTERNS.items()
}
def detect_initial_language(message_text: str, default_language: str = 'en') -> str:
    """
    Detect the initial language from a user's first message, focusing on common greetings.
    
    This function is specifically designed for detecting language from initial greetings
    when a user first interacts with the system.
    
    Args:
        message_text: The text message to analyze
        default_language: The default language to return if no match is found
    
    Returns:
        The detected language code ('en', 'xh', or 'af')
    """
    logger.info(f"Detecting initial language from greeting: {message_text}")
    
    # Use the existing language detection logic
    return detect_language(message_text, default_language)

def detect_language(text: str, default_language: str = 'en') -> str:
    """
    Detect the language of a text message.
    
    Args:
        text: The text message to analyze
        default_language: The default language to return if no match is found
    
    Returns:
        The detected language code ('en', 'xh', or 'af')
    """
    logger.info(f"Detecting language for: {text}")
    
    if not text:
        return default_language
    
    # Convert to string in case None is passed
    if text is None:
        return default_language
        
    text = str(text).lower()
    
    # Check each language's patterns
    for lang, patterns in COMPILED_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                return lang
    
    # If no match is found, return the default language
    return default_language
    return default_language

def get_user_language(user_id: str, default_language: str = 'en') -> str:
    """
    Get a user's preferred language from the database.
    
    Args:
        user_id: The ID of the user
        default_language: The default language to return if no preference is found
    
    Returns:
        The user's preferred language code ('en', 'xh', or 'af')
    """
    # TODO: Implement user language retrieval
    logger.info(f"Getting language preference for user: {user_id}")
    
    # When implemented, this should work:
    # from src.db.supabase_client import get_client, get_user
    # 
    # client = get_client()
    # user = get_user(client, user_id)
    # 
    # if user and 'preferred_language' in user:
    #     return user['preferred_language']
    # 
    # return default_language
    
    # For now, return English as a placeholder
    return default_language

def set_user_language(user_id: str, language: str) -> bool:
    """
    Set a user's preferred language in the database.
    
    Args:
        user_id: The ID of the user
        language: The language code to set ('en', 'xh', or 'af')
    
    Returns:
        True if successful, False otherwise
    """
    # TODO: Implement user language setting
    logger.info(f"Setting language preference for user {user_id} to {language}")
    
    # Validate the language code
    if language not in ['en', 'xh', 'af']:
        logger.error(f"Invalid language code: {language}")
        return False
    
    # When implemented, this should work:
    # from src.db.supabase_client import get_client, get_user, create_user, update_user_language
    # 
    # client = get_client()
    # user = get_user(client, user_id)
    # 
    # if user:
    #     # Update existing user
    #     result = update_user_language(client, user_id, language)
    # else:
    #     # Create new user with language preference
    #     from datetime import datetime
    #     user_data = {
    #         'user_id': user_id,
    #         'preferred_language': language,
    #         'created_at': datetime.now().isoformat()
    #     }
    #     result = create_user(client, user_data)
    # 
    # return result["error"] is None
    
    # For now, return True as a placeholder
    return True

def get_language_name(language_code: str) -> str:
    """
    Get the full name of a language from its code.
    
    Args:
        language_code: The language code ('en', 'xh', or 'af')
    
    Returns:
        The full name of the language
    """
    language_names = {
        'en': 'English',
        'xh': 'isiXhosa',
        'af': 'Afrikaans'
    }
    
    return language_names.get(language_code, 'Unknown')