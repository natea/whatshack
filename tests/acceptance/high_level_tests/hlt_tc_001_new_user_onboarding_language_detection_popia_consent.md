# HLT-TC-001: New User Onboarding, Language Auto-Detection, and POPIA Consent

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Gemini)

## 1. Test Overview
This High-Level Test (HLT) verifies the end-to-end process for a new user onboarding to Township Connect, including automatic language detection from an initial greeting, presentation of the POPIA notice, logging of user consent, and offering service bundle selection.

## 2. User Story / Scenario
*   **User Story (PRD 4.1):** *As a new user, I want to scan a QR code from a flyer to easily pair my phone with Township Connect so I can start using its services quickly.*
*   **User Story (PRD 4.1):** *As a user whose primary language is isiXhosa, I want the system to detect my language when I send "Molo" so that all further interactions are in isiXhosa.*
*   **User Story (PRD 4.1):** *As a user, I want to view a clear POPIA notice and provide opt-in consent so I understand how my data is used.*
*   **Scenario (HLT Strategy 4.1):** A new user scans a QR code, pairs their phone, and sends an initial greeting "Molo".
*   **Scenario (PRD 6.3 Onboarding Flow):** Scan QR -> Phone pairs -> User sends first text (e.g., "Hi") -> Bot replies in detected language (or default) -> User selects a free "bundle" -> Chat commands trigger background workflows.

## 3. Preconditions
*   A valid QR code for pairing with Township Connect is available and functional.
*   The Township Connect system (Baileys, Node.js, n8n, Supabase, Redis) is running and accessible.
*   The test user's WhatsApp number is not already registered in the system.
*   POPIA notice content and service bundle options are configured in the system for English, isiXhosa, and Afrikaans.
*   Language detection for "Molo" (isiXhosa), "Hallo" (Afrikaans), and "Hi" (English) is configured.

## 4. Test Steps

| Step | User Action (via WhatsApp)                                  | Expected System Response (WhatsApp Message & Backend)                                                                                                                                                                                                                            | AI Verifiable Checks                                                                                                                                                                                                                                                                                                                                                        |
| :--- | :---------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Scan QR code and initiate a WhatsApp session with the service. | **System (Backend):** Baileys pairs with the new WhatsApp number. A new user session is initiated.                                                                                                                                                                              | Backend logs confirm new WhatsApp connection established for the test user's number.                                                                                                                                                                                                                                                                                        |
| 2    | Send initial greeting: "Molo"                               | **System (WhatsApp):** Responds with a welcome message in isiXhosa. Presents the POPIA notice in isiXhosa, requesting opt-in consent (e.g., "Nceda phendula ngo 'Ewe' ukuze wamkele okanye 'Hayi' ukwala" / "Please reply 'Yes' to accept or 'No' to decline").<br>**System (Backend):** Detects language as isiXhosa. Logs the initial interaction.                   | WhatsApp response received is in isiXhosa. Response content matches the expected welcome and POPIA notice text for isiXhosa. Backend logs show language detected as isiXhosa for the user.                                                                                                                                                                                   |
| 3    | Send consent: "Ewe"                                         | **System (WhatsApp):** Responds with a confirmation of consent in isiXhosa. Presents options for service bundle selection in isiXhosa (e.g., "Street-Vendor CRM", "Community Info").<br>**System (Backend):** Logs the user's POPIA consent (opt-in) with a timestamp. User status updated to 'active' or 'consented'. | WhatsApp response received is in isiXhosa, confirming consent and presenting bundle options. Supabase database query verifies: 1. POPIA consent for the user is recorded as 'true' or 'accepted'. 2. Timestamp of consent is recorded. 3. User's language preference is stored as 'xh'. Backend logs confirm consent processing. |
| 4    | (Repeat steps 2-3 with "Hallo" for Afrikaans)               | **System (WhatsApp & Backend):** Similar flow as above, but all interactions are in Afrikaans.                                                                                                                                                                               | WhatsApp responses are in Afrikaans. Backend logs show language detected as Afrikaans. Supabase database shows consent and language preference 'af'.                                                                                                                                                                                                                         |
| 5    | (Repeat steps 2-3 with "Hi" for English)                    | **System (WhatsApp & Backend):** Similar flow as above, but all interactions are in English.                                                                                                                                                                                 | WhatsApp responses are in English. Backend logs show language detected as English. Supabase database shows consent and language preference 'en'.                                                                                                                                                                                                                             |

## 5. Acceptance Criteria
*   **AC-01:** The system successfully pairs with a new user's WhatsApp account upon QR code scan and initiation.
    *   **AI Verifiable:** Backend logs show successful Baileys pairing for the test user's number.
*   **AC-02:** The system correctly auto-detects the user's language from their initial greeting ("Molo" -> isiXhosa, "Hallo" -> Afrikaans, "Hi" -> English).
    *   **AI Verifiable:** Application logs confirm correct language detection. User's language preference is correctly stored in Supabase.
*   **AC-03:** The system presents the POPIA notice clearly in the detected language and requests explicit opt-in consent.
    *   **AI Verifiable:** WhatsApp message content matches the pre-defined POPIA notice for the detected language.
*   **AC-04:** The system correctly logs the user's POPIA consent (opt-in) with a timestamp in the Supabase database.
    *   **AI Verifiable:** Supabase query confirms `consent_given = true` (or equivalent) and a valid `consent_timestamp` for the user.
*   **AC-05:** After consent, the system presents service bundle selection options to the user in their chosen language.
    *   **AI Verifiable:** WhatsApp message content includes bundle options and is in the correct language.
*   **AC-06:** All interactions are data-efficient (≤5KB per interaction).
    *   **AI Verifiable:** Network monitoring tool output (or payload size calculation for WhatsApp messages) for each step shows data ≤5KB.

## 6. Dependencies & Assumptions
*   The content for welcome messages, POPIA notices, and bundle options in all three languages is accurately loaded into the system's content/template store.
*   The language detection module is correctly configured and functional for the specified greeting keywords.
*   Supabase schema includes fields for `user_id`, `phone_number`, `language_preference`, `popia_consent_given`, `popia_consent_timestamp`.

## 7. References
*   PRD Section: 4.1 (User Onboarding & Setup), 5.1 (Account Management & Onboarding), 6.3 (Onboarding Flow), 8.6 (Compliance - POPIA).
*   High-Level Test Strategy Report Section: 4.1 (User Onboarding & Account Management).
*   Master Acceptance Test Plan: HLT-TC-001.