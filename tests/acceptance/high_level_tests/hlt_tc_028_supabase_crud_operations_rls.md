# HLT-TC-028: Supabase CRUD Operations and RLS Enforcement

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect correctly performs Create, Read, Update, and Delete (CRUD) operations against the Supabase database, and that Row-Level Security (RLS) policies are properly enforced for each operation type.

## 2. User Story / Scenario
* **Feature:** Supabase database integration with proper data access controls.
* **Scenario (HLT Strategy 4.7):** Test Supabase CRUD operations via typical user actions. Verification: Data is correctly created, read, updated, and deleted. RLS is enforced.

## 3. Preconditions
* Township Connect is fully operational with Supabase integration configured.
* Test WhatsApp accounts are set up for at least two different users (User A and User B).
* Supabase database has tables for user profiles, transactions, and other relevant data.
* Row-Level Security (RLS) policies are configured on all relevant tables.
* Database access is available for verification queries.

## 4. Test Steps

| Step | Test Action | Expected System Response & Verification |
|------|-------------|----------------------------------------|
| 1 | **CREATE Operations:** User A completes onboarding via WhatsApp | System creates a new user profile record in Supabase. Verify via database query that the record exists with correct data. |
| 2 | User A logs a sale: "Sale 50 snacks" | System creates a new sales record in Supabase. Verify via database query that the record exists with correct data and is associated with User A. |
| 3 | User A logs an expense: "Expense R30 transport" | System creates a new expense record in Supabase. Verify via database query that the record exists with correct data and is associated with User A. |
| 4 | **READ Operations:** User A requests a summary of recent sales | System reads sales records for User A from Supabase and returns a summary. Verify via logs that only User A's records were accessed. |
| 5 | User B attempts to access User A's sales data via a simulated API call | Access is denied by RLS policies. Verify via logs that the attempt was blocked and no data was returned. |
| 6 | **UPDATE Operations:** User A updates their language preference: "/lang afrikaans" | System updates User A's profile record in Supabase. Verify via database query that the language preference was updated correctly. |
| 7 | User A modifies a previous sale via a command like "Update sale 123 amount 75" (if supported) | System updates the specified sales record in Supabase. Verify via database query that the record was updated correctly. |
| 8 | User B attempts to update User A's profile data via a simulated API call | Update is denied by RLS policies. Verify via logs that the attempt was blocked and no data was modified. |
| 9 | **DELETE Operations:** User A deletes a specific record via an appropriate command (if supported) | System deletes the specified record from Supabase. Verify via database query that the record no longer exists. |
| 10 | User A requests account deletion: "/delete" and confirms | System executes deletion or anonymization of User A's data in Supabase. Verify via database queries that the data was properly removed or anonymized. |
| 11 | User B attempts to delete User A's data via a simulated API call | Deletion is denied by RLS policies. Verify via logs that the attempt was blocked and no data was deleted. |
| 12 | **Complex Scenarios:** Perform a series of mixed operations in sequence | All operations are executed correctly with proper RLS enforcement. Verify via database queries and logs that data state changes match expectations. |

## 5. Acceptance Criteria (AI Verifiable)
* All CREATE operations successfully insert new records with correct data into the appropriate Supabase tables.
* All READ operations successfully retrieve the correct data, limited to records the requesting user is authorized to access.
* All UPDATE operations successfully modify existing records, limited to records the requesting user is authorized to modify.
* All DELETE operations successfully remove or anonymize records, limited to records the requesting user is authorized to delete.
* Row-Level Security (RLS) policies correctly prevent users from accessing, modifying, or deleting data belonging to other users.
* Database transactions are atomic and consistent (e.g., related records are updated together or not at all).
* Error handling for database operations is robust (e.g., attempting to update non-existent records).
* The system maintains proper data integrity constraints (e.g., foreign key relationships).
* All database operations are properly logged for audit purposes.

## 6. References
* High-Level Test Strategy Report Section 4.7: API Integrations
* Master Acceptance Test Plan Section 3, Phase 7: API Integration Robustness
* HLT-TC-021: Data Segregation (Row-Level Security)
* Supabase documentation on CRUD operations and RLS

## 7. Notes
* This test focuses specifically on database operations and security, not on the functional correctness of the features using these operations.
* For AI verification purposes, database queries and operation logs should be analyzed.
* The test should cover all major data entities in the system, including but not limited to:
  * User profiles
  * Sales records
  * Expense records
  * Service bundle selections
  * Transaction history
  * Consent records
* Special attention should be paid to:
  * Edge cases such as concurrent operations
  * Error handling for invalid operations
  * Performance of database operations under load
  * Proper implementation of database transactions for multi-step operations
* This test complements HLT-TC-021 (Data Segregation) but focuses more broadly on all CRUD operations rather than just data access security.
* Consider testing with various user roles if the system implements role-based access control in addition to user-based RLS.
* Document any database optimization strategies implemented (e.g., indexing, query optimization) and verify they work as intended.