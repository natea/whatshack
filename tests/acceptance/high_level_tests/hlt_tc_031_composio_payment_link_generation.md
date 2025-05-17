# HLT-TC-031: Composio Integration for Payment Link Generation

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect correctly integrates with Composio for payment link generation, ensuring that payment requests from users result in valid, functional payment links for supported payment providers (SnapScan, MoMo).

## 2. User Story / Scenario
* **User Story (PRD 4.2):** *As a spaza shop owner (Maria), when a customer wants to pay, I want to type "SnapScan 75" or "MoMo link 75" into Township Connect so I can quickly receive a payment link or QR code to share with my customer.*
* **Feature (PRD 5.2):** Payment Link Generation: Auto-generate SnapScan / MoMo payment links via simple commands.
* **Scenario (HLT Strategy 4.7):** A payment link generation request involving Composio results in a valid link. Composio logs or system logs show successful API interaction with the payment provider via Composio.

## 3. Preconditions
* Township Connect is fully operational with Composio integration configured.
* Test WhatsApp account is set up and connected to Township Connect.
* Composio is configured with test/sandbox accounts for payment providers (SnapScan, MoMo).
* System logging is configured to capture API interactions with Composio.
* Access to Composio logs is available (if possible).

## 4. Test Steps

| Step | Test Action | Expected System Response & Verification |
|------|-------------|----------------------------------------|
| 1 | Configure system logging to capture detailed information about Composio API interactions | Logging is correctly configured to capture API requests, responses, and error conditions. |
| 2 | **SnapScan Payment Link:** User sends the command "SnapScan 75" via WhatsApp | System parses the command correctly. System makes API call to Composio requesting a SnapScan payment link for R75. Composio returns a valid payment link. System forwards the payment link to the user via WhatsApp. System logs show successful API interaction. |
| 3 | Verify the received SnapScan payment link | Link has correct format for SnapScan. Link contains the correct amount (R75). Link is accessible when opened in a browser. Payment provider sandbox shows the pending payment. |
| 4 | **MoMo Payment Link:** User sends the command "MoMo link 100" via WhatsApp | System parses the command correctly. System makes API call to Composio requesting a MoMo payment link for R100. Composio returns a valid payment link. System forwards the payment link to the user via WhatsApp. System logs show successful API interaction. |
| 5 | Verify the received MoMo payment link | Link has correct format for MoMo. Link contains the correct amount (R100). Link is accessible when opened in a browser. Payment provider sandbox shows the pending payment. |
| 6 | **Error Handling:** User sends malformed payment request (e.g., "SnapScan abc") | System detects invalid amount. System responds with appropriate error message. No API call is made to Composio. System logs show validation failure. |
| 7 | **Error Handling:** Simulate Composio API failure (if possible) | System handles API failure gracefully. System provides appropriate error message to user. System logs show API failure and error handling. |
| 8 | **Concurrent Requests:** Multiple users simultaneously request payment links | All requests are processed correctly. Each user receives the correct payment link. No cross-contamination of requests occurs. System logs show successful processing of all requests. |
| 9 | **Transaction Logging:** Check that payment link generation is properly logged in the system | Database contains records of all payment link generation attempts, including timestamp, user ID, payment provider, amount, and success/failure status. |
| 10 | **Payment Completion:** If possible, simulate payment completion through the sandbox environment | System correctly handles payment completion notification (if implemented). User receives confirmation of payment (if implemented). Transaction status is updated in the database (if implemented). |

## 5. Acceptance Criteria (AI Verifiable)
* Payment link generation commands ("SnapScan [amount]" and "MoMo link [amount]") are correctly parsed and processed.
* API calls to Composio are correctly formatted with all required parameters.
* Generated payment links are valid, accessible, and contain the correct payment amount.
* Payment links are correctly delivered to users via WhatsApp.
* The system properly validates input before making API calls (e.g., ensuring amount is a valid number).
* Error conditions (invalid input, API failures) are handled gracefully with appropriate user feedback.
* Concurrent payment link requests are processed correctly without interference.
* All payment link generation attempts are properly logged for audit and troubleshooting purposes.
* If implemented, payment completion notifications are correctly processed and reflected in the system.
* The Composio integration demonstrates reliability and robustness under various conditions.

## 6. References
* PRD Section 4.2: Business & Finance (Entrepreneurs)
* PRD Section 5.2: Payment Link Generation
* High-Level Test Strategy Report Section 4.7: API Integrations
* Master Acceptance Test Plan Section 3, Phase 7: API Integration Robustness
* Composio documentation
* Payment provider (SnapScan, MoMo) documentation

## 7. Notes
* This test focuses specifically on the Composio integration for payment link generation, not on the detailed functionality of the payment providers themselves.
* For AI verification purposes, system logs, API interaction records, and generated payment links should be analyzed.
* The test should be performed in a sandbox/test environment to avoid actual financial transactions.
* Special attention should be paid to:
  * Security of API interactions (e.g., proper authentication, HTTPS)
  * Handling of sensitive payment information
  * Resilience to API failures or timeouts
  * Correct formatting of payment links for different providers
  * Transaction logging for reconciliation and audit purposes
* This test is critical for ensuring the reliability of a core business function for Township Connect users.
* Consider testing edge cases such as:
  * Minimum and maximum payment amounts
  * Special characters in reference fields (if supported)
  * International currency handling (if applicable)
* Verify that payment link generation performance meets the response time requirements established in HLT-TC-024.