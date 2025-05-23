# Diagnosis Report: Test Failures for Micro-task 2.4 (Manual Language Switching)

**Date:** 2025-05-18
**Feature Context:** Micro-task 2.4: Manual Language Switching (`/lang` command)
**Debugger:** AI Assistant

## 1. Overview

This report details the diagnosis of 5 test failures encountered during the `pytest` run after the attempted implementation of "Micro-task 2.4: Manual Language Switching." The failures are primarily related to Supabase setup, RLS configuration, and client interaction issues, rather than the language switching logic itself. These appear to be pre-existing problems.

## 2. Identified Failures & Root Causes

### Failure 1: `tests/test_supabase_setup.py::test_supabase_connection`
*   **Error:** `TypeError: Client.rpc() missing 1 required positional argument: 'params'`
*   **File & Line:** [`tests/test_supabase_setup.py:35`](tests/test_supabase_setup.py:35)
*   **Diagnosis:** The `supabase_client.rpc('version').execute()` call is missing the required `params` argument. The `supabase-py` library's `rpc` method expects a dictionary for parameters, even if it's empty.
*   **Root Cause:** Incorrect usage of the `supabase-py` client's `rpc` method.
*   **Suggested Fix:** Modify the call to `supabase_client.rpc('version', {}).execute()`.

### Failure 2: `tests/test_supabase_setup.py::test_apply_schema_script`
*   **Error:** `AssertionError: apply_supabase_schema.py failed with error: ... ERROR - Error executing SQL: SyncQueryRequestBuilder.execute() got an unexpected keyword argument 'options'`
*   **File & Line:** Test calls `scripts/apply_supabase_schema.py`. The error originates from [`src/db/supabase_client.py:88`](src/db/supabase_client.py:88) within the `execute_sql` function.
*   **Diagnosis:** The `scripts/apply_supabase_schema.py` script uses a custom `execute_sql` function ([`src/db/supabase_client.py:69`](src/db/supabase_client.py:69)) to apply SQL schema. This function incorrectly attempts to pass an `options` dictionary to the `supabase-py` client's `execute()` method when trying to run raw SQL via a POST request to `/rest/v1/`. The `execute()` method of a query builder does not support this `options` parameter for such an operation.
*   **Root Cause:** Flawed implementation of the `execute_sql` utility function in [`src/db/supabase_client.py`](src/db/supabase_client.py).
*   **Suggested Fix:** Refactor `execute_sql` to correctly execute raw SQL. This might involve using RPC calls for defined SQL functions in Supabase or ensuring the `service_role` key is used with appropriate client methods if direct schema manipulation is intended. For applying schema files, consider using Supabase's built-in migration tools or a more standard PostgreSQL library if complex scripting is needed with the service role.

### Failure 3: `tests/test_supabase_setup.py::test_configure_rls_script`
*   **Error:** `AssertionError: configure_rls.py failed with error: ... ERROR - Error executing SQL: SyncQueryRequestBuilder.execute() got an unexpected keyword argument 'options'`
*   **File & Line:** Test calls `scripts/configure_rls.py`. The error originates from [`src/db/supabase_client.py:88`](src/db/supabase_client.py:88) within the `execute_sql` function.
*   **Diagnosis:** Similar to `test_apply_schema_script`, the `scripts/configure_rls.py` script also relies on the same flawed `execute_sql` function to enable RLS and create policies.
*   **Root Cause:** Flawed implementation of the `execute_sql` utility function in [`src/db/supabase_client.py`](src/db/supabase_client.py).
*   **Suggested Fix:** Same as for `test_apply_schema_script`. RLS configuration SQL should be executed correctly.

### Failure 4: `tests/test_core_handler.py::test_handle_incoming_message_empty`
*   **Error:** `AssertionError: assert 'POPIA NOTICE' in "Welcome to Township Connect! ..."`
*   **Underlying Log Error:** `ERROR src.db.supabase_client:supabase_client.py:275 Exception during create_user: {'code': '42501', ..., 'message': 'new row violates row-level security policy for table "users"'}`
*   **File & Line:** Indirect failure; the test calls `handle_incoming_message`, which calls `create_user` in [`src/db/supabase_client.py:236`](src/db/supabase_client.py:236).
*   **Diagnosis:** The test fails because the `create_user` operation is blocked by RLS. This is a direct consequence of `scripts/apply_supabase_schema.py` and `scripts/configure_rls.py` failing to set up the schema and RLS policies correctly due to the `execute_sql` issue.
*   **Root Cause:** Cascading failure from improper schema/RLS setup.
*   **Suggested Fix:** Resolve the issues in `execute_sql`, `apply_supabase_schema.py`, and `configure_rls.py`.

### Failure 5: `tests/test_supabase_setup.py::test_insert_and_retrieve_user`
*   **Error:** `postgrest.exceptions.APIError: {'code': '42501', ..., 'message': 'new row violates row-level security policy for table "users"'}`
*   **File & Line:** [`tests/test_supabase_setup.py:232`](tests/test_supabase_setup.py:232) (user insertion).
*   **Diagnosis:** This test directly attempts to insert a user, which fails due to RLS policies not being correctly applied or the schema being in an inconsistent state because the setup scripts (`apply_supabase_schema.py`, `configure_rls.py`) failed.
*   **Root Cause:** Cascading failure from improper schema/RLS setup.
*   **Suggested Fix:** Resolve the issues in `execute_sql`, `apply_supabase_schema.py`, and `configure_rls.py`.

## 3. Impact of MT2.4 Changes

The code changes introduced for "Micro-task 2.4: Manual Language Switching" do **not** appear to be the direct cause of these 5 specific test failures. The identified issues are foundational, relating to how the application interacts with Supabase for schema management and basic operations.

## 4. Recommendations

1.  **Refactor `execute_sql` ([`src/db/supabase_client.py`](src/db/supabase_client.py)):**
    *   This function needs to be rewritten to correctly execute raw SQL against Supabase. The `supabase-py` library allows execution of PostgreSQL functions via `client.rpc('function_name', params)`. Schema and RLS setup commands should ideally be idempotent and managed through such functions or Supabase's migration CLI.
    *   If direct, arbitrary SQL execution is absolutely necessary (e.g., for scripting), it should be done with extreme caution, typically using a client initialized with the `SERVICE_ROLE_KEY` and ensuring the methods used are appropriate (e.g., not misusing query builder `execute()` methods).

2.  **Fix `test_supabase_connection`:**
    *   Update the RPC call in [`tests/test_supabase_setup.py:35`](tests/test_supabase_setup.py:35) to `supabase_client.rpc('version', {}).execute()`.

3.  **Verify Schema and RLS Scripts:**
    *   Once `execute_sql` (or its replacement approach) is fixed, thoroughly test `scripts/apply_supabase_schema.py` and `scripts/configure_rls.py` to ensure they correctly set up the database.

4.  **Re-run All Tests:** After addressing the above, re-run the entire test suite to confirm these foundational issues are resolved and to see if any new issues related to MT2.4 emerge.

Addressing these underlying problems is crucial for stable development and reliable testing of any features interacting with the Supabase backend.