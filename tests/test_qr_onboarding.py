import pytest
import re
import json
from src.core_handler import handle_incoming_message
from src.db.supabase_client import get_service_client, get_user as get_user_by_whatsapp_id_from_db # Renaming to avoid conflict
from supabase import Client as SupabaseClientTypeHint # For type hinting
from unittest.mock import MagicMock

# A unique phone number for testing to avoid conflicts
# Using a common test prefix like +000 followed by a unique sequence
TEST_PHONE_NUMBER_QR = "+000987654321"
TEST_PHONE_NUMBER_QR_CLEAN = "000987654321" # For DB checks if stored without '+'

@pytest.fixture(scope="module")
def supabase_client_qr() -> SupabaseClientTypeHint:
    """Provides a Supabase service client instance for QR onboarding tests."""
    # Use get_service_client for tests that need to manipulate data directly
    client = get_service_client()
    return client

def cleanup_test_user_qr(client: SupabaseClientTypeHint, phone_number: str):
    """Helper function to delete the test user after the test."""
    # Ensure the number is in the format used for deletion (e.g. with or without '+')
    # Assuming the hard_delete_user_data function expects the number as stored or can handle it.
    # Attempt to delete the user directly by whatsapp_id as RPC hard_delete_user_data seems problematic.
    try:
        user_to_delete = get_user_by_whatsapp_id_from_db(client, phone_number)
        if user_to_delete:
            print(f"User {phone_number} found, attempting direct delete from 'users' table.")
            client.table("users").delete().eq("whatsapp_id", phone_number).execute()
            
            # Optionally, also try to call the RPC function, but don't rely on it for primary cleanup verification here.
            try:
                print(f"Additionally calling RPC hard_delete_user_data for {phone_number}.")
                client.rpc("hard_delete_user_data", {"user_whatsapp_id": phone_number}).execute()
            except Exception as rpc_e:
                print(f"Ignoring error from secondary RPC call during cleanup: {rpc_e}")

            # Verify deletion
            user_after_delete = get_user_by_whatsapp_id_from_db(client, phone_number)
            if user_after_delete is None:
                print(f"Successfully cleaned up user {phone_number} by direct delete.")
            else:
                print(f"Failed to clean up user {phone_number} even after direct delete attempt.")
        else:
            print(f"User {phone_number} not found for cleanup. No action needed.")
            
    except Exception as e:
        print(f"Error during cleanup_test_user_qr for {phone_number}: {e}")


@pytest.mark.integration
def test_simulate_qr_user_command_creates_new_user(supabase_client_qr: SupabaseClientTypeHint):
    """
    Tests that the /simulate_qr_user command successfully creates a new user
    in the Supabase 'users' table.
    """
    # Ensure the user does not exist before the test
    cleanup_test_user_qr(supabase_client_qr, TEST_PHONE_NUMBER_QR)
    
    user_before = get_user_by_whatsapp_id_from_db(supabase_client_qr, TEST_PHONE_NUMBER_QR)
    assert user_before is None, f"User {TEST_PHONE_NUMBER_QR} already exists before test."

    # Mock the incoming message data structure that handle_message expects
    # This structure might need adjustment based on how Twilio/gateway formats it.
    # For a command, the crucial part is 'Body' and 'From'.
    # 'From' typically is 'whatsapp:+1234567890'
    # 'To' would be the service number.
    
    # The command "/simulate_qr_user [new_phone_number]" is sent by an *admin* or *test* number.
    # Let's assume an admin number sends this command.
    admin_sender_id = "whatsapp:+111000111" # An arbitrary admin/test number
    service_number = "whatsapp:+222000222"  # The service's number

    mock_incoming_message_data = {
        "From": admin_sender_id, # Command sender
        "To": service_number,     # Service number
        "Body": f"/simulate_qr_user {TEST_PHONE_NUMBER_QR}",
        "MessageSid": "SMqrtest123",
        "NumMedia": "0"
        # Add other fields if core_handler expects them
    }

    # We might need to mock external dependencies of handle_message if they are not relevant
    # to this specific user creation path (e.g., external API calls for language detection if QR bypasses it).
    # For now, assume handle_message can be called directly.

    # Call the handler
    # handle_message is synchronous based on current understanding
    response_message = handle_incoming_message(json.dumps(mock_incoming_message_data))

    # Verification: Check if the user was created
    user_after = get_user_by_whatsapp_id_from_db(supabase_client_qr, TEST_PHONE_NUMBER_QR)
    
    assert user_after is not None, f"User {TEST_PHONE_NUMBER_QR} was not created after /simulate_qr_user command."
    assert user_after.get('whatsapp_id') == TEST_PHONE_NUMBER_QR
    # Add more assertions if needed, e.g., default language, popia_consent_date is null initially etc.
    # Based on MT2.1, a new user flow involves language detection & POPIA.
    # The response_message should ideally be the start of that flow (e.g., language prompt).
    # For this test, the primary check is user creation.
    # The response_message from handle_message when processing /simulate_qr_user might be an ack message
    # to the admin, or it might be empty if it directly triggers a flow for the *new* user.
    # Let's assume it's an acknowledgement or a success message.
    assert "Simulated QR user onboarding for" in response_message or "User creation process initiated for" in response_message, \
           f"Unexpected response from /simulate_qr_user: {response_message}"


    # Cleanup: Delete the created user
    cleanup_test_user_qr(supabase_client_qr, TEST_PHONE_NUMBER_QR)
    user_after_cleanup = get_user_by_whatsapp_id_from_db(supabase_client_qr, TEST_PHONE_NUMBER_QR)
    assert user_after_cleanup is None, f"User {TEST_PHONE_NUMBER_QR} was not cleaned up after test."