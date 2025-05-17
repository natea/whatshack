# HLT-TC-015: End-to-End User Journey in isiXhosa

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that users can complete an entire end-to-end journey through Township Connect in isiXhosa, with all system prompts and responses being accurate, natural, and consistent in isiXhosa language.

## 2. User Story / Scenario
* **Feature (PRD 6.2):** WhatsApp-Native interface with multilingual support.
* **Scenario:** A user completes a multi-step journey involving onboarding, business functionality, and information access entirely in isiXhosa.

## 3. Preconditions
* A test WhatsApp account is available and not previously registered with Township Connect.
* The system is configured to support isiXhosa language interactions.
* All required backend services (Supabase, n8n, Redis, etc.) are operational.
* Test payment gateway integrations are configured in sandbox/test mode.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | Scan QR code and send initial message: "Molo" | System detects isiXhosa language, sends welcome message in isiXhosa, presents POPIA notice in isiXhosa, and requests opt-in consent. |
| 2 | Reply with consent: "Ewe, ndiyavuma" | System acknowledges consent, logs it in database with timestamp, and presents service bundle options in isiXhosa. |
| 3 | Select a bundle: "Street-Vendor CRM" (or isiXhosa equivalent) | System confirms bundle selection, updates user profile in database, and provides a brief overview of available features in isiXhosa. |
| 4 | Log a sale: "Intengiso 50 iziselo" (Sale 50 drinks) | System confirms the sale has been logged, provides a brief confirmation message in isiXhosa. Database reflects the new sales entry. |
| 5 | Request a payment link: "SnapScan 75" | System generates and returns a valid SnapScan payment link or QR code with instructions in isiXhosa. Transaction is logged in database. |
| 6 | Ask for business information: "Ndingayifumana njani imvume yokuthengisa?" (How to get a trading permit?) | System responds with relevant information about trading permits in clear, natural isiXhosa. Response is data-light (≤5KB). |
| 7 | Request a business tip: "Ndinike icebo leshishini" (Give me a business tip) | System provides a relevant business tip in natural isiXhosa. Response is data-light (≤5KB). |
| 8 | Log an expense: "Inkcitho R30 isithuthi" (Expense R30 transport) | System confirms the expense has been logged with a message in isiXhosa. Database reflects the new expense entry. |
| 9 | Request directions: "Iindlela zokuya e-Khayelitsha Clinic" (Directions to Khayelitsha Clinic) | System provides concise, text-based directions in isiXhosa. Response is data-light (≤5KB). |

## 5. Acceptance Criteria (AI Verifiable)
* All system responses throughout the journey are in grammatically correct, natural isiXhosa.
* The language context is maintained as isiXhosa throughout the entire session without any lapses into other languages.
* Each functional step (sale logging, payment link generation, etc.) completes successfully with appropriate database updates.
* All text-based responses (information, tips, directions) are concise, relevant, and data-light (≤5KB).
* The system correctly processes and responds to all user commands in isiXhosa.
* User profile in database correctly reflects isiXhosa as the preferred language.
* All error messages or guidance (if triggered) are provided in isiXhosa.

## 6. References
* PRD Section 6.2: Interface - WhatsApp-Native
* PRD Section 5.1-5.4: Product Features
* Master Acceptance Test Plan Section 3, Phase 4: Multilingual Support Verification

## 7. Notes
* This test verifies both functional correctness and language consistency throughout a complete user journey.
* The test should be executed by a native or fluent isiXhosa speaker who can assess the naturalness and correctness of the language used.
* For AI verification purposes, all system responses should be logged and analyzed for language consistency, grammar, and appropriate terminology.
* Special attention should be paid to cultural nuances and context-appropriate expressions in isiXhosa.
* This test complements HLT-TC-014 (English journey) and HLT-TC-016 (Afrikaans journey), which follow the same steps but in different languages.