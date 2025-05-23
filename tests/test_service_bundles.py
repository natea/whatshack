"""
Tests for service bundle functionality in Township Connect.

These tests verify that the service bundle selection functionality works correctly,
including retrieving bundles, updating user bundles, handling bundle selection commands,
and populating the service_bundles table from JSON files.
"""

import json
import pytest
import sys
import os
import glob
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.supabase_client import get_service_bundles, update_user_bundle
from src.core_handler import handle_incoming_message, parse_message, generate_response, generate_bundle_selection_prompt

@pytest.fixture
def sample_bundles():
    """Fixture that provides sample service bundles for testing."""
    return [
        {
            "bundle_id": "street_vendor_crm",
            "bundle_name_en": "Street-Vendor CRM",
            "bundle_name_xh": "Isixhobo soThengiso",
            "bundle_name_af": "Straatverkoper CRM",
            "description_en": "Tools for street vendors.",
            "description_xh": "Izixhobo zabathengisi basesitratweni.",
            "description_af": "Gereedskap vir straatverkopers."
        },
        {
            "bundle_id": "small_business",
            "bundle_name_en": "Small Business Suite",
            "bundle_name_xh": "Iseti yoShishino oluNcinci",
            "bundle_name_af": "Klein Besigheid Suite",
            "description_en": "Complete tools for small businesses.",
            "description_xh": "Izixhobo ezipheleleyo zamashishini amancinci.",
            "description_af": "Volledige gereedskap vir klein besighede."
        }
    ]

@pytest.mark.unit
def test_get_service_bundles():
    """Test that the get_service_bundles function retrieves bundles correctly."""
    # Mock the Supabase client
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.execute.return_value = {
        "data": [
            {
                "bundle_id": "street_vendor_crm",
                "bundle_name_en": "Street-Vendor CRM"
            }
        ],
        "error": None
    }
    
    # Call the function
    result = get_service_bundles(mock_client)
    
    # Verify the result
    assert len(result) == 1
    assert result[0]["bundle_id"] == "street_vendor_crm"
    assert result[0]["bundle_name_en"] == "Street-Vendor CRM"
    
    # Verify the mock was called correctly
    mock_client.table.assert_called_with("service_bundles")
    mock_client.table.return_value.select.assert_called_with("*")

@pytest.mark.unit
def test_update_user_bundle():
    """Test that the update_user_bundle function updates a user's bundle correctly."""
    # Mock the Supabase client
    mock_client = MagicMock()
    mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value = {
        "data": [
            {
                "whatsapp_id": "whatsapp:+27123456789",
                "current_bundle": "street_vendor_crm"
            }
        ],
        "error": None
    }
    
    # Call the function
    result = update_user_bundle(mock_client, "whatsapp:+27123456789", "street_vendor_crm")
    
    # Verify the result
    assert result["data"][0]["whatsapp_id"] == "whatsapp:+27123456789"
    assert result["data"][0]["current_bundle"] == "street_vendor_crm"
    
    # Verify the mock was called correctly
    mock_client.table.assert_called_with("users")
    mock_client.table.return_value.update.return_value.eq.assert_called_with("whatsapp_id", "whatsapp:+27123456789")

@pytest.mark.unit
def test_parse_message_bundle_select():
    """Test that the parse_message function correctly parses bundle selection messages."""
    # Test a bundle selection message (a number)
    command_type, params = parse_message("1")
    assert command_type == "bundle_select"
    assert params["bundle_number"] == 1
    
    # Test another bundle selection message
    command_type, params = parse_message("2")
    assert command_type == "bundle_select"
    assert params["bundle_number"] == 2
    
    # Test with whitespace
    command_type, params = parse_message("  3  ")
    assert command_type == "bundle_select"
    assert params["bundle_number"] == 3
    
    # Test the /bundle command
    command_type, params = parse_message("/bundle")
    assert command_type == "bundle_list"
    assert params == {}

@pytest.mark.unit
def test_generate_bundle_selection_prompt(sample_bundles):
    """Test that the generate_bundle_selection_prompt function generates the correct prompt."""
    # Test English prompt
    prompt_en = generate_bundle_selection_prompt(sample_bundles, "en")
    assert "Please choose a service bundle" in prompt_en
    assert "1. Street-Vendor CRM" in prompt_en
    assert "2. Small Business Suite" in prompt_en
    
    # Test Xhosa prompt
    prompt_xh = generate_bundle_selection_prompt(sample_bundles, "xh")
    assert "Nceda ukhethe iphakheji" in prompt_xh
    assert "1. Isixhobo soThengiso" in prompt_xh
    assert "2. Iseti yoShishino oluNcinci" in prompt_xh
    
    # Test Afrikaans prompt
    prompt_af = generate_bundle_selection_prompt(sample_bundles, "af")
    assert "Kies asseblief 'n diensbondel" in prompt_af
    assert "1. Straatverkoper CRM" in prompt_af
    assert "2. Klein Besigheid Suite" in prompt_af

@pytest.mark.unit
def test_handle_incoming_message_bundle_selection():
    """Test that the handle_incoming_message function handles bundle selection correctly."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles, \
         patch('src.core_handler.update_user_bundle') as mock_update_bundle:
        
        # Setup mocks
        mock_user = {'preferred_language': 'en', 'popia_consent_given': True}
        mock_get_user.return_value = mock_user
        
        mock_bundles = [
            {
                "bundle_id": "street_vendor_crm",
                "bundle_name_en": "Street-Vendor CRM"
            },
            {
                "bundle_id": "small_business",
                "bundle_name_en": "Small Business Suite"
            }
        ]
        mock_get_bundles.return_value = mock_bundles
        
        # Create a test message for bundle selection
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': '1'  # Select the first bundle
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert "Bundle 'Street-Vendor CRM' selected!" in result_data['reply_text']
        
        # Verify the update_user_bundle function was called correctly
        mock_update_bundle.assert_called_with(mock_client, 'whatsapp:+27123456789', 'street_vendor_crm')

@pytest.mark.unit
def test_handle_incoming_message_bundle_prompt():
    """Test that users without a bundle are prompted to select one."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks
        mock_user = {'preferred_language': 'en', 'popia_consent_given': True, 'current_bundle': None}
        mock_get_user.return_value = mock_user
        
        mock_bundles = [
            {
                "bundle_id": "street_vendor_crm",
                "bundle_name_en": "Street-Vendor CRM",
                "description_en": "Tools for street vendors."
            }
        ]
        mock_get_bundles.return_value = mock_bundles
        
        # Mock the template to include the actual bundle list
        mock_get_template.return_value = "Please choose a service bundle by replying with the number:\n\n{bundle_list}\n\nReply with the number of your choice."
        
        # Create a test message
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'  # Any message that's not a bundle selection
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        assert "Please choose a service bundle" in result_data['reply_text']
        
        # The test was failing because the template placeholder wasn't being replaced
        # We don't need to check for the exact bundle text, just that the response contains
        # the word "bundle" and doesn't still have the placeholder
        assert "{bundle_list}" not in result_data['reply_text']
        assert "Street-Vendor CRM" in result_data['reply_text']

@pytest.mark.unit
def test_load_service_bundles_from_json():
    """Test loading service bundles from JSON files."""
    # Create mock JSON files
    mock_json_data = [
        {
            "bundle_id": "street_vendor_crm",
            "bundle_name_en": "Street-Vendor CRM",
            "bundle_name_xh": "Isixhobo soThengiso",
            "bundle_name_af": "Straatverkoper CRM",
            "description_en": "Tools for street vendors.",
            "description_xh": "Izixhobo zabathengisi basesitratweni.",
            "description_af": "Gereedskap vir straatverkopers.",
            "features": [
                {
                    "feature_id": "customer_tracking",
                    "name_en": "Customer Tracking"
                }
            ],
            "price_tier": "free",
            "active": True
        }
    ]
    
    # Mock the glob function to return a list of mock file paths
    mock_file_paths = ['data/service_bundles/street_vendor_crm.json']
    
    # Mock the open function to return the mock JSON data
    with patch('glob.glob', return_value=mock_file_paths), \
         patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data[0]))), \
         patch('src.db.supabase_client.get_client') as mock_get_client:
        
        # Create a mock Supabase client
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Import the function to test
        from scripts.populate_service_bundles import load_service_bundles_from_json
        
        # Call the function
        bundles = load_service_bundles_from_json()
        
        # Verify the result
        assert len(bundles) == 1
        assert bundles[0]['bundle_id'] == 'street_vendor_crm'
        assert bundles[0]['bundle_name_en'] == 'Street-Vendor CRM'
        assert bundles[0]['bundle_name_xh'] == 'Isixhobo soThengiso'
        assert bundles[0]['bundle_name_af'] == 'Straatverkoper CRM'
        assert bundles[0]['description_en'] == 'Tools for street vendors.'
        assert bundles[0]['price_tier'] == 'free'
        assert bundles[0]['active'] is True

@pytest.mark.unit
def test_populate_service_bundles_table():
    """Test populating the service_bundles table from JSON files."""
    # Create mock bundles
    mock_bundles = [
        {
            "bundle_id": "street_vendor_crm",
            "bundle_name_en": "Street-Vendor CRM",
            "bundle_name_xh": "Isixhobo soThengiso",
            "bundle_name_af": "Straatverkoper CRM",
            "description_en": "Tools for street vendors.",
            "description_xh": "Izixhobo zabathengisi basesitratweni.",
            "description_af": "Gereedskap vir straatverkopers.",
            "price_tier": "free",
            "active": True
        }
    ]
    
    # Mock the Supabase client
    mock_client = MagicMock()
    mock_client.table.return_value.upsert.return_value.execute.return_value = {
        "data": mock_bundles,
        "error": None
    }
    
    # Import the function to test
    from scripts.populate_service_bundles import populate_service_bundles_table
    
    # Call the function
    result = populate_service_bundles_table(mock_client, mock_bundles)
    
    # Verify the result
    assert result["data"] == mock_bundles
    assert result["error"] is None
    
    # Verify the mock was called correctly
    mock_client.table.assert_called_with("service_bundles")
    mock_client.table.return_value.upsert.assert_called_once()

@pytest.mark.unit
def test_handle_incoming_message_new_user_with_popia_consent():
    """Test that a new user with POPIA consent is prompted to select a bundle."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles, \
         patch('src.core_handler.get_message_template') as mock_get_template, \
         patch('src.core_handler.update_user_popia_consent') as mock_update_popia:
        
        # Setup mocks for the first message (new user gets POPIA notice)
        mock_get_user.return_value = None  # User doesn't exist initially
        
        # Mock templates
        mock_get_template.side_effect = lambda template_name: {
            "popia_notice_en.txt": "POPIA NOTICE: This is a test notice.",
            "bundle_select_prompt_en.txt": "Please choose a service bundle:\n\n1. Street-Vendor CRM",
            "welcome_en.txt": "Welcome to Township Connect!"
        }.get(template_name, "")
        
        # Create a test message for the new user
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'Hello'  # New user's first message
        }
        
        # Call the function - first message from new user should get POPIA notice
        result = handle_incoming_message(json.dumps(test_message))
        result_data = json.loads(result)
        assert "Welcome to Township Connect!" in result_data['reply_text']
        assert "POPIA" in result_data['reply_text']
        
        # Now setup for the second message (user agrees to POPIA)
        # User now exists and has no bundle
        mock_get_user.return_value = {
            'preferred_language': 'en',
            'popia_consent_given': False,  # Will be updated when they agree
            'current_bundle': None
        }
        
        mock_bundles = [
            {
                "bundle_id": "street_vendor_crm",
                "bundle_name_en": "Street-Vendor CRM"
            }
        ]
        mock_get_bundles.return_value = mock_bundles
        
        # Create a test message for POPIA agreement
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'AGREE POPIA'  # User agrees to POPIA
        }
        
        # After POPIA agreement, user should get bundle selection prompt
        # We need to update the mock to reflect that POPIA consent has been given
        mock_get_user.return_value = {
            'preferred_language': 'en',
            'popia_consent_given': True,  # Now they have given consent
            'current_bundle': None
        }
        
        # Call the function again with POPIA agreement
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        
        # For an existing user with POPIA consent who just agreed to POPIA, they get a thank you message
        assert "Thank you for your consent" in result_data['reply_text']
        assert "Welcome to Township Connect" in result_data['reply_text']
        
        # Now test that the next message after POPIA consent will trigger bundle selection
        mock_get_user.return_value = {
            'preferred_language': 'en',
            'popia_consent_given': True,
            'current_bundle': None
        }
        
        # Create a test message after POPIA agreement
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': 'What can I do?'  # User's next message after POPIA agreement
        }
        
        # Call the function again
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Now they should get the bundle selection prompt
        assert "Please choose a service bundle" in result_data['reply_text']
        assert "1. Street-Vendor CRM" in result_data['reply_text']

@pytest.mark.unit
def test_dynamic_bundle_list_in_prompt():
    """Test that the bundle selection prompt includes a dynamic list of bundles."""
    # Mock the message template
    with patch('src.core_handler.get_message_template') as mock_get_template:
        # Include the bundle_list placeholder in the template
        mock_get_template.return_value = "Please choose a service bundle by replying with the number:\n\n{bundle_list}\n\nReply with the number of your choice."
        
        # Create mock bundles
        mock_bundles = [
            {
                "bundle_id": "street_vendor_crm",
                "bundle_name_en": "Street-Vendor CRM",
                "description_en": "Tools for street vendors."
            },
            {
                "bundle_id": "small_business",
                "bundle_name_en": "Small Business Suite",
                "description_en": "Complete tools for small businesses."
            },
            {
                "bundle_id": "delivery_runner",
                "bundle_name_en": "Delivery Runner",
                "description_en": "Tools for local delivery runners."
            }
        ]
        
        # Generate the prompt
        prompt = generate_bundle_selection_prompt(mock_bundles, "en")
        
        # Verify the prompt contains all bundles
        assert "Please choose a service bundle" in prompt
        assert "1. Street-Vendor CRM" in prompt
        assert "2. Small Business Suite" in prompt
        assert "3. Delivery Runner" in prompt
        assert "Tools for street vendors" in prompt
        assert "Complete tools for small businesses" in prompt
        assert "Tools for local delivery runners" in prompt

@pytest.mark.unit
def test_bundle_selection_confirmation_multilingual():
    """Test that bundle selection confirmation is sent in the user's language."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles, \
         patch('src.core_handler.update_user_bundle') as mock_update_bundle:
        
        # Test for each language
        for lang, expected_text in [
            ('en', "Bundle 'Street-Vendor CRM' selected!"),
            ('xh', "Iphakheji 'Isixhobo soThengiso' ikhethiwe!"),
            ('af', "Bondel 'Straatverkoper CRM' gekies!")
        ]:
            # Setup mocks
            mock_user = {'preferred_language': lang, 'popia_consent_given': True}
            mock_get_user.return_value = mock_user
            
            mock_bundles = [
                {
                    "bundle_id": "street_vendor_crm",
                    "bundle_name_en": "Street-Vendor CRM",
                    "bundle_name_xh": "Isixhobo soThengiso",
                    "bundle_name_af": "Straatverkoper CRM"
                }
            ]
            mock_get_bundles.return_value = mock_bundles
            
            # Create a test message for bundle selection
            test_message = {
                'sender_id': f'whatsapp:+27123456789_{lang}',  # Use different IDs for each test
                'text': '1'  # Select the first bundle
            }
            
            # Call the function
            result = handle_incoming_message(json.dumps(test_message))
            
            # Parse the result
            result_data = json.loads(result)
            
            # Verify the result
            assert 'reply_to' in result_data
            assert 'reply_text' in result_data
            assert result_data['reply_to'] == f'whatsapp:+27123456789_{lang}'
            assert expected_text in result_data['reply_text']
            
            # Verify the update_user_bundle function was called correctly
            mock_update_bundle.assert_called_with(mock_client, f'whatsapp:+27123456789_{lang}', 'street_vendor_crm')

@pytest.mark.unit
def test_handle_bundle_list_command():
    """Test that the /bundle command lists available bundles and shows current bundle."""
    # Mock the Supabase client and functions
    with patch('src.core_handler.supabase_client') as mock_client, \
         patch('src.core_handler.get_user') as mock_get_user, \
         patch('src.core_handler.get_service_bundles') as mock_get_bundles, \
         patch('src.core_handler.get_message_template') as mock_get_template:
        
        # Setup mocks for a user with an existing bundle
        mock_user = {
            'preferred_language': 'en',
            'popia_consent_given': True,
            'current_bundle': 'street_vendor_crm'
        }
        mock_get_user.return_value = mock_user
        
        mock_bundles = [
            {
                "bundle_id": "street_vendor_crm",
                "bundle_name_en": "Street-Vendor CRM",
                "description_en": "Tools for street vendors."
            },
            {
                "bundle_id": "small_business",
                "bundle_name_en": "Small Business Suite",
                "description_en": "Complete tools for small businesses."
            }
        ]
        mock_get_bundles.return_value = mock_bundles
        
        # Mock the template
        mock_get_template.return_value = "Please choose a service bundle by replying with the number:\n\n{bundle_list}\n\nReply with the number of your choice."
        
        # Create a test message for the /bundle command
        test_message = {
            'sender_id': 'whatsapp:+27123456789',
            'text': '/bundle'
        }
        
        # Call the function
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result
        assert 'reply_to' in result_data
        assert 'reply_text' in result_data
        assert result_data['reply_to'] == 'whatsapp:+27123456789'
        
        # Check that the response includes the current bundle
        assert "Your current bundle is: 'Street-Vendor CRM'" in result_data['reply_text']
        
        # Check that the response includes the available bundles - case insensitive
        assert "1. street-vendor crm" in result_data['reply_text'].lower()
        assert "2. small business suite" in result_data['reply_text'].lower()
        
        # Now test with a user who doesn't have a bundle yet
        mock_user = {
            'preferred_language': 'en',
            'popia_consent_given': True,
            'current_bundle': None
        }
        mock_get_user.return_value = mock_user
        
        # Call the function again
        result = handle_incoming_message(json.dumps(test_message))
        
        # Parse the result
        result_data = json.loads(result)
        
        # Verify the result doesn't mention current bundle
        assert "Your current bundle is" not in result_data['reply_text']
        
        # But still lists available bundles
        assert "1. Street-Vendor CRM" in result_data['reply_text']
        assert "2. Small Business Suite" in result_data['reply_text']