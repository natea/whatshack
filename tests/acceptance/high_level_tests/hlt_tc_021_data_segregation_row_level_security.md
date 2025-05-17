# HLT-TC-021: Data Segregation (Row-Level Security)

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect properly implements data segregation through Supabase's Row-Level Security (RLS) policies, ensuring that users can only access their own data and not that of other users, in compliance with POPIA's data protection requirements.

## 2. User Story / Scenario
* **Feature (PRD 2.3):** Achieve 100% POPIA compliance, including data segregation.
* **Scenario (HLT Strategy 4.5):** Verify data segregation. Simulate one user attempting to access another user's data; access is denied due to Row-Level Security.

## 3. Preconditions
* At least two test users (User A and User B) are fully onboarded with Township Connect and have active profiles.
* Both test users have generated some data in the system (e.g., logged sales, expenses, requested information).
* Supabase is configured with Row-Level Security (RLS) policies on relevant tables.
* Test environment allows for simulated API calls or database queries with user-specific authentication tokens.

## 4. Test Steps

| Step | User Action (Simulated API/Database Access) | Expected System Response (Backend) |
|------|-------------------------------------------|-----------------------------------|
| 1 | Create test data: User A logs several sales and expenses via WhatsApp | System confirms the transactions. Database reflects User A's transactions with their user ID. |
| 2 | Create test data: User B logs different sales and expenses via WhatsApp | System confirms the transactions. Database reflects User B's transactions with their user ID. |
| 3 | Authenticate as User A and query the sales table for all records | Database returns only User A's sales records, not User B's. |
| 4 | Authenticate as User A and query the expenses table for all records | Database returns only User A's expense records, not User B's. |
| 5 | Authenticate as User A and attempt to query User B's profile information | Query returns no results or access is denied with an appropriate error message. |
| 6 | Authenticate as User B and query the sales table for all records | Database returns only User B's sales records, not User A's. |
| 7 | Authenticate as User B and query the expenses table for all records | Database returns only User B's expense records, not User A's. |
| 8 | Authenticate as User B and attempt to query User A's profile information | Query returns no results or access is denied with an appropriate error message. |
| 9 | Authenticate as an admin user with elevated permissions | Database returns records for both User A and User B, demonstrating that the data exists but is protected by RLS. |
| 10 | Attempt to bypass RLS by using SQL injection techniques in a simulated user input | System prevents the attack, maintaining data segregation. |

## 5. Acceptance Criteria (AI Verifiable)
* Row-Level Security (RLS) policies are properly implemented on all tables containing user data.
* When authenticated as a specific user, database queries only return that user's own data.
* Attempts to access another user's data are blocked by RLS policies.
* RLS policies do not prevent authorized administrative access for legitimate purposes.
* The system is resistant to common attempts to bypass RLS (e.g., SQL injection).
* RLS policies are consistently applied across all relevant tables in the database.
* The implementation complies with POPIA requirements for data protection and privacy.

## 6. References
* PRD Section 2.3: Specific Objectives - 100% POPIA compliance
* High-Level Test Strategy Report Section 4.5: POPIA Compliance
* Master Acceptance Test Plan Section 3, Phase 5: POPIA Compliance Verification
* Protection of Personal Information Act (POPIA) requirements for data protection
* Supabase documentation on Row-Level Security

## 7. Notes
* This test focuses specifically on the backend data segregation through RLS, not on the user interface restrictions.
* For AI verification purposes, database queries with different authentication contexts should be used to confirm the effectiveness of RLS policies.
* The test should be expanded to cover all tables containing user-specific data, not just the examples provided in the test steps.
* Special attention should be paid to edge cases, such as:
  * Shared resources (if any exist in the system)
  * Aggregated analytics data that might indirectly expose user information
  * Logs and audit trails that contain user identifiers
* This test is critical for POPIA compliance, as it ensures that users' personal information is protected from unauthorized access.
* In a production environment, regular security audits should include verification of RLS effectiveness.