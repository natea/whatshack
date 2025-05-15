"""
Supabase Client Module for Township Connect WhatsApp Assistant.

This module provides functions for interacting with the Supabase database,
including storing and retrieving user data, messages, and other information.
"""

import os
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from supabase import create_client, Client
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

def get_client():
    """
    Get a Supabase client instance.
    
    Returns:
        A Supabase client instance
    
    Raises:
        ValueError: If the required environment variables are not set
    """
    # Check for required environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        logger.warning("SUPABASE_URL and/or SUPABASE_ANON_KEY environment variables not set. Using mock client.")
        return MockSupabaseClient()
    
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        logger.error(f"Error creating Supabase client: {str(e)}")
        return MockSupabaseClient()

def execute_sql(sql, params=None) -> Tuple[bool, Any]:
    """
    Execute SQL using the Supabase REST API.
    
    Args:
        sql: The SQL to execute
        params: Optional parameters for the SQL query
        
    Returns:
        A tuple of (success, result) where success is a boolean and result is the query result or error message
    """
    try:
        # Get Supabase client
        client = get_client()
        if hasattr(client, '__class__') and client.__class__.__name__ == 'MockSupabaseClient':
            logger.warning("Using mock Supabase client. SQL execution will be simulated.")
            return True, []
        
        # Execute the SQL query
        result = client.from_('_').select('*').execute(
            count='exact',
            head=False,
            options={
                'method': 'POST',
                'url': f"{os.getenv('SUPABASE_URL')}/rest/v1/",
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': f"Bearer {os.getenv('SUPABASE_SERVICE_KEY')}",
                    'Prefer': 'return=representation'
                },
                'body': {
                    'query': sql,
                    'params': params or {}
                }
            }
        )
        
        if result.get('error'):
            logger.error(f"Error executing SQL: {result['error']}")
            return False, result['error']
        
        return True, result.get('data', [])
    except Exception as e:
        logger.error(f"Error executing SQL: {str(e)}")
        return False, str(e)
        return False, str(e)

class MockSupabaseClient:
    """
    A mock Supabase client for testing and development.
    """
    def __init__(self):
        self.users = {}
        self.messages = []
        self.current_table = None
        self.current_query = {}
        
    def table(self, table_name):
        self.current_table = table_name
        self.current_query = {}
        return self
        
    def select(self, columns="*"):
        self.current_query["select"] = columns
        return self
        
    def insert(self, data, returning="representation"):
        if self.current_table == "users":
            user_id = data.get("whatsapp_id")
            if user_id:
                self.users[user_id] = data
        elif self.current_table == "message_logs":
            self.messages.append(data)
        return self
        
    def update(self, data):
        self.current_query["update"] = data
        return self
        
    def eq(self, column, value):
        self.current_query["eq"] = (column, value)
        return self
        
    def execute(self):
        if self.current_table == "users":
            if "eq" in self.current_query:
                column, value = self.current_query["eq"]
                if column == "whatsapp_id":
                    if value in self.users:
                        return {"data": [self.users[value]], "error": None}
                    else:
                        return {"data": [], "error": None}
            elif "update" in self.current_query and "eq" in self.current_query:
                column, value = self.current_query["eq"]
                if column == "whatsapp_id" and value in self.users:
                    self.users[value].update(self.current_query["update"])
                    return {"data": [self.users[value]], "error": None}
            elif "insert" in self.current_query:
                return {"data": [self.current_query["insert"]], "error": None}
        elif self.current_table == "message_logs":
            return {"data": self.messages[-1:] if self.messages else [], "error": None}
        
        return {"data": [], "error": None}

def log_message(client, user_whatsapp_id: str, direction: str, message_content: str, data_size_kb: float = 0.1) -> Dict[str, Any]:
    """
    Log a message in the database.
    
    Args:
        client: A Supabase client instance
        user_whatsapp_id: The WhatsApp ID of the user
        direction: The direction of the message ('inbound' or 'outbound')
        message_content: The content of the message
        data_size_kb: The size of the message in KB (default: 0.1)
    
    Returns:
        The result of the database operation
    """
    logger.info(f"Logging {direction} message for user {user_whatsapp_id}")
    
    # Prepare message data
    from datetime import datetime
    message_data = {
        "user_whatsapp_id": user_whatsapp_id,
        "direction": direction,
        "message_content": message_content,
        "timestamp": datetime.now().isoformat(),
        "data_size_kb": data_size_kb
    }
    
    try:
        return client.table("message_logs").insert(message_data).execute()
    except Exception as e:
        logger.error(f"Error logging message: {str(e)}")
        return {"data": [message_data], "error": str(e)}

def get_user(client, whatsapp_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a user from the database.
    
    Args:
        client: A Supabase client instance
        whatsapp_id: The WhatsApp ID of the user to get
    
    Returns:
        The user data, or None if the user doesn't exist
    """
    logger.info(f"Getting user: {whatsapp_id}")
    
    try:
        result = client.table("users").select("*").eq("whatsapp_id", whatsapp_id).execute()
        if result["data"] and len(result["data"]) > 0:
            return result["data"][0]
        return None
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return None

def create_user(client, whatsapp_id: str, preferred_language: str = 'en', popia_consent: bool = False) -> Dict[str, Any]:
    """
    Create a new user in the database.
    
    Args:
        client: A Supabase client instance
        whatsapp_id: The WhatsApp ID of the user
        preferred_language: The user's preferred language (default: 'en')
        popia_consent: Whether the user has given POPIA consent (default: False)
    
    Returns:
        The result of the database operation
    """
    logger.info(f"Creating user: {whatsapp_id} with language {preferred_language}")
    
    # Prepare user data
    from datetime import datetime
    user_data = {
        "whatsapp_id": whatsapp_id,
        "preferred_language": preferred_language,
        "popia_consent_given": popia_consent,
        "created_at": datetime.now().isoformat(),
        "last_active_at": datetime.now().isoformat()
    }
    
    try:
        return client.table("users").insert(user_data).execute()
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return {"data": [user_data], "error": str(e)}

def update_user_language(client, whatsapp_id: str, language: str) -> Dict[str, Any]:
    """
    Update a user's preferred language.
    
    Args:
        client: A Supabase client instance
        whatsapp_id: The WhatsApp ID of the user to update
        language: The new preferred language
    
    Returns:
        The result of the database operation
    """
    logger.info(f"Updating user language: {whatsapp_id} -> {language}")
    
    # Validate the language code
    if language not in ['en', 'xh', 'af']:
        logger.error(f"Invalid language code: {language}")
        return {"data": [], "error": f"Invalid language code: {language}"}
    
    try:
        # Update the user's last active timestamp as well
        from datetime import datetime
        return client.table("users").update({
            "preferred_language": language,
            "last_active_at": datetime.now().isoformat()
        }).eq("whatsapp_id", whatsapp_id).execute()
    except Exception as e:
        logger.error(f"Error updating user language: {str(e)}")
        return {"data": [], "error": str(e)}

def delete_user_data(client, whatsapp_id: str) -> Dict[str, Any]:
    """
    Delete all data for a user (POPIA compliance).
    
    Args:
        client: A Supabase client instance
        whatsapp_id: The WhatsApp ID of the user whose data should be deleted
    
    Returns:
        The result of the database operation
    """
    logger.info(f"Deleting user data: {whatsapp_id}")
    
    try:
        # Log the deletion for security audit
        from datetime import datetime
        security_log = {
            "user_whatsapp_id": whatsapp_id,
            "event_type": "DATA_DELETE_CONFIRMED",
            "details": {"timestamp": datetime.now().isoformat()},
            "timestamp": datetime.now().isoformat()
        }
        client.table("security_logs").insert(security_log).execute()
        
        # Delete messages
        client.table("message_logs").delete().eq("user_whatsapp_id", whatsapp_id).execute()
        
        # Delete user
        result = client.table("users").delete().eq("whatsapp_id", whatsapp_id).execute()
        return result
    except Exception as e:
        logger.error(f"Error deleting user data: {str(e)}")
        return {"data": [], "error": str(e)}

def get_service_bundles(client) -> List[Dict[str, Any]]:
    """
    Get all available service bundles from the database.
    
    Args:
        client: A Supabase client instance
    
    Returns:
        A list of service bundle data
    """
    logger.info("Getting service bundles")
    
    try:
        result = client.table("service_bundles").select("*").execute()
        return result["data"] if result["data"] else []
    except Exception as e:
        logger.error(f"Error getting service bundles: {str(e)}")
        return []

def update_user_bundle(client, whatsapp_id: str, bundle_id: str) -> Dict[str, Any]:
    """
    Update a user's selected service bundle.
    
    Args:
        client: A Supabase client instance
        whatsapp_id: The WhatsApp ID of the user to update
        bundle_id: The ID of the selected bundle
    
    Returns:
        The result of the database operation
    """
    logger.info(f"Updating user bundle: {whatsapp_id} -> {bundle_id}")
    
    try:
        # Update the user's bundle and last active timestamp
        from datetime import datetime
        return client.table("users").update({
            "current_bundle": bundle_id,
            "last_active_at": datetime.now().isoformat()
        }).eq("whatsapp_id", whatsapp_id).execute()
    except Exception as e:
        logger.error(f"Error updating user bundle: {str(e)}")
        return {"data": [], "error": str(e)}

def update_user_popia_consent(client, whatsapp_id: str, consent_given: bool) -> Dict[str, Any]:
    """
    Update a user's POPIA consent status.
    
    Args:
        client: A Supabase client instance
        whatsapp_id: The WhatsApp ID of the user to update
        consent_given: Whether the user has given POPIA consent
    
    Returns:
        The result of the database operation
    """
    logger.info(f"Updating POPIA consent for user {whatsapp_id} to {consent_given}")
    
    try:
        # Update the user's POPIA consent and last active timestamp
        from datetime import datetime
        return client.table("users").update({
            "popia_consent_given": consent_given,
            "last_active_at": datetime.now().isoformat()
        }).eq("whatsapp_id", whatsapp_id).execute()
    except Exception as e:
        logger.error(f"Error updating user POPIA consent: {str(e)}")
        return {"data": [], "error": str(e)}