# HLT-TC-014: End-to-End User Journey in English

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that users can complete an entire end-to-end journey through Township Connect in English, with all system prompts and responses being accurate, natural, and consistent in English language.

## 2. User Story / Scenario
* **Feature (PRD 6.2):** WhatsApp-Native interface with multilingual support.
* **Scenario:** A user completes a multi-step journey involving onboarding, business functionality, and information access entirely in English.

## 3. Preconditions
* A test WhatsApp account is available and not previously registered with Township Connect.
* The system is configured to support English language interactions.
* All required backend services (Supabase, n8n, Redis, etc.) are operational.
* Test payment gateway integrations are configured in sandbox/test mode.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | Scan QR code and send initial message: "Hello" | System detects English language, sends welcome message in English, presents POPIA notice in English, and requests opt-in consent. |
| 2 | Reply with consent: "Yes, I agree" | System acknowledges consent, logs it in database with timestamp, and presents service bundle options in English. |
| 3 | Select a bundle: "Street-Vendor CRM" | System confirms bundle selection, updates user profile in database, and provides a brief overview of available features in English. |
| 4 | Log a sale: "Sale 50 snacks" | System confirms the sale has been logged, provides a brief confirmation message in English. Database reflects the new sales entry. |
| 5 | Request a payment link: "SnapScan 75" | System generates and returns a valid SnapScan payment link or QR code in English. Transaction is logged in database. |
| 6 | Ask for business information: "How to get a trading permit?" | System responds with relevant information about trading permits in clear, natural English. Response is data-light (≤5KB). |
| 7 | Request a business tip: "Give me a marketing tip" | System provides a relevant marketing tip in natural English. Response is data-light (≤5KB). |
| 8 | Log an expense: "Expense R30 transport" | System confirms the expense has been logged with a message in English. Database reflects the new expense entry. |
| 9 | Request directions: "Directions to Cape Town City Hall" | System provides concise, text-based directions in English. Response is data-light (≤5KB). |

## 5. Acceptance Criteria (AI Verifiable)
* All system responses throughout the journey are in grammatically correct, natural English.
* The language context is maintained as English throughout the entire session without any lapses into other languages.
* Each functional step (sale logging, payment link generation, etc.) completes successfully with appropriate database updates.
* All text-based responses (information, tips, directions) are concise, relevant, and data-light (≤5KB).
* The system correctly processes and responds to all user commands in English.
* User profile in database correctly reflects English as the preferred language.
* All error messages or guidance (if triggered) are provided in English.

## 6. References
* PRD Section 6.2: Interface - WhatsApp-Native
* PRD Section 5.1-5.4: Product Features
* Master Acceptance Test Plan Section 3, Phase 4: Multilingual Support Verification

## 7. Notes
* This test verifies both functional correctness and language consistency throughout a complete user journey.
* The test should be executed by a native or fluent English speaker who can assess the naturalness and correctness of the language used.
* For AI verification purposes, all system responses should be logged and analyzed for language consistency, grammar, and appropriate terminology.
* This test complements HLT-TC-015 (isiXhosa journey) and HLT-TC-016 (Afrikaans journey), which follow the same steps but in different languages.