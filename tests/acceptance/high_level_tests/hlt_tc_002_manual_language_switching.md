# HLT-TC-002: Manual Language Switching

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Gemini)

## 1. Test Overview
This High-Level Test (HLT) verifies that an existing, onboarded user can manually switch their preferred language for Township Connect interactions using a specific command.

## 2. User Story / Scenario
*   **User Story (PRD 4.1):** *As a user, I want to use a simple command like "/lang afrikaans" to switch my preferred language at any time.*
*   **Scenario (HLT Strategy 4.1):** An existing user wishes to change their language. User sends `/lang afrikaans`, system switches to Afrikaans for all subsequent interactions.

## 3. Preconditions
*   The test user is already onboarded and has an active session with Township Connect.
*   The user's current language preference is set to English (or any language other than the target language for switching).
*   The system is configured to support manual language switching via the `/lang [en|xh|af]` command.
*   Content for system responses (e.g., confirmation messages, sample interactions) is available in English, isiXhosa, and Afrikaans.

## 4. Test Steps

| Step | User Action (via WhatsApp)                               | Expected System Response (WhatsApp Message & Backend)                                                                                                                                                                                                                                                           | AI Verifiable Checks                                                                                                                                                                                                                                                                                                                                                                                       |
| :--- | :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | User (current language English) sends: `/lang afrikaans` | **System (WhatsApp):** Responds with a confirmation message in Afrikaans (e.g., "Taal is nou Afrikaans." / "Language is now Afrikaans.").<br>**System (Backend):** Updates the user's language preference in the Supabase database to 'af'. Logs the language change event.                                        | WhatsApp response received is in Afrikaans and matches the expected confirmation text. Supabase database query verifies the user's `language_preference` is updated to 'af'. Backend logs show the language change event.                                                                                                                                                                       |
| 2    | User sends a common command, e.g., "Help"                | **System (WhatsApp):** Responds with help information or a menu, entirely in Afrikaans.<br>**System (Backend):** Processes the "Help" command using Afrikaans language resources.                                                                                                                               | WhatsApp response content is entirely in Afrikaans and is appropriate for the "Help" command. Backend logs confirm request processed using Afrikaans language context.                                                                                                                                                                                                                                       |
| 3    | User (current language Afrikaans) sends: `/lang xhosa`   | **System (WhatsApp):** Responds with a confirmation message in isiXhosa (e.g., "Ulwimi ngoku luxhosa." / "Language is now isiXhosa.").<br>**System (Backend):** Updates the user's language preference in Supabase to 'xh'. Logs the language change.                                                              | WhatsApp response received is in isiXhosa and matches expected confirmation. Supabase query verifies `language_preference` is 'xh'. Backend logs show language change.                                                                                                                                                                                                                                   |
| 4    | User sends a common command, e.g., "Help"                | **System (WhatsApp):** Responds with help information or a menu, entirely in isiXhosa.<br>**System (Backend):** Processes the "Help" command using isiXhosa language resources.                                                                                                                                 | WhatsApp response content is entirely in isiXhosa. Backend logs confirm isiXhosa context.                                                                                                                                                                                                                                                                                                                              |
| 5    | User (current language isiXhosa) sends: `/lang english`  | **System (WhatsApp):** Responds with a confirmation message in English (e.g., "Language is now English.").<br>**System (Backend):** Updates the user's language preference in Supabase to 'en'. Logs the language change.                                                                                           | WhatsApp response received is in English and matches expected confirmation. Supabase query verifies `language_preference` is 'en'. Backend logs show language change.                                                                                                                                                                                                                                     |
| 6    | User sends a common command, e.g., "Help"                | **System (WhatsApp):** Responds with help information or a menu, entirely in English.<br>**System (Backend):** Processes the "Help" command using English language resources.                                                                                                                                   | WhatsApp response content is entirely in English. Backend logs confirm English context.                                                                                                                                                                                                                                                                                                                                |
| 7    | User sends an invalid language code, e.g., `/lang fr`    | **System (WhatsApp):** Responds with an error message in the user's current language (English), indicating the invalid language choice and listing supported languages (e.g., "Sorry, 'fr' is not a supported language. Please use /lang [en|xh|af].").<br>**System (Backend):** Logs the invalid attempt. | WhatsApp response is in English, matches the expected error message for invalid language. User's language preference in Supabase remains 'en'. Backend logs show the invalid language switch attempt.                                                                                                                                                                                                       |


## 5. Acceptance Criteria
*   **AC-01:** The system successfully changes the user's active language preference upon receiving a valid `/lang [target_language]` command.
    *   **AI Verifiable:** Supabase query confirms `language_preference` field is updated to the target language code (en, xh, af).
*   **AC-02:** The system sends a confirmation message in the *newly selected* language.
    *   **AI Verifiable:** WhatsApp response content and language match the expected confirmation for the new language.
*   **AC-03:** All subsequent interactions with the user (prompts, responses, error messages) are in the newly selected language until another `/lang` command is issued.
    *   **AI Verifiable:** Analysis of subsequent WhatsApp messages from the system confirms they are in the correct language. Backend logs show processing in the correct language context.
*   **AC-04:** The system provides a helpful error message in the *current* language if an invalid or unsupported language code is provided with the `/lang` command.
    *   **AI Verifiable:** WhatsApp error message content and language match expected output for invalid language selection. User's language preference in Supabase remains unchanged.
*   **AC-05:** Language switching is data-efficient (≤5KB per interaction).
    *   **AI Verifiable:** Network monitoring tool output (or payload size calculation) for each step shows data ≤5KB.

## 6. Dependencies & Assumptions
*   The `/lang` command processing logic is correctly implemented.
*   User's language preference is reliably stored and retrieved from Supabase.
*   All system message templates are available and correctly translated into English, isiXhosa, and Afrikaans.

## 7. References
*   PRD Section: 4.1 (User Onboarding & Setup - `/lang` command), 5.1 (Account Management & Onboarding - Manual Language Switching).
*   High-Level Test Strategy Report Section: 4.1 (User Onboarding & Account Management - Manual Language Switching).
*   Master Acceptance Test Plan: HLT-TC-002.