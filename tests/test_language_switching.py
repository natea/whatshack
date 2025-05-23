import pytest
import json
from unittest.mock import patch, MagicMock

from supabase import Client # type: ignore

from src.core_handler import handle_incoming_message, supabase_client as core_supabase_client, CONTENT_DIR
from src.db.supabase_client import get_user, update_user_language

# Ensure conftest.py's supabase_client fixture is available
# and test_user fixture can be used.

# Content of confirmation files for verification
CONFIRMATION_EN = "Language set to English."
CONFIRMATION_XH = "Ulwimi lusetelwe kwiXhosa."
CONFIRMATION_AF = "Taal ingestel op Afrikaans."

@pytest.fixture(scope="module", autouse=True)
def setup_confirmation_files():
    """Ensure confirmation files exist for tests."""
    (CONTENT_DIR / "lang_confirmation_en.txt").write_text(CONFIRMATION_EN)
    (CONTENT_DIR / "lang_confirmation_xh.txt").write_text(CONFIRMATION_XH)
    (CONTENT_DIR / "lang_confirmation_af.txt").write_text(CONFIRMATION_AF)
    yield
    # No specific teardown needed for these files for now

@pytest.mark.parametrize("lang_code, expected_confirmation_content", [
    ("en", CONFIRMATION_EN),
    ("xh", CONFIRMATION_XH),
    ("af", CONFIRMATION_AF),
])
def test_language_switch_updates_db_and_returns_confirmation(
    supabase_client_session: Client,
    test_user: str, # whatsapp_id of the test user from conftest
    lang_code: str,
    expected_confirmation_content: str
):
    """
    Test that sending a /lang command updates the preferred_language in Supabase
    and returns the correct confirmation message.
    """
    sender_id = test_user

    # Ensure the core_handler uses the test Supabase client
    # This can be tricky if core_handler.supabase_client is initialized at module level.
    # For robust testing, dependency injection or a settable client in core_handler would be better.
    # For now, we assume conftest.py's setup correctly influences the client,
    # or we directly patch it if necessary.
    
    # Patch the global supabase_client in core_handler for this test
    with patch('src.core_handler.supabase_client', supabase_client_session):
        # Simulate incoming message for language change
        message_data = {
            "sender_id": sender_id,
            "text": f"/lang {lang_code}"
        }
        message_json = json.dumps(message_data)

        response_json = handle_incoming_message(message_json)
        response_data = json.loads(response_json)

        # 1. Verify response content
        assert response_data["reply_to"] == sender_id
        assert response_data["reply_text"] == expected_confirmation_content, \
            f"Expected confirmation '{expected_confirmation_content}', got '{response_data['reply_text']}'"

        # 2. Verify database update
        # Use the original supabase_client_session fixture for direct DB verification
        user_db_record = get_user(supabase_client_session, sender_id)
        assert user_db_record is not None, f"User {sender_id} not found after lang switch."
        assert user_db_record.get("preferred_language") == lang_code, \
            f"Expected language '{lang_code}', got '{user_db_record.get('preferred_language')}' in DB."

def test_language_switch_n8n_format(
    supabase_client_session: Client,
    test_user: str
):
    """Test language switching with n8n style message format."""
    sender_id = test_user
    lang_code = "xh"
    expected_confirmation_content = CONFIRMATION_XH

    with patch('src.core_handler.supabase_client', supabase_client_session):
        message_data_n8n = {
            "message": {
                "from": sender_id,
                "body": f"/lang {lang_code}"
            }
        }
        message_json = json.dumps(message_data_n8n)
        response_json = handle_incoming_message(message_json)
        response_data = json.loads(response_json)

        assert response_data["reply_to"] == sender_id
        assert response_data["reply_text"] == expected_confirmation_content

        user_db_record = get_user(supabase_client_session, sender_id)
        assert user_db_record is not None
        assert user_db_record.get("preferred_language") == lang_code

def test_unknown_lang_command_echoes(
    supabase_client_session: Client,
    test_user: str
):
    """Test that an invalid /lang command (e.g., /lang fr) is treated as an echo."""
    sender_id = test_user
    original_lang = "en" # Assuming user starts with 'en' or it's set by test_user fixture

    # Set initial language for the user
    update_user_language(supabase_client_session, sender_id, original_lang)

    invalid_command = "/lang fr"
    
    with patch('src.core_handler.supabase_client', supabase_client_session):
        message_data = {"sender_id": sender_id, "text": invalid_command}
        message_json = json.dumps(message_data)
        response_json = handle_incoming_message(message_json)
        response_data = json.loads(response_json)

        # Expecting echo behavior
        assert response_data["reply_text"] == f"Echo: {invalid_command}"

        # Verify language in DB has NOT changed
        user_db_record = get_user(supabase_client_session, sender_id)
        assert user_db_record is not None
        assert user_db_record.get("preferred_language") == original_lang

def test_message_after_lang_switch_uses_new_lang_for_popia(
    supabase_client_session: Client,
    test_user: str
):
    """
    Test that if a user switches language, and then sends another message
    triggering a POPIA notice (e.g., new user flow simulated by resetting consent),
    the notice is in the new language.
    This test assumes the test_user fixture creates a user who has already given POPIA consent.
    We will manually set popia_consent_given to False to trigger the notice.
    """
    sender_id = test_user
    new_lang_code = "af"

    with patch('src.core_handler.supabase_client', supabase_client_session):
        # 1. Switch language
        lang_switch_message = json.dumps({"sender_id": sender_id, "text": f"/lang {new_lang_code}"})
        handle_incoming_message(lang_switch_message) # Response ignored for this part

        # 2. Modify user to simulate needing POPIA notice again
        #    (e.g., by setting popia_consent_given to False)
        data, error = supabase_client_session.table("users").update({"popia_consent_given": False}).eq("whatsapp_id", sender_id).execute()
        
        if error:
            error_code = getattr(error, 'code', None)
            error_message = getattr(error, 'message', str(error))
            # Allow test to proceed if error is just that row doesn't exist (e.g. if test_user failed setup but skipped)
            # Or if it's a unique constraint violation (though less likely for an update)
            # For RLS issues, '42501' is common.
            if error_code not in [None, 'PGRST116']: # PGRST116: "Searched for range '(0,0)' but resource has 0 items." (row not found)
                 assert error_code is None, f"Failed to set popia_consent_given to False: Code: {error_code}, Msg: {error_message}"
            else:
                print(f"Warning/Info during popia_consent_given update: Code: {error_code}, Msg: {error_message}")

        # Fetch user to confirm POPIA status for debugging
        updated_user = get_user(supabase_client_session, sender_id)
        assert updated_user is not None and updated_user.get("popia_consent_given") is False, "POPIA consent not set to False"
        assert updated_user.get("preferred_language") == new_lang_code, "Language not updated correctly before POPIA check"


        # 3. Send a generic message that would normally trigger POPIA if not consented
        generic_message_text = "Hello again"
        generic_message = json.dumps({"sender_id": sender_id, "text": generic_message_text})
        
        # Ensure popia_notice_af.txt exists for this test
        popia_af_path = CONTENT_DIR / "popia_notice_af.txt"
        if not popia_af_path.exists():
             popia_af_path.write_text("Afrikaans POPIA Notice. Type AGREE POPIA to consent.")


        response_json = handle_incoming_message(generic_message)
        response_data = json.loads(response_json)

        # 4. Verify POPIA notice is in Afrikaans
        # This relies on having 'popia_notice_af.txt' in the content directory
        # and that generate_response correctly fetches it.
        expected_popia_af = (CONTENT_DIR / "popia_notice_af.txt").read_text()
        assert response_data["reply_text"] == expected_popia_af, \
             f"Expected Afrikaans POPIA notice, got: {response_data['reply_text']}"

    # Clean up: Set POPIA consent back to True for other tests if needed, or rely on test_user teardown.
    # These lines are now correctly indented to be outside the 'with' block.
    supabase_client_session.table("users").update({"popia_consent_given": True}).eq("whatsapp_id", sender_id).execute()
    if popia_af_path.exists() and popia_af_path.read_text() == "Afrikaans POPIA Notice. Type AGREE POPIA to consent.":
        popia_af_path.unlink() # Clean up temporary file

def test_lang_command_without_supabase(test_user: str):
    """Test that /lang command returns an error if Supabase is not available."""
    sender_id = test_user
    with patch('src.core_handler.supabase_client', None): # Simulate Supabase client being None
        message_data = {"sender_id": sender_id, "text": "/lang en"}
        message_json = json.dumps(message_data)
        response_json = handle_incoming_message(message_json)
        response_data = json.loads(response_json)

        assert "Sorry, I cannot change the language at the moment" in response_data["reply_text"]