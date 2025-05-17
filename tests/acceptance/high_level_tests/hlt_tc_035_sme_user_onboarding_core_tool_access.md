# HLT-TC-035: SME User Onboarding and Core Tool Access for Pilot

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect supports the pilot program goal of onboarding 50 active SMEs by ensuring that new SME users can successfully complete the onboarding process, select appropriate service bundles, and access core business tools like sales logging and payment link generation.

## 2. User Story / Scenario
* **Feature (PRD 2.3):** Onboard at least 50 active Small and Medium Enterprises (SMEs) within the first 60 days of pilot.
* **Scenario:** A new SME user successfully completes onboarding, selects an SME-relevant bundle, and can successfully use core tools like sales logging and payment link generation. Database reflects the user as an SME.

## 3. Preconditions
* Township Connect is fully operational with all SME-focused features enabled.
* Test WhatsApp account is available that has not previously registered with Township Connect.
* SME-relevant service bundles (e.g., "Street-Vendor CRM", "Small Business", "Delivery Runner") are configured in the system.
* Database access is available for verification.

## 4. Test Steps

| Step | Test Action | Expected System Response & Verification |
|------|-------------|----------------------------------------|
| 1 | Scan QR code and initiate WhatsApp conversation with Township Connect by sending "Hello" | System responds with welcome message, language detection, POPIA notice, and request for consent. |
| 2 | Provide consent to POPIA notice | System acknowledges consent, logs it in database with timestamp, and presents service bundle options with clear descriptions of each bundle's features. |
| 3 | Select an SME-relevant bundle: "Street-Vendor CRM" | System confirms bundle selection, updates user profile in database with the selected bundle, and provides an introduction to the bundle's key features. Database record indicates user is an SME based on bundle selection. |
| 4 | Request help or guidance on available features | System provides a concise overview of available commands and features specific to the selected SME bundle. |
| 5 | Test core sales logging functionality: "Sale 50 sweets" | System confirms the sale has been logged. Database reflects the new sales entry associated with the user. |
| 6 | Test payment link generation: "SnapScan 75" | System generates and returns a valid SnapScan payment link or QR code. Transaction attempt is logged in database. |
| 7 | Test expense tracking: "Expense R30 transport" | System confirms the expense has been logged. Database reflects the new expense entry associated with the user. |
| 8 | Request a simple sales report or summary (if supported) | System provides a basic summary of recent sales activity. |
| 9 | Test at least one additional SME-specific feature from the selected bundle | Feature functions as expected. Appropriate database updates occur if applicable. |
| 10 | Repeat steps 1-9 with different SME-relevant bundles (e.g., "Small Business", "Delivery Runner") | All SME bundles can be successfully selected during onboarding, and their specific features function correctly. |

## 5. Acceptance Criteria (AI Verifiable)
* New users can successfully complete the onboarding process, including POPIA consent.
* SME-relevant service bundles are clearly presented with descriptions that help users make appropriate selections.
* Users can successfully select SME-relevant bundles during onboarding.
* The database correctly records the user's SME status and selected bundle.
* Core SME tools function correctly after onboarding:
  * Sales logging creates appropriate database records
  * Payment link generation produces valid, functional links
  * Expense tracking creates appropriate database records
  * Any bundle-specific features function as expected
* The onboarding process and core tools work consistently across all supported languages.
* The system can scale to support at least 50 concurrent active SME users.
* The entire process is data-efficient (≤5KB per interaction) and responsive (critical actions <10s).

## 6. References
* PRD Section 2.3: Specific Objectives - Onboard at least 50 active SMEs within the first 60 days of pilot
* PRD Section 4.1: User Onboarding & Setup
* PRD Section 4.2: Business & Finance (Entrepreneurs)
* PRD Section 5.1: Account Management & Onboarding
* PRD Section 5.2: Business & Finance Tools
* Master Acceptance Test Plan Section 3, Phase 9: Pilot Program Objective Validation

## 7. Notes
* This test specifically focuses on the SME onboarding and core tool access aspects of the system, which are critical for achieving the pilot program goal of 50 active SMEs.
* For AI verification purposes, database records and system logs should be analyzed to confirm successful onboarding and tool usage.
* The test should be performed with each of the SME-relevant service bundles to ensure all are functioning correctly.
* Special attention should be paid to:
  * Clarity of bundle descriptions to ensure SMEs select appropriate options
  * Functionality of core business tools that provide immediate value to SMEs
  * Database tracking of SME status for reporting on pilot program goals
  * Performance and reliability under load as the number of SME users increases
* This test complements earlier tests of individual features (e.g., HLT-TC-005, HLT-TC-007) but focuses specifically on the end-to-end SME experience from onboarding through core tool usage.
* Consider testing with various SME profiles (e.g., street vendor, spaza shop owner, tutor, delivery runner) to ensure the system meets the needs of different SME types.
* While this test verifies the system's capability to support 50 active SMEs, actual achievement of this pilot goal will depend on real-world adoption and usage.
* Verify that the onboarding process and core tools are accessible and usable on the types of devices commonly used by township SMEs, including low-end smartphones.