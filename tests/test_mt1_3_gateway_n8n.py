import os
import re
import pytest
import json
import requests
from pathlib import Path

class TestWhatsAppGatewaySetup:
    """Tests for Micro-task 1.3: WhatsApp Gateway Selection, Setup & Initial n8n Configuration"""
    
    def test_gateway_selection_document_exists(self):
        """Test that the gateway selection rationale document exists"""
        doc_path = Path("docs/gateway_selection_rationale.md")
        assert doc_path.exists(), "Gateway selection rationale document does not exist"
        
        # Check content to ensure it's a proper document with a decision
        with open(doc_path, 'r') as f:
            content = f.read()
        
        assert "Decision:" in content, "Gateway selection document does not contain a decision"
        assert "WAHA" in content, "Gateway selection document does not mention WAHA"
        assert "Twilio" in content, "Gateway selection document does not mention Twilio"
    
    def test_n8n_setup_log_exists(self):
        """Test that the n8n setup log exists"""
        log_path = Path("logs/n8n_setup.log")
        assert log_path.exists(), "n8n setup log does not exist"
        
        # Check content to ensure it contains necessary sections
        with open(log_path, 'r') as f:
            content = f.read()
        
        assert "WhatsApp Gateway Selection" in content, "Setup log does not contain gateway selection section"
        assert "n8n Instance Setup" in content, "Setup log does not contain n8n instance setup section"
        assert "Twilio Account Setup" in content, "Setup log does not contain Twilio account setup section"
        assert "n8n-Twilio Integration" in content, "Setup log does not contain n8n-Twilio integration section"
    
    def test_gateway_selection_is_logged(self):
        """Test that the gateway selection is properly logged"""
        log_path = Path("logs/n8n_setup.log")
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Check if either WAHA or Twilio is selected
        gateway_selected = False
        if "Selected Gateway: WAHA" in content:
            gateway_selected = True
        elif "Selected Gateway: Twilio" in content:
            gateway_selected = True
        
        assert gateway_selected, "No WhatsApp gateway selection is logged"
    
    def test_n8n_instance_is_configured(self):
        """Test that an n8n instance is configured and logged"""
        log_path = Path("logs/n8n_setup.log")
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Check for n8n URL
        url_pattern = re.compile(r'URL: (https?://[^\s]+)')
        url_match = url_pattern.search(content)
        
        assert url_match, "n8n instance URL is not logged"
        
        # Check for API key placeholder or actual key
        api_key_pattern = re.compile(r'API Key: ([^\s]+)')
        api_key_match = api_key_pattern.search(content)
        
        assert api_key_match, "n8n API key is not logged"
    
    def test_twilio_or_waha_configuration(self):
        """Test that either Twilio or WAHA is configured based on selection"""
        log_path = Path("logs/n8n_setup.log")
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Determine which gateway was selected
        if "Selected Gateway: Twilio" in content:
            # Check for Twilio configuration
            assert "Account SID:" in content, "Twilio Account SID is not logged"
            assert "Auth Token:" in content, "Twilio Auth Token is not logged"
            assert "WhatsApp Sender Number:" in content, "Twilio WhatsApp Sender Number is not logged"
            
            # Check for Twilio workflow
            assert "Incoming_WhatsApp_Webhook_Twilio" in content, "Twilio webhook workflow is not mentioned"
        
        elif "Selected Gateway: WAHA" in content:
            # Check for WAHA configuration
            assert "WAHA instance" in content, "WAHA instance details are not logged"
            assert "WAHA session" in content, "WAHA session details are not logged"
            
            # Check for WAHA workflow
            assert "Incoming_WhatsApp_Webhook_WAHA" in content, "WAHA webhook workflow is not mentioned"
    
    def test_n8n_workflow_json_exists(self):
        """Test that the n8n workflow JSON file exists"""
        # Check which gateway was selected
        log_path = Path("logs/n8n_setup.log")
        with open(log_path, 'r') as f:
            content = f.read()
        
        if "Selected Gateway: Twilio" in content:
            workflow_path = Path("n8n_workflows/Incoming_WhatsApp_Webhook_Twilio.json")
        elif "Selected Gateway: WAHA" in content:
            workflow_path = Path("n8n_workflows/Incoming_WhatsApp_Webhook_WAHA.json")
        else:
            pytest.fail("No gateway selection found in log")
        
        # This test might be skipped if the workflow is only in n8n cloud and not exported
        if not workflow_path.exists():
            pytest.skip(f"Workflow JSON file {workflow_path} does not exist. This is acceptable if using n8n cloud without local export.")
        
        # If file exists, validate it's a proper JSON
        if workflow_path.exists():
            with open(workflow_path, 'r') as f:
                try:
                    workflow_json = json.load(f)
                    assert "nodes" in workflow_json, "Workflow JSON does not contain nodes"
                    assert "connections" in workflow_json, "Workflow JSON does not contain connections"
                except json.JSONDecodeError:
                    pytest.fail(f"Workflow file {workflow_path} is not valid JSON")
    
    def test_optional_n8n_connectivity(self):
        """Optional test to check if n8n instance is actually reachable"""
        log_path = Path("logs/n8n_setup.log")
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Extract URL
        url_pattern = re.compile(r'URL: (https?://[^\s]+)')
        url_match = url_pattern.search(content)
        
        if not url_match:
            pytest.skip("n8n URL not found in log")
        
        n8n_url = url_match.group(1)
        
        # Skip if URL is just a placeholder
        if "placeholder" in n8n_url:
            pytest.skip("n8n URL is just a placeholder")
        
        # Try to connect to n8n
        try:
            response = requests.get(n8n_url, timeout=5)
            assert response.status_code in [200, 301, 302, 307, 308], f"n8n instance not reachable, status code: {response.status_code}"
        except requests.RequestException as e:
            pytest.skip(f"Could not connect to n8n instance: {e}")


if __name__ == "__main__":
    pytest.main(["-v", "test_mt1_3_gateway_n8n.py"])