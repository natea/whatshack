# Plan: Core Message Handler Implementation (Township Connect)

**Version:** 1.0
**Date:** 2025-05-14

## 1. Overview

This document outlines the plan for implementing the **Core Message Handler** for the Township Connect WhatsApp Assistant. This work aligns with:
*   **Project Plan:** Micro-task 1.4 ("Python Core Logic - Basic Inbound Message Handling via n8n").
*   **.pheromone signal:** `township-priority-001` (High priority focus on Core Message Handler).
*   **PRD:** Sections 4.1, 5.1, 7.2, 8.1.

The primary goal is to create a Python-based handler that can receive WhatsApp message data (via n8n), process it, and prepare a reply.

## 2. Revised Priority & Approach

Based on recent feedback, the implementation will prioritize establishing a **basic end-to-end message flow with n8n integration first**. Supabase interactions (user creation, message logging) may be initially mocked or have minimal implementation to facilitate this end-to-end test.

Once the basic flow is confirmed, a Test-Driven Development (TDD) approach will be rigorously applied to:
*   Fully implement and test Supabase interactions for user management and message logging.
*   Develop and test other specific logic within the Core Message Handler.

## 3. Detailed Steps

### Phase A: Basic End-to-End Flow (n8n Integration Focus)

1.  **Define Minimal Message Structure:**
    *   Agree on the minimal JSON structure `core_handler.py` expects from n8n (e.g., `{'sender_id': 'whatsapp:+12345', 'text': 'Hello'}`).
    *   Agree on the minimal JSON structure `core_handler.py` will return to n8n (e.g., `{'reply_to': 'whatsapp:+12345', 'reply_text': 'Received: Hello'}`).

2.  **Skeleton `core_handler.py`:**
    *   Create a basic Python function `handle_incoming_message(message_data)` in `src/core_handler.py`.
    *   This function will initially parse `message_data`, construct a simple echo reply, and return it in the agreed-upon structure.
    *   Supabase calls for user lookup/creation and message logging will be **mocked** or be very simple stubs (e.g., print to console).

3.  **Basic n8n Workflow:**
    *   Set up a simple n8n workflow (as per Project Plan Micro-task 1.3, but can be simplified for this initial step):
        *   Webhook trigger to receive simulated WhatsApp messages.
        *   Node to call the Python `core_handler.py` script/function (e.g., via HTTP request if `core_handler` is exposed via a simple Flask/FastAPI endpoint for testing, or "Execute Command" node).
        *   Node to process the reply from `core_handler.py` and simulate sending it back.
    *   *Dependency Note:* This step might require coordination with whoever is setting up n8n if it's a separate task. For now, the focus is on the Python handler being callable.

4.  **End-to-End Test (Manual/Simulated):**
    *   Send a test JSON payload to the n8n webhook.
    *   Verify that `core_handler.py` is called.
    *   Verify that `core_handler.py` produces the expected simple reply structure.
    *   Verify that n8n receives this reply.

### Phase B: Full Implementation with TDD (Supabase & Logic Focus)

1.  **Test Design (TDD for Supabase Interactions & Core Logic):**
    *   Define detailed test cases in `pytest` for `core_handler.py`.
    *   **Test Case 1: New User - First Message (with Real Supabase)**
        *   Input: Message data from a new `sender_id`.
        *   Expected: New user in `users` table, message logged in `message_logs`, welcome reply prepared & logged.
    *   **Test Case 2: Existing User - Subsequent Message (with Real Supabase)**
        *   Input: Message data from an existing `sender_id`.
        *   Expected: User retrieved, message logged, echo reply prepared & logged.
    *   **Test Case 3: Message Logging Details**
        *   Input: Any message.
        *   Expected: `message_logs` entries correctly capture all required fields.
    *   (Further test cases for language detection, POPIA consent stubs, etc., as development progresses on those aspects of the Core Message Handler).

2.  **Supabase Client Implementation (`src/db/supabase_client.py` or similar):**
    *   Implement robust functions for:
        *   `get_user(whatsapp_id)`
        *   `create_user(whatsapp_id, preferred_language='en', popia_consent=False)`
        *   `log_message(user_whatsapp_id, direction, message_content, data_size_kb=0.1)` (data_size_kb to be refined later as per MT 5.1).
    *   Ensure proper connection handling and error management.

3.  **Core Logic Refinement (`src/core_handler.py`):**
    *   Replace mocked Supabase calls with actual calls to `supabase_client.py`.
    *   Implement logic for differentiating new vs. existing users.
    *   Implement initial reply logic (e.g., welcome for new users, echo for existing).
    *   Ensure all interactions are logged to Supabase.

4.  **Iterative TDD Cycle:**
    *   Write failing tests for specific functionalities.
    *   Write/modify code in `core_handler.py` and `supabase_client.py` to make tests pass.
    *   Refactor and repeat.

## 4. Key Considerations

*   **Credentials:** Supabase credentials will be managed via environment variables (placeholders from `.pheromone` to be used during initial local dev, actuals in Replit secrets later).
*   **Data Directories:** Placeholder directories `data/message_templates/` and `data/user_profiles/` will be created. Actual content and usage will be part of subsequent feature development.
*   **Error Handling:** Basic error handling will be incorporated in both Python and n8n workflows.
*   **Data Efficiency:** While the initial focus is flow, the ≤5 KB data target (PRD 8.1) must be kept in mind for message construction.

## 5. TDD Flow Diagram (Focus on Phase B)

```mermaid
graph TD
    A[Start: Implement Core Message Handler - Phase B] --> B{Write Test First};
    B -- Test for New User (Supabase) --> C[Define New User Test Case in `tests/test_core_handler.py`];
    C --> D[Implement `handle_incoming_message` in `core_handler.py` to pass New User Test];
    D -- Needs DB Interaction --> E[Implement/Refine `get_user`, `create_user`, `log_message` in `supabase_client.py`];
    E --> D;
    D -- Test Passes --> F{Write Test for Existing User (Supabase)};
    F --> G[Define Existing User Test Case in `tests/test_core_handler.py`];
    G --> H[Refine `handle_incoming_message` to pass Existing User Test];
    H -- Test Passes --> I{Write Test for Message Logging Details};
    I --> J[Define Logging Detail Test Case];
    J --> K[Refine `log_message` and its usage to pass Logging Test];
    K -- Test Passes --> L[All Core Handler Basic Tests Pass];
    L --> M[End: Core Message Handler Basics Implemented with TDD];

    subgraph "Supabase Client (`supabase_client.py`)"
        E
    end

    subgraph "Core Handler (`core_handler.py`)"
        D
        H
        K
    end

    subgraph "Tests (`tests/test_core_handler.py`)"
        C
        G
        J
    end
```

This plan will guide the initial development of the Core Message Handler, ensuring both early end-to-end visibility and subsequent robust, test-covered implementation.