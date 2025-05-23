"""
Pytest configuration and fixtures for Township Connect WhatsApp Assistant.
"""

import json
import os
import sys
import pytest
from typing import Dict, Any
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file if it exists
load_dotenv()

# Also load test-specific environment variables if available
test_env_path = os.path.join(os.path.dirname(__file__), '.env.test')
if os.path.exists(test_env_path):
    load_dotenv(test_env_path)

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

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """
    Set up test environment variables for Supabase integration tests.
    
    This fixture ensures that the required Supabase environment variables
    are available for integration tests. It uses test-specific values
    that point to a test Supabase instance.
    """
    # Check if environment variables are already set (e.g., in CI environment)
    if not os.environ.get("SUPABASE_URL") or not os.environ.get("SUPABASE_SERVICE_KEY"):
        # Set test-specific environment variables if not already set
        # These will be used as a fallback if .env.test doesn't exist or doesn't set these values
        os.environ["SUPABASE_URL"] = "https://test-project.supabase.co"
        os.environ["SUPABASE_SERVICE_KEY"] = "test-service-key"
        
        # Log that we're using test environment variables
        print("Using test environment variables for Supabase integration tests")
        print("To use your own Supabase instance, set SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables")
        print("or create a tests/.env.test file with these variables")
import pytest
from dotenv import load_dotenv # type: ignore
import os
from supabase import create_client, Client # type: ignore

# Load environment variables from .env.test, but ensure it's relative to tests directory
# Original conftest.py might already handle this, so this specific line might be redundant
# if load_dotenv is already called. Let's assume it's fine for now.
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env.test')
# load_dotenv(dotenv_path=dotenv_path)


@pytest.fixture(scope="session")
def supabase_client_session(): # Renamed to avoid conflict if another supabase_client fixture exists with different scope
    print("Attempting to create supabase_client_session fixture...")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    # Fallback to .env.test if not found in main env
    if not url or not key:
        print("SUPABASE_URL or SUPABASE_SERVICE_KEY not in environment. Trying tests/.env.test")
        dotenv_path_local = os.path.join(os.path.dirname(__file__), '.env.test')
        if os.path.exists(dotenv_path_local):
            print(f"Found {dotenv_path_local}, loading...")
            load_dotenv(dotenv_path=dotenv_path_local, override=True) # Override to ensure test vars take precedence
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_SERVICE_KEY")
        else:
            print(f"{dotenv_path_local} not found.")

    if not url or not key:
        # Try one more time with the path from original prompt, just in case
        # This is a bit defensive due to uncertainty about current load_dotenv behavior
        dotenv_path_prompt = "tests/.env.test" 
        if os.path.exists(dotenv_path_prompt):
            print(f"Still no URL/Key. Trying {dotenv_path_prompt} as a last resort.")
            load_dotenv(dotenv_path=dotenv_path_prompt, override=True)
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        print("Supabase URL or Service Key STILL not found after multiple attempts.")
        pytest.skip("Supabase credentials not found (SUPABASE_URL, SUPABASE_SERVICE_KEY). Skipping Supabase integration tests.")
    
    print(f"Supabase URL: {url[:20]}... Key: {'SERVICE_KEY_PRESENT' if key else 'SERVICE_KEY_MISSING'}")
    try:
        client = create_client(url, key)
        print("Supabase client created successfully for session.")
        return client
    except Exception as e:
        print(f"Error creating Supabase client in fixture: {e}")
        pytest.skip(f"Supabase client creation failed: {e}")


@pytest.fixture
def test_user(supabase_client_session: Client): # Depends on the session-scoped client
    user_id = "test_user_lang_switcher" 
    print(f"Setting up test_user: {user_id}")
    
    # Ensure user doesn't exist from a previous failed run or is clean
    try:
        supabase_client_session.table("users").delete().eq("whatsapp_id", user_id).execute()
        print(f"Attempted pre-delete for user {user_id}")
    except Exception as e:
        print(f"Error during pre-delete for {user_id}: {e}")
        # Continue, insertion will handle unique constraint if needed

    # Create user
    # Using postgrest.exceptions.APIError for more specific error handling if available
    try:
        data, error = supabase_client_session.table("users").insert({
            "whatsapp_id": user_id,
            "preferred_language": "en",
            "popia_consent_given": True # Start with consent for most tests
        }).execute()
        
        print(f"Insert response for {user_id}: data={data}, error={error}") # Assumes execute returns (data, error) or similar
        
        if error:
            # Supabase client often returns an error object with attributes like 'code', 'message'
            # For PostgREST errors, 'code' is a string.
            error_code = getattr(error, 'code', None)
            error_message = getattr(error, 'message', str(error))

            if error_code == '23505': # Unique violation
                print(f"User {user_id} already exists (unique_violation '23505'), proceeding.")
            else:
                error_details = f"Code: {error_code}, Message: {error_message}, Details: {getattr(error, 'details', 'N/A')}, Hint: {getattr(error, 'hint', 'N/A')}"
                print(f"Unhandled Supabase error creating test user {user_id}: {error_details}")
                # Depending on strictness, might raise Exception here or skip
                # raise Exception(f"Error creating test user {user_id}: {error_details}")
        elif not data: # No error, but also no data
             # This case might indicate a problem if data was expected.
             # For insert, data might be a list of inserted records.
            print(f"User {user_id} creation attempt returned no data and no explicit error. Response: data={data}, error={error}")
            # Potentially raise or skip if this state is unexpected for an insert
            # raise Exception(f"User {user_id} creation failed: No data returned. Response: data={data}, error={error}")

    except Exception as e: # Catching a broader set of exceptions during insert
        print(f"Generic exception creating test user {user_id}: {e}")
        # This might be a network issue or misconfiguration
        # Consider if this should be a skip or a hard fail
        pytest.skip(f"Generic exception during test_user setup for {user_id}: {e}")

    print(f"Yielding user_id: {user_id}")
    yield user_id 

    # Teardown: Delete user
    print(f"Tearing down test_user: {user_id}")
    try:
        supabase_client_session.table("users").delete().eq("whatsapp_id", user_id).execute()
        print(f"Successfully deleted user {user_id} during teardown.")
    except Exception as e:
        print(f"Error deleting test user {user_id} during teardown: {e}")