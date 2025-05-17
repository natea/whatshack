# HLT-TC-023: Data Payload per Interaction (≤5KB)

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect maintains data efficiency by ensuring that all WhatsApp message interactions (both incoming and outgoing) have a payload size of ≤5KB, making the service accessible and affordable for users with limited data resources.

## 2. User Story / Scenario
* **Feature (PRD 2.3):** Ensure all interactions are highly data-efficient (≤5 KB per text interaction).
* **Scenario (HLT Strategy 4.6):** User performs a series of typical interactions. Each interaction's data payload (request and response) is ≤5KB. Measure using network monitoring tools.

## 3. Preconditions
* Township Connect is fully operational with all features enabled.
* Network monitoring tools or proxy setup is available to measure data payload sizes.
* Test WhatsApp account is set up and connected to Township Connect.
* Various typical user interactions are defined for testing.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response & Measurement |
|------|----------------------------|----------------------------------------|
| 1 | Set up network monitoring to capture WhatsApp message payloads | Monitoring tools are correctly configured to capture and measure data sizes. |
| 2 | Send a simple greeting: "Hello" | System responds with welcome message. Measure the size of both the outgoing "Hello" message and the incoming welcome response. Both should be ≤5KB. |
| 3 | Request a payment link: "SnapScan 75" | System generates and returns a payment link. Measure the size of both the outgoing request and the incoming payment link response. Both should be ≤5KB. |
| 4 | Log a sale: "Sale 50 snacks" | System confirms the sale has been logged. Measure the size of both the outgoing logging request and the incoming confirmation. Both should be ≤5KB. |
| 5 | Ask for business information: "How to register my business?" | System responds with business registration information. Measure the size of both the outgoing question and the incoming information response. Both should be ≤5KB. |
| 6 | Request directions: "Directions to Khayelitsha Clinic" | System provides text-based directions. Measure the size of both the outgoing request and the incoming directions. Both should be ≤5KB. |
| 7 | Request a business tip: "Give me a marketing tip" | System provides a business tip. Measure the size of both the outgoing request and the incoming tip. Both should be ≤5KB. |
| 8 | Switch language: "/lang afrikaans" | System confirms language change. Measure the size of both the outgoing command and the incoming confirmation. Both should be ≤5KB. |
| 9 | Trigger an error condition: "abcxyz" | System responds with an error message. Measure the size of both the outgoing invalid command and the incoming error message. Both should be ≤5KB. |
| 10 | Request data deletion: "/delete" | System asks for confirmation. Measure the size of both the outgoing command and the incoming confirmation request. Both should be ≤5KB. |

## 5. Acceptance Criteria (AI Verifiable)
* All incoming (system to user) WhatsApp message payloads are ≤5KB in size.
* All outgoing (user to system) WhatsApp message payloads are ≤5KB in size.
* The data efficiency requirement is met across all types of interactions:
  * Simple commands and confirmations
  * Information requests and responses
  * Transaction processing
  * Error messages
  * Language switching
  * Data management operations
* The system does not use techniques that would artificially reduce measured payload size while increasing actual data usage (e.g., triggering external downloads).
* The data efficiency is maintained across all three supported languages (English, isiXhosa, and Afrikaans).

## 6. References
* PRD Section 2.3: Specific Objectives - Ensure all interactions are highly data-efficient (≤5 KB per text interaction)
* High-Level Test Strategy Report Section 4.6: Performance and Data Efficiency
* Master Acceptance Test Plan Section 3, Phase 6: Performance and Data Efficiency

## 7. Notes
* This test focuses specifically on the data payload size, not on the functional correctness of the responses.
* For AI verification purposes, logs or screenshots from network monitoring tools showing payload sizes should be analyzed.
* The test should cover a representative sample of all major interaction types available in Township Connect.
* Special attention should be paid to responses that might naturally be longer, such as:
  * Information guides
  * Directions
  * Business tips
  * Error messages with detailed explanations
* If direct network monitoring is not possible, alternative methods such as:
  * WhatsApp API payload size analysis
  * Proxy server measurements
  * Simulated message size calculations based on character count and encoding
  * May be used as alternative verification approaches.
* This test is critical for ensuring Township Connect remains accessible to users with limited data resources, as specified in the PRD.