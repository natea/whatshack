# WhatsApp Gateway and n8n Setup Details

## 1. Gateway Selection

**Twilio** has been selected as the WhatsApp Gateway for the Township Connect project. This decision was made based on several factors including reliability, compliance with WhatsApp's terms of service, ease of integration with n8n, scalability, and professional support. For detailed rationale, see [Gateway Selection Rationale](gateway_selection_rationale.md).

## 2. n8n Instance Details

### Production n8n Instance
- **URL**: https://n-8-n-ai-native-workflow-automation-natejaunetow.replit.app
- **Status**: Functional and ready for integration

### Local Development/Testing Instance (Optional)
- A local n8n instance can be set up for development and testing purposes
- Local instance can be exposed via ngrok for webhook testing
- See [Local n8n Debugging Environment Setup Report](local_n8n_debugging_env_setup_report.md) for details

## 3. n8n API Key Management

The n8n API key should be securely stored and managed using the following approach:

- **Storage Location**: The API key should be stored as a Replit secret named `N8N_API_KEY`
- **Access Control**: Access to the Replit secrets should be restricted to authorized developers only
- **Usage in Code**: The API key should be accessed via environment variables in any code that needs to interact with the n8n API
- **Rotation Policy**: The API key should be rotated periodically (recommended every 90 days) and immediately upon any suspected compromise

## 4. Required Twilio Credentials

The following Twilio credentials are required for n8n integration:

1. **Account SID**: The unique identifier for your Twilio account
   - Format: Starts with "AC" followed by a 32-character string
   - Example: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

2. **Auth Token**: The authentication token for your Twilio account
   - Format: 32-character string
   - Note: Keep this secure and never expose it in client-side code

3. **WhatsApp Sender Number/Sandbox**:
   - For production: A Twilio WhatsApp-enabled phone number
   - For testing: Twilio WhatsApp Sandbox
   - Format: For production numbers, use E.164 format (e.g., `+27123456789`)

These credentials must be configured within n8n as a credential set of type "Twilio API" with the name "Twilio account" (as referenced in the workflow configuration).

## 5. Twilio Webhook Configuration

The Twilio WhatsApp Sandbox (or purchased number) must be configured to send inbound message webhooks to the n8n "Webhook" node URL. This is crucial for the system to receive incoming WhatsApp messages.

### Webhook URL Configuration

1. The webhook URL will be generated when the `Incoming_WhatsApp_Webhook_Twilio` n8n workflow is created and activated
2. The URL format will be: `https://n-8-n-ai-native-workflow-automation-natejaunetow.replit.app/webhook/twilio`
3. This URL must be configured in the Twilio console under:
   - For Sandbox: Messaging > Try it Out > WhatsApp > Sandbox Settings
   - For Production Number: Phone Numbers > Manage > Active Numbers > [Your Number] > Messaging Configuration

### Important Notes

- The webhook URL must be publicly accessible
- Twilio will send a POST request to this URL when a message is received
- The n8n workflow is configured to process this webhook and forward the message to the Python core handler
- For testing purposes, a local n8n instance with ngrok can be used to generate a temporary webhook URL

## 6. Verification

After configuration, send a test message to the Twilio WhatsApp number to verify that:
1. The message triggers the n8n webhook
2. The n8n workflow executes successfully
3. The Python core handler processes the message
4. A response is sent back to the WhatsApp user

This completes the foundational setup for the WhatsApp Gateway and n8n integration.