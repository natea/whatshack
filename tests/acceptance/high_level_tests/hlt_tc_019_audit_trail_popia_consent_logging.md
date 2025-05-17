# HLT-TC-019: Audit Trail for POPIA Consent Logging

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect properly logs and maintains an audit trail of user consent to POPIA notices, ensuring that each user's opt-in consent is recorded with a timestamp and the specific version of the notice they agreed to.

## 2. User Story / Scenario
* **User Story (PRD 4.1):** *As a user, I want to view a clear POPIA notice and provide opt-in consent so I understand how my data is used.*
* **Feature (PRD 5.1):** POPIA Compliance Module: Opt-in notice presentation and consent logging.
* **Scenario (HLT Strategy 4.5):** Audit trail for POPIA consent. System logs timestamped consent for each user. Admins can verify consent status.

## 3. Preconditions
* The system has a database schema that includes tables for storing user consent records.
* The POPIA notice has a version identifier that is included in consent records.
* Test users are available for onboarding.
* Database access is available for verification queries.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | New User A sends initial message: "Hello" | System detects language, sends welcome message, and presents POPIA notice with a version identifier (e.g., v1.0) in English. |
| 2 | User A responds with consent: "Yes, I agree" | System acknowledges consent and proceeds with onboarding. In the backend, the system logs User A's consent with: user ID, timestamp, POPIA notice version (v1.0), and consent status (true). |
| 3 | New User B sends initial message: "Molo" | System detects isiXhosa, sends welcome message, and presents POPIA notice with the same version identifier in isiXhosa. |
| 4 | User B responds with consent: "Ewe, ndiyavuma" | System acknowledges consent and proceeds with onboarding. In the backend, the system logs User B's consent with: user ID, timestamp, POPIA notice version (v1.0), and consent status (true). |
| 5 | (Simulated) System administrator runs a database query to retrieve consent records for Users A and B | Database returns complete consent records for both users, including user IDs, timestamps, POPIA notice versions, and consent statuses. |
| 6 | (Simulated) POPIA notice is updated to a new version (v1.1) | System database is updated with the new POPIA notice version. |
| 7 | New User C sends initial message: "Hallo" | System detects Afrikaans, sends welcome message, and presents the updated POPIA notice (v1.1) in Afrikaans. |
| 8 | User C responds with consent: "Ja, ek stem saam" | System acknowledges consent and proceeds with onboarding. In the backend, the system logs User C's consent with: user ID, timestamp, POPIA notice version (v1.1), and consent status (true). |
| 9 | (Simulated) System administrator runs a database query to retrieve all consent records | Database returns complete consent records for all users, showing different notice versions for users who consented before and after the notice update. |

## 5. Acceptance Criteria (AI Verifiable)
* For each user who completes onboarding, a consent record is created in the database with the following attributes:
  * Unique user identifier
  * Timestamp of when consent was provided
  * Version identifier of the POPIA notice that was presented
  * Consent status (true for opt-in)
  * Method of consent (e.g., WhatsApp message)
* Consent records are immutable once created (cannot be altered).
* Consent records are retained even if a user later deletes their account (may be anonymized but the record of consent remains).
* Database queries can retrieve consent records filtered by user ID, timestamp range, or notice version.
* The system correctly associates the appropriate POPIA notice version with each new user based on when they onboard.

## 6. References
* PRD Section 4.1: User Onboarding & Setup
* PRD Section 5.1: POPIA Compliance Module
* High-Level Test Strategy Report Section 4.5: POPIA Compliance
* Master Acceptance Test Plan Section 3, Phase 5: POPIA Compliance Verification
* Protection of Personal Information Act (POPIA) requirements

## 7. Notes
* This test focuses specifically on the logging and auditability of consent, not on the content or presentation of the POPIA notice itself.
* For AI verification purposes, database queries should be used to confirm the presence and correctness of consent records.
* In a production environment, these consent records would serve as legal proof of compliance with POPIA's consent requirements.
* The test should be expanded to include scenarios where a user initially declines consent and then later provides it, to ensure all consent interactions are properly logged.