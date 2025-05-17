# HLT-TC-020: Verification of Data Erasure from Backend (Supabase)

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that when a user requests data erasure via the `/delete` command, all personally identifiable information (PII) related to that user is properly removed or anonymized in the Supabase backend, in compliance with POPIA's right to be forgotten.

## 2. User Story / Scenario
* **User Story (PRD 4.1):** *As a user, I want to be able to send `/delete` to erase my data so I have control over my personal information.*
* **Feature (PRD 5.1):** Self-Service Data Erasure: `/delete` command to wipe user data.
* **Scenario (HLT Strategy 4.5):** Test data erasure confirmation. After `/delete`, user receives confirmation, and subsequent attempts to access their data fail. Check Supabase for data removal.

## 3. Preconditions
* A test user is fully onboarded with Township Connect and has an active profile.
* The test user has generated some data in the system (e.g., logged sales, expenses, requested information).
* Database access is available for verification queries.
* The system has implemented the `/delete` command functionality.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | Before deletion, (simulated) run database queries to confirm the test user's data exists in Supabase | Database returns the user's profile information, transaction history, and any other associated data. |
| 2 | Test user sends the command: "/delete" | System responds with a confirmation request, asking the user to confirm they want to delete their data. |
| 3 | Test user confirms deletion: "Yes" or "Confirm" | System acknowledges the deletion request and informs the user that their data will be erased. Backend processes begin the data erasure operation. |
| 4 | Wait for the data erasure process to complete (may be immediate or slightly delayed depending on implementation) | System sends a final confirmation message that the data has been erased. |
| 5 | (Simulated) Run database queries to check user profile table | User's profile should either be completely removed or anonymized (e.g., name replaced with "Deleted User", contact information nullified or replaced with non-identifying values). |
| 6 | (Simulated) Run database queries to check transaction history tables | Transactions should either be completely removed or anonymized (user ID replaced with a non-identifying value while preserving non-PII data for analytics if required). |
| 7 | (Simulated) Run database queries to check any other tables that might contain user PII | All PII should be removed or anonymized across all tables. |
| 8 | Test user attempts to interact with the system again: "Hello" | System should treat the user as a new user, not recognizing their previous history. Onboarding process should begin again. |
| 9 | (Simulated) Check audit logs for the deletion operation | Audit logs should record that a deletion operation was performed, without containing the deleted PII itself. |

## 5. Acceptance Criteria (AI Verifiable)
* After the `/delete` command is processed, no personally identifiable information (PII) related to the user remains in the Supabase database in its original form.
* All user data is either:
  * Completely removed from the database, OR
  * Fully anonymized such that it cannot be linked back to the individual user
* The system maintains a record of the deletion operation itself (for audit purposes) without preserving the deleted PII.
* If the system preserves anonymized data for analytics purposes, this data cannot be used to identify the individual user.
* The user is treated as a completely new user if they attempt to interact with the system after deletion.
* The entire deletion process complies with POPIA requirements for the right to be forgotten.

## 6. References
* PRD Section 4.1: User Onboarding & Setup
* PRD Section 5.1: Self-Service Data Erasure
* High-Level Test Strategy Report Section 4.5: POPIA Compliance
* Master Acceptance Test Plan Section 3, Phase 5: POPIA Compliance Verification
* Protection of Personal Information Act (POPIA) requirements for data erasure

## 7. Notes
* This test focuses specifically on the backend data erasure, not just the user-facing confirmation messages.
* For AI verification purposes, database queries should be used to confirm the absence or anonymization of user data after deletion.
* The test should verify that all tables potentially containing user PII are checked, including:
  * User profiles
  * Transaction history
  * Message logs
  * Service bundle selections
  * Any other tables specific to Township Connect's implementation
* The specific anonymization approach may vary based on implementation details, but the key requirement is that the data can no longer be linked to the individual user.
* This test complements HLT-TC-003 (User Self-Service Data Erasure) but focuses specifically on backend verification rather than the user-facing process.