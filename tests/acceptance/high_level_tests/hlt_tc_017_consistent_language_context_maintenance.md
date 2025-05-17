# HLT-TC-017: Consistent Language Context Maintenance

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect maintains consistent language context throughout a user session with multiple interactions, ensuring that all system responses adhere to the user's selected or auto-detected language preference without any lapses.

## 2. User Story / Scenario
* **Feature (PRD 5.1):** Language Auto-Detection and Manual Language Switching.
* **Scenario:** A user interacts with multiple features consecutively in their chosen language, and the system maintains consistent language context throughout the session.

## 3. Preconditions
* A test WhatsApp account is available and registered with Township Connect.
* The system supports all three languages: English, isiXhosa, and Afrikaans.
* All required backend services (Supabase, n8n, Redis, etc.) are operational.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | Send a message in isiXhosa: "Molo" | System detects isiXhosa, responds in isiXhosa, and sets user language preference to isiXhosa in the database. |
| 2 | Log a sale in abbreviated format: "Sale 50" (using English word but in context of isiXhosa session) | System maintains isiXhosa context despite the English word "Sale", confirms the sale has been logged with a message in isiXhosa. |
| 3 | Request a payment link with minimal text: "SnapScan 75" | System maintains isiXhosa context, generates payment link with instructions in isiXhosa. |
| 4 | Send a message with code-switching (mixing languages): "Ndifuna ukwazi about business permits" | System maintains isiXhosa as the primary language, responds to the query about business permits in isiXhosa. |
| 5 | Switch language using command: "/lang english" | System acknowledges language change to English, updates user preference in database, and confirms the change in English. |
| 6 | Send a message with isiXhosa words: "Give me icebo for my business" | System maintains English as the primary language despite the isiXhosa word, responds in English. |
| 7 | Request information: "How to register a business?" | System responds in English with the requested information. |
| 8 | Switch language again: "/lang afrikaans" | System acknowledges language change to Afrikaans, updates user preference in database, and confirms the change in Afrikaans. |
| 9 | Send multiple consecutive requests in Afrikaans for different features (e.g., business tip, directions, expense logging) | System consistently responds in Afrikaans to all requests. |

## 5. Acceptance Criteria (AI Verifiable)
* The system correctly detects the initial language based on the greeting.
* Language preference is properly stored in the user's profile in the database.
* All system responses are in the user's current language preference, even when the user's input contains words from other languages.
* Language switching commands are correctly processed, and the system updates the user's language preference accordingly.
* After language switching, all subsequent responses are consistently in the newly selected language.
* The system maintains language context across different types of interactions (e.g., business functions, information requests, error messages).
* No lapses into incorrect languages occur at any point in the session.

## 6. References
* PRD Section 5.1: Account Management & Onboarding - Language Auto-Detection and Manual Language Switching
* PRD Section 6.2: Interface - WhatsApp-Native
* Master Acceptance Test Plan Section 3, Phase 4: Multilingual Support Verification

## 7. Notes
* This test specifically focuses on language consistency rather than functional correctness of the features being used.
* The test should verify that the system can handle code-switching (when users mix languages in a single message) while maintaining the primary language context.
* For AI verification purposes, all system responses should be logged and analyzed for language consistency.
* Special attention should be paid to edge cases like abbreviated commands, proper nouns, or technical terms that might be the same across languages.
* This test complements the end-to-end language journey tests (HLT-TC-014, HLT-TC-015, HLT-TC-016) by specifically focusing on language maintenance across transitions and mixed-language inputs.