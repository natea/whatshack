# QR Code Onboarding Flow

This document outlines the proposed flow for onboarding new users via a QR code mechanism and how a simulation of this flow is implemented for testing purposes.

## Ideal QR Code Triggered Onboarding

1.  **QR Code Scan**: A potential user scans a QR code.
2.  **Pre-filled Message**: The QR code is designed to open WhatsApp on the user's device and pre-fill a "Hi" message (or a similar generic greeting) addressed to the service's WhatsApp number.
    *   Example QR code data: `https://wa.me/YOUR_SERVICE_WHATSAPP_NUMBER?text=Hi`
3.  **User Sends Message**: The user sends the pre-filled message.
4.  **System Receives Message**: The system receives this "Hi" message from a WhatsApp number (`whatsapp_id`).

## Recognizing a QR-Initiated First Message

The system can recognize a message as potentially originating from a QR scan by identifying it as a "first message" from a new user. This is achieved by:

*   Checking if the `whatsapp_id` (phone number) of the sender is new to the system.
*   If the `whatsapp_id` does not exist in the `users` table in the Supabase database, the system treats this as a new user interaction.

While the exact content of the first message ("Hi") could be a weak indicator on its own, the primary mechanism for identifying a new user is the absence of their `whatsapp_id` in the database. For the purpose of this simulated flow, any first message from an unknown number will trigger the new user onboarding process.

## "Pairing Complete" Logic and Existing New User Flow

The existing "new user" onboarding flow, as defined in MT2.1 of the Master Project Plan, inherently serves as the "pairing complete" logic for users onboarded via this simulated QR flow.

When a message from a new `whatsapp_id` is received (simulating the "Hi" message sent after a QR scan):
1.  The system detects it's a new user.
2.  The standard new user onboarding process is initiated:
    *   Language detection/selection.
    *   POPIA consent.
    *   Welcome message.
    *   Creation of a new user record in the Supabase `users` table.

This existing flow correctly handles the registration and initial setup for any new user, regardless of whether their first interaction was manually composed or (in a real-world scenario) pre-filled by a QR code. Therefore, no new coding is required for the "pairing complete" aspect beyond the simulation command itself. The successful creation of the user record signifies that the "pairing" (i.e., associating the WhatsApp number with a user profile in the system) is complete.

## Development/Testing Simulation Command

For development and testing purposes, a command `"/simulate_qr_user [new_phone_number]"` is implemented. This command allows developers to directly trigger the new user onboarding flow for a specified phone number, mimicking the outcome of a new user sending their first message after a QR scan.