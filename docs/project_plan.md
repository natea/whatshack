# Project Plan: Township Connect - WhatsApp Assistant

## Overall Project Goal (Derived from PRD):
Deliver a WhatsApp-native assistant ("Township Connect") for Cape Town township residents that provides accessible, data-light (≤5 KB/interaction) tools for business, services, and skills development in English, isiXhosa, and Afrikaans, achieving 100% POPIA compliance. The system will be ready to support the pilot program objectives, including onboarding 50 active SMEs and securing a paid corporate PoC within 90 days post-launch, as validated by PRD Sections 2.3 and 9.

---

## Phase 1: Foundation Setup & Core Infrastructure
**Phase AI-Verifiable End Goal:** All micro-tasks in Phase 1 are complete. A Supabase project in `af-south-1` is configured with initial user and core data schemas. A Python-based application connected to a selected WhatsApp Gateway (WAHA or Twilio via n8n) can receive and log an inbound test message. Basic CI/CD is functional for the Python core logic.
**Relevant PRD Sections/Requirements:** PRD Sections 7 (Platform and Technical Requirements), 8.5 (Security - initial setup), 8.6 (Compliance - data residency).

### Micro-task 1.1: Hosting and Repository Setup
*   **Task Description:** Establish Replit Reserved-VM, Git repository, and basic CI/CD pipeline for Python core logic.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A Replit Reserved-VM is provisioned and accessible (URL or ID noted).
    2.  A Git repository (URL noted) is created.
    3.  A `main.py` (or similar entry point for Python) file exists in the repository.
    4.  A CI pipeline configuration file (e.g., `.github/workflows/python-ci.yml` or Replit CI equivalent) exists.
    5.  The CI pipeline executes successfully (e.g., linting with Flake8 passes, a basic placeholder test in `tests/test_smoke.py` that `import main` passes) upon a test commit to the repository.
*   **Relevant PRD Sections/Requirements:** PRD Section 7.2 (Hosting).

### Micro-task 1.2: Supabase Project Initialization & Schema Definition
*   **Task Description:** Create and configure Supabase project ensuring data residency. Define initial database schemas for core entities.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A Supabase project (Project ID logged) is created and confirmed to be hosted in the `af-south-1` region.
    2.  Database connection string and service key for the Supabase project are securely stored (e.g., as Replit secrets).
    3.  A SQL script `db_schema_v1.sql` exists in the repository containing `CREATE TABLE` statements for at least:
        *   `users` (with fields like `whatsapp_id` (PRIMARY KEY, TEXT UNIQUE), `preferred_language` (TEXT, default 'en'), `current_bundle` (TEXT), `popia_consent_given` (BOOLEAN, default FALSE), `created_at` (TIMESTAMPTZ), `last_active_at` (TIMESTAMPTZ), `baileys_creds_encrypted` (TEXT, if applicable and implies future need for user-specific encryption for session resumption if Baileys were user-specific)).
        *   `service_bundles` (with fields like `bundle_id` (TEXT, PRIMARY KEY), `bundle_name_en` (TEXT), `bundle_name_xh` (TEXT), `bundle_name_af` (TEXT), `description_en` (TEXT), `description_xh` (TEXT), `description_af` (TEXT)).
        *   `message_logs` (with fields like `log_id` (SERIAL PRIMARY KEY), `user_whatsapp_id` (TEXT REFERENCES users(whatsapp_id)), `direction` (TEXT, 'inbound'/'outbound'), `message_content` (TEXT), `timestamp` (TIMESTAMPTZ), `data_size_kb` (FLOAT)).
    4.  The `db_schema_v1.sql` script executes successfully against the Supabase project either via Supabase Studio SQL editor or a CLI tool, resulting in the creation of these tables.
    5.  Row-Level Security (RLS) is enabled on the `users` table (basic policy: `users.whatsapp_id = auth.uid()` if using Supabase Auth per user, or a placeholder for app-level user ID checks).
*   **Relevant PRD Sections/Requirements:** PRD Sections 7.2 (Database), 7.3 (Data Residency), 8.5 (Data Segregation - initial RLS).

### Micro-task 1.3: WhatsApp Gateway Selection, Setup & Initial n8n Configuration
*   **Task Description:** Select and configure one WhatsApp Gateway (WAHA with n8n integration or Twilio with n8n integration as primary options). Configure basic n8n webhook for incoming messages.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  Decision for WhatsApp Gateway (WAHA or Twilio) is logged.
    2.  A functional n8n instance is running (either self-hosted on Replit if feasible or using n8n cloud). URL and API key for n8n are logged/stored.
    3.  For **WAHA with n8n:**
        *   WAHA instance is running and accessible (URL logged).
        *   The WAHA n8n custom node/plugin is installed and configured in the n8n instance.
        *   A WAHA session for a test WhatsApp number is active and logs `Session status: "ONLINE"`.
        *   An n8n workflow exists named `Incoming_WhatsApp_Webhook_WAHA` which is triggered by the WAHA "Message Received" node.
    4.  For **Twilio with n8n:**
        *   Twilio account SID, Auth Token, and a Twilio WhatsApp sender number are configured as n8n credentials.
        *   A Twilio WhatsApp Sandbox (or a purchased number) is configured to send inbound message webhooks to a specific n8n "Webhook" node URL.
        *   An n8n workflow exists named `Incoming_WhatsApp_Webhook_Twilio` which is triggered by the Twilio "Webhook" node.
    5.  A log file (e.g., `n8n_setup.log`) or a screenshot of the n8n workflow shows the selected gateway's "Message Received" trigger successfully activating upon sending a test message to the configured test WhatsApp number.
*   **Relevant PRD Sections/Requirements:** PRD Section 7.2 (WhatsApp Integration, Orchestration).

### Micro-task 1.4: Python Core Logic - Basic Inbound Message Handling via n8n
*   **Task Description:** Develop a Python script callable by n8n to receive message data, log it to Supabase, and send a basic echo reply.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A Python script (e.g., `core_handler.py`) exists containing a function `handle_incoming_message(message_data_json_string)`.
    2.  The function, when called with a JSON string representing a test WhatsApp message (e.g., `{'sender_id': 'whatsapp:+12345', 'text': 'Test Message'}`), successfully parses it.
    3.  The Python function uses the Supabase client library (e.g., `supabase-py`) to insert a record into the `message_logs` table in Supabase (verified by querying Supabase: `SELECT COUNT(*) FROM message_logs WHERE user_whatsapp_id = 'whatsapp:+12345' AND message_content = 'Test Message'` returns 1).
    4.  The Python function returns a JSON string for n8n to process, e.g., `{'reply_to': 'whatsapp:+12345', 'reply_text': 'Echo: Test Message'}`.
    5.  The n8n workflow (from 1.3) is updated to call this Python script (e.g., via an "Execute Command" node or an HTTP request to a simple Python HTTP server if exposed).
    6.  Upon sending "Hello Bot" to the test WhatsApp number, a reply "Echo: Hello Bot" is received on the originating WhatsApp client, and the `message_logs` table in Supabase shows both the inbound "Hello Bot" and a conceptual outbound "Echo: Hello Bot" log entry.
*   **Relevant PRD Sections/Requirements:** PRD Section 7.2 (Core Logic), 5 (basic interaction).

### Micro-task 1.5: Redis Streams (Upstash) Basic Setup
*   **Task Description:** Set up Upstash Redis and configure Python application for basic message queue publishing (for future worker scaling).
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  An Upstash Redis instance is created; connection details (host, port, password) are logged/stored securely.
    2.  The `core_handler.py` Python script from MT1.4 is modified: after receiving a message (before sending echo), it successfully publishes the `message_data_json_string` to a Redis Stream named `incoming_whatsapp_messages` using a Python Redis client (e.g., `redis-py`).
    3.  A separate utility script `check_redis_stream.py` can connect to Upstash and read at least one message from the `incoming_whatsapp_messages` stream after a test message is sent through the system. The content of the read message matches the sent test message data.
*   **Relevant PRD Sections/Requirements:** PRD Section 7.2 (Message Queuing).

---

## Phase 2: User Account Management, Onboarding & POPIA Compliance
**Phase AI-Verifiable End Goal:** All micro-tasks in Phase 2 are complete. A new user sending a message for the first time is created in Supabase `users` table, POPIA notice is sent, language is detected/set. Existing users are identified. Users can switch language and request data deletion. All these interactions are logged. The system correctly handles user identification for ongoing interactions.
**Relevant PRD Sections/Requirements:** PRD Sections 4.1, 5.1, 8.5 (Security - RLS for user data), 8.6 (POPIA).

### Micro-task 2.1: User Identification & Creation in Python Core Logic
*   **Task Description:** Enhance `core_handler.py` to check if an incoming `sender_id` exists in Supabase `users` table. If not, create a new user entry. If exists, retrieve user details.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` function `handle_incoming_message` modifies behavior:
        *   Upon receiving a message from a `sender_id` not in `users` table, it inserts a new row into `users` with the `sender_id` (as `whatsapp_id`), default `preferred_language` ('en'), and `popia_consent_given` (FALSE). `SELECT COUNT(*) FROM users WHERE whatsapp_id = 'new_test_user_id'` returns 1 after first message.
        *   Upon receiving a message from an existing `sender_id`, it successfully queries and retrieves `preferred_language` and `popia_consent_given` for that user from Supabase. (Log output from Python confirms retrieval).
    2.  Unit tests in `tests/test_user_management.py` for this user check/creation logic pass.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.1, 4.1 (first interaction).

### Micro-task 2.2: POPIA Notice Presentation & Consent Logging
*   **Task Description:** Implement logic to send POPIA notice on first interaction and log user consent (simulated for now, explicit opt-in mechanism for later).
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A plain text file `popia_notice_en.txt` (and placeholders `popia_notice_xh.txt`, `popia_notice_af.txt`) exists in a `content/` directory, containing the POPIA notice.
    2.  `core_handler.py`: If a user is newly created (or `popia_consent_given` is FALSE), the system prepares to send the content of `popia_notice_en.txt` (or language-specific once lang detection is in) as a WhatsApp reply *before* any other functional reply.
    3.  For simulation: If the user's first message is specifically "AGREE POPIA", the `popia_consent_given` field for that user in Supabase is updated to TRUE. `SELECT popia_consent_given FROM users WHERE whatsapp_id = 'test_user_agreeing'` returns TRUE.
    4.  The fact that the POPIA notice was sent (message content or a flag "POPIA_NOTICE_SENT") is logged in `message_logs` for the user.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.1 (POPIA Compliance Module), 4.1.

### Micro-task 2.3: Basic Language Auto-Detection and Storage
*   **Task Description:** Implement initial language detection from common greetings and store user's preferred language.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A Python function `detect_initial_language(message_text)` in `language_utils.py` exists.
    2.  `detect_initial_language("Hi")` returns "en".
    3.  `detect_initial_language("Molo")` returns "xh".
    4.  `detect_initial_language("Hallo")` returns "af".
    5.  `detect_initial_language("Test")` returns a default (e.g., "en" or None).
    6.  When a new user sends "Molo" as their first message:
        *   The `detect_initial_language` function is called.
        *   The `preferred_language` field for that new user in Supabase `users` table is set to "xh". `SELECT preferred_language FROM users WHERE whatsapp_id = 'xhosa_test_user'` returns "xh".
    7.  Unit tests in `tests/test_language_utils.py` for `detect_initial_language` pass.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.1 (Language Auto-Detection), 4.1.

### Micro-task 2.4: Manual Language Switching (`/lang` command)
*   **Task Description:** Implement `/lang [en|xh|af]` command to allow users to change their preferred language.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects if an incoming message is `"/lang en"`, `"/lang xh"`, or `"/lang af"`.
    2.  If detected, the `preferred_language` field in the Supabase `users` table for that `sender_id` is updated to "en", "xh", or "af" respectively. Verified by `SELECT preferred_language FROM users WHERE whatsapp_id = 'user_switching_lang'` returning the new language.
    3.  A confirmation message (e.g., "Language set to English.", "Ulwimi lusetelwe kwiXhosa.", "Taal ingestel op Afrikaans.") is prepared for sending back to the user in the *newly selected* language. (Message content is defined in `content/lang_confirmation_[lang].txt`).
    4.  An automated test script sends "/lang xh" for a test user; then `SELECT preferred_language FROM users ...` confirms "xh"; then the system sends a test command, and the reply's language marker (if any, or just logging) shows it's using Xhosa.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.1 (Manual Language Switching), 4.1.

### Micro-task 2.5: Self-Service Data Erasure (`/delete` command)
*   **Task Description:** Implement the `/delete` command to wipe user data from relevant tables.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A Supabase SQL function `hard_delete_user_data(user_whatsapp_id TEXT)` exists.
    2.  This SQL function, when executed, deletes all records from `message_logs` and other related data tables (e.g., future `sales_logs`, `expense_logs` if designed with `user_whatsapp_id` FOREIGN KEY and CASCADE DELETE) for the given `user_whatsapp_id`. Finally, it deletes the user from the `users` table.
    3.  `core_handler.py` detects if an incoming message is `"/delete"`.
    4.  If detected, it first sends a confirmation request message like "Are you sure you want to delete all your data? Reply '/delete confirm' to proceed." (Content in `content/delete_prompt_en.txt` etc.)
    5.  If the next message from the same user within N minutes is `"/delete confirm"`, the Python script calls the `hard_delete_user_data` Supabase function with the user's `sender_id`.
    6.  After successful execution of `/delete confirm` by a test user:
        *   `SELECT COUNT(*) FROM users WHERE whatsapp_id = 'deleted_test_user'` returns 0.
        *   `SELECT COUNT(*) FROM message_logs WHERE user_whatsapp_id = 'deleted_test_user'` returns 0.
    7.  A final acknowledgment "Your data has been deleted." (from `content/delete_ack_en.txt` etc.) is sent to the user *before* their session is effectively ended from the system's perspective.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.1 (Self-Service Data Erasure), 4.1, 8.6 (POPIA right-to-be-forgotten).

### Micro-task 2.6: QR Code Onboarding Flow Definition & Placeholder
*   **Task Description:** Define the technical flow for QR code onboarding and implement a placeholder for pairing initiation. (Actual QR generation and initial message prefill via QR might be dependent on WhatsApp Gateway capabilities and outside direct AI control).
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A document `qr_onboarding_flow.md` is created outlining:
        *   How a QR code would ideally trigger a pre-filled "Hi" message to the service's WhatsApp number.
        *   How the system recognizes a "first message" as potentially coming from a QR scan (e.g., by checking if the user `whatsapp_id` is new).
    2.  The existing "new user" flow from MT2.1 serves as the "pairing complete" logic.
    3.  A specific test command, e.g., `"/simulate_qr_user [new_phone_number]"`, when processed by `core_handler.py` (dev/test only), triggers the new user creation flow for `[new_phone_number]` as if they sent their first message. This is verified by checking the Supabase `users` table for `[new_phone_number]`.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.1 (QR Code Phone Pairing), 6.3.

### Micro-task 2.7: Service Bundle Selection - Data Structure & Basic Logic
*   **Task Description:** Populate `service_bundles` table and allow a user to select a bundle, storing it on their user record.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  The `service_bundles` table in Supabase is populated with at least one test bundle, e.g., ('street_vendor_crm', 'Street-Vendor CRM', 'Isixhobo soThengiso', 'Straatverkoper CRM', 'Tools for street vendors.', ..., ...).
    2.  When a new user is created (or an existing user has no bundle), `core_handler.py` sends a message listing available bundles by querying `service_bundles` (e.g., "Choose a bundle: 1. Street-Vendor CRM. Reply with number."). (Content from `content/bundle_select_prompt_en.txt` etc., with dynamic list).
    3.  If the user replies with a valid number corresponding to a `bundle_id`, the `current_bundle` field in their `users` Supabase record is updated with that `bundle_id`. Verified by `SELECT current_bundle FROM users WHERE whatsapp_id = 'user_choosing_bundle'` returning the selected bundle_id.
    4.  A confirmation like "Bundle 'Street-Vendor CRM' selected!" is sent.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.1 (Service Bundle Selection), 4.1.

---

## Phase 3: Core Feature Implementation - Business & Finance Tools
**Phase AI-Verifiable End Goal:** All micro-tasks in Phase 3 are complete. Users associated with the "Street-Vendor CRM" bundle can generate payment links (mocked Composio/n8n interaction), log sales, and track expenses. These transactions are stored in Supabase, linked to the user. Basic customer communication placeholders are functional.
**Relevant PRD Sections/Requirements:** PRD Sections 4.2, 5.2, 7.2 (Composio, n8n for payments).

### Micro-task 3.1: Composio/n8n Setup for Mock Payment Link Generation
*   **Task Description:** Set up Composio for SnapScan/MoMo (or mock equivalent if live access not yet available for dev) and an n8n workflow to be triggered by Python for payment link generation.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A Composio account is set up.
    2.  Connectors for SnapScan and MoMo are explored/configured in Composio (even if pointing to sandbox/mock endpoints for now). A log or screenshot shows configured SnapScan/MoMo actions in Composio.
    3.  An n8n workflow named `Generate_Payment_Link_n8n` exists.
    4.  This workflow has an HTTP webhook trigger.
    5.  The workflow includes nodes that (conceptually or via mock service calls logged by Composio/n8n) represent:
        *   Receiving `amount`, `provider` (SnapScan/MoMo), `user_id` from the webhook.
        *   Calling the Composio "Generate Payment Link" action for the specified provider and amount.
        *   Returning a mock payment link (e.g., `{"payment_link": "https://mock.snapscan.com/pay/test123"}`) or an error structure.
    6.  Calling the n8n webhook URL (e.g., via `curl` or Postman) with `{"amount": 100, "provider": "SnapScan", "user_id": "test_user"}` results in the n8n workflow log showing successful execution and the mock payment link structure is returned in the HTTP response from n8n.
*   **Relevant PRD Sections/Requirements:** PRD Section 7.2 (Composio, n8n), 5.2 (Payment Link Generation).

### Micro-task 3.2: Database Schema for Business Transactions
*   **Task Description:** Create Supabase tables for `payment_transactions`, `sales_logs`, and `expense_logs`.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  SQL `CREATE TABLE` statements are added to `db_schema_v1.sql` (or a new `db_schema_v2.sql`) for:
        *   `payment_transactions` (`transaction_id` SERIAL PK, `user_whatsapp_id` TEXT FK, `provider` TEXT, `amount` DECIMAL, `link_generated` TEXT, `status` TEXT DEFAULT 'pending', `created_at` TIMESTAMPTZ).
        *   `sales_logs` (`sale_id` SERIAL PK, `user_whatsapp_id` TEXT FK, `description` TEXT, `amount` DECIMAL, `payment_transaction_id` INT FK NULL, `sale_date` TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP).
        *   `expense_logs` (`expense_id` SERIAL PK, `user_whatsapp_id` TEXT FK, `description` TEXT, `amount` DECIMAL, `expense_date` TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP).
    2.  The SQL script executes successfully against Supabase, creating these tables.
    3.  RLS is enabled on these tables to ensure a user can only access their own transactions (e.g., policy `user_whatsapp_id = current_setting('request.jwt.claims', true)::json->>'sub'` if using Supabase Auth JWT, or similar application-level checks if custom auth).
*   **Relevant PRD Sections/Requirements:** PRD Section 5.2, general data management.

### Micro-task 3.3: Python Logic for "Generate Payment Link" Command
*   **Task Description:** Implement user command (e.g., "Pay R75" or "Snapscan 75") in `core_handler.py` to trigger the n8n payment link workflow.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects commands like `"Pay [Amount]"`, `"SnapScan [Amount]"`, `"MoMo link [Amount]"`.
    2.  It parses `Amount` and `provider` (SnapScan/MoMo, defaulting if "Pay" is used and user has a preference or only one option configured for their bundle).
    3.  It makes an HTTP POST request to the `Generate_Payment_Link_n8n` webhook URL (from MT3.1) with payload `{"amount": ParsedAmount, "provider": ParsedProvider, "user_id": sender_id}`.
    4.  It receives the JSON response from n8n.
    5.  A new record is inserted into `payment_transactions` table in Supabase with the amount, provider, user_id, and the received `payment_link`. `SELECT COUNT(*) FROM payment_transactions WHERE user_whatsapp_id = 'test_user' AND amount = 75` returns 1.
    6.  The `payment_link` from the n8n response is formatted and sent back to the user as a WhatsApp message (e.g., "Here's the SnapScan link for R75: [link]. To log this sale once paid, reply 'Log sale 75'.").
*   **Relevant PRD Sections/Requirements:** PRD Section 5.2 (Payment Link Generation), 4.2.

### Micro-task 3.4: Python Logic for "Log Sale" Command
*   **Task Description:** Implement user command (e.g., "Log sale 75 sweets") in `core_handler.py`.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects command like `"Log sale [Amount] [Description]"`.
    2.  It parses `Amount` and `Description`.
    3.  A new record is inserted into `sales_logs` table in Supabase with `user_whatsapp_id`, `Description`, `Amount`. `SELECT COUNT(*) FROM sales_logs WHERE user_whatsapp_id = 'test_user' AND amount = 75 AND description = 'sweets'` returns 1.
    4.  A confirmation message (e.g., "Sale of R75 for 'sweets' logged.") is sent to the user.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.2 (Sales Logging), 4.2.

### Micro-task 3.5: Python Logic for "Track Expense" Command
*   **Task Description:** Implement user command (e.g., "Expense R50 airtime") in `core_handler.py`.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects command like `"Expense [Amount] [Description]"`.
    2.  It parses `Amount` and `Description`.
    3.  A new record is inserted into `expense_logs` table in Supabase with `user_whatsapp_id`, `Description`, `Amount`. `SELECT COUNT(*) FROM expense_logs WHERE user_whatsapp_id = 'test_user' AND amount = 50 AND description = 'airtime'` returns 1.
    4.  A confirmation message (e.g., "Expense of R50 for 'airtime' logged.") is sent to the user.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.2 (Expense Tracking), 4.2.

### Micro-task 3.6: Customer Communication Placeholders
*   **Task Description:** Implement basic command handlers for "Reply to order", "Send status update", "Broadcast promotion" that send placeholder confirmation messages. Actual logic to come later or via different mechanisms.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects commands like `"/reply_order [customer_number] [message_text]"`, `"/send_status [order_id] [status_text]"`, `"/broadcast_promo [promo_message_text]"`.
    2.  For each command, a log is generated in `message_logs` indicating the command was received and a placeholder action was acknowledged.
    3.  The system sends a WhatsApp message back to the user confirming receipt of command, e.g., "Placeholder: Order reply to [customer_number] would be sent with message: [message_text]".
    4.  No actual external messages are sent beyond the confirmation to the originating user.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.2 (Customer Communication - initial stubs).

---

## Phase 4: Logistics, Info Access & Learning Tools Implementation
**Phase AI-Verifiable End Goal:** All micro-tasks in Phase 4 are complete. Users can query for mock parcel locations, get placeholder directions, and access basic, static learning content (tips/guides) in their selected language. All interactions are logged.
**Relevant PRD Sections/Requirements:** PRD Sections 4.3, 5.3, 5.4.

### Micro-task 4.1: Mock Parcel Location Tracking
*   **Task Description:** Implement command to "track parcel [tracking_id]" which returns a mock/static status.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects command `"/track_parcel [tracking_id]"`.
    2.  A Python function `get_mock_parcel_status(tracking_id)` returns a predefined string like "Parcel [tracking_id] is out for delivery."
    3.  The mock status is sent as a WhatsApp reply to the user.
    4.  Interaction logged in `message_logs`.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.3 (Parcel Location Tracking).

### Micro-task 4.2: Placeholder Map Directions
*   **Task Description:** Implement command "Directions to [location_name]" which returns a placeholder or very basic static text.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects command `"/directions [location_name]"`.
    2.  A Python function `get_placeholder_directions(location_name)` returns a string like "Placeholder: Directions to [location_name] would be provided here in a data-light format."
    3.  The placeholder direction text is sent as a WhatsApp reply.
    4.  Interaction logged in `message_logs`.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.3 (Map Directions).

### Micro-task 4.3: Placeholder Pickup Reminders
*   **Task Description:** Implement command `"/remind_pickup [item] at [time]"` which logs reminder and confirms (no actual scheduler yet).
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  `core_handler.py` detects command `"/remind_pickup [item] at [time]"`.
    2.  A record is inserted into a new Supabase table `reminders` (`reminder_id` PK, `user_whatsapp_id` FK, `item_description` TEXT, `reminder_time_text` TEXT, `created_at` TIMESTAMPTZ, `status` TEXT DEFAULT 'pending'). Verified by `SELECT COUNT(*) FROM reminders WHERE user_whatsapp_id = 'test_user'` incrementing.
    3.  A confirmation message "Placeholder: Reminder set for [item] at [time]." is sent.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.3 (Pickup Reminders).

### Micro-task 4.4: Basic Q&A from Static Content Files
*   **Task Description:** Implement a simple Q&A by matching keywords in user queries to static text files for answers.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A directory `content/qa/` exists.
    2.  Inside `content/qa/`, files like `register_business_en.txt`, `register_business_xh.txt`, `register_business_af.txt` exist containing relevant answers.
    3.  `core_handler.py` has a function `get_static_answer(query_text, language_code)`:
        *   It attempts to match keywords from `query_text` (e.g., "register business", "how to small business") to filenames or metadata associated with the content files.
        *   If a match is found, it reads and returns the content of the corresponding language file (e.g., `register_business_[language_code].txt`).
        *   If no match, returns a "Sorry, I don't have an answer for that yet." message from `content/qa_no_answer_[language_code].txt`.
    4.  Sending "How to register my small business?" (when user language is 'en') results in the content of `register_business_en.txt` being sent back.
    5.  Sending "random gibberish query" results in the "Sorry..." message being sent.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.3 (Q&A Capability), 4.3.

### Micro-task 4.5: Static Learning Content (Business Tips & Compliance Guides)
*   **Task Description:** Implement commands to access static business tips and compliance guides.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  Directory structure `content/tips/[lang]/tip1.txt`, `content/guides/[lang]/compliance_guide1.txt` exists, populated with sample content.
    2.  `core_handler.py` detects commands like `"/get_tip"` and `"/get_compliance_guide"`.
    3.  `"/get_tip"` command logic reads a random .txt file from `content/tips/[user_preferred_language]/` and sends its content.
    4.  `"/get_compliance_guide"` command logic reads `content/guides/[user_preferred_language]/compliance_guide1.txt` (or a specific one if multiple) and sends its content.
    5.  A message "No more tips available." or "Guide not found." (from `content/..._not_found_[lang].txt`) is sent if content is missing for the language.
    6.  Automated tests trigger these commands for each supported language; responses match the content of the respective .txt files.
*   **Relevant PRD Sections/Requirements:** PRD Section 5.4 (Learning & Upskilling).

---

## Phase 5: NFRs, Testing & Pilot Preparation
**Phase AI-Verifiable End Goal:** All micro-tasks in Phase 5 are complete. Key NFRs (data efficiency, low-RAM fallback thought process, core security logging) are addressed/verified. Unit test coverage for Python core logic reaches a defined threshold. End-to-end test scenarios (PRD 4.4) are automated and pass. A basic admin dashboard stub exists in Replit web portal for monitoring message counts. Pilot user onboarding documentation for ambassadors is drafted.
**Relevant PRD Sections/Requirements:** PRD Sections 8 (NFRs), 4.4 (Example Scenario for testing), 9 (KPIs - message counts), 10.1 (Pilot Roadmap Prep).

### Micro-task 5.1: Data Efficiency Testing & Optimization Hooks
*   **Task Description:** Implement a test script to measure data usage per interaction for common commands. Add logging for message sizes.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  The `message_logs` table in Supabase has its `data_size_kb` field populated by `core_handler.py` for every inbound and outbound message (calculated based on text length + estimated WhatsApp overhead, or from gateway if available).
    2.  A Python script `test_data_efficiency.py` exists which:
        *   Sends a sequence of 10 representative commands (e.g., `/lang`, payment link request, log sale, get tip) via direct call to handler functions or through the test WhatsApp setup.
        *   Queries `message_logs` for these interactions.
        *   Calculates and logs the average `data_size_kb` for the platform's part of these interactions.
    3.  The output of `test_data_efficiency.py` shows the average `data_size_kb` is less than or equal to 5KB.
*   **Relevant PRD Sections/Requirements:** PRD Section 8.1 (Data Efficiency).

### Micro-task 5.2: Low-RAM Device Fallback Strategy Definition
*   **Task Description:** Document strategies for graceful fallbacks on low-RAM devices (e.g., avoiding large image/media sends by default, simplifying complex messages).
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A markdown file `low_ram_strategy.md` is created in the repository.
    2.  This document lists at least 3 specific, actionable strategies derived from PRD (e.g., "Default to text-only responses, QR codes sent as links first with option for image," "Keep message choices short (e.g., 3 options max)," "Break down long guides into smaller, individually requestable chunks.").
    3.  Code in `core_handler.py` where messages are constructed includes commented-out placeholders or conditional logic stubs (e.g., `if not user_prefers_low_data_mode: send_image_else_send_link()`) for at least one of these strategies. (Full implementation of these modes is future).
*   **Relevant PRD Sections/Requirements:** PRD Section 8.4 (Device Compatibility).

### Micro-task 5.3: Basic Security Logging & RLS Verification
*   **Task Description:** Implement basic security event logging (e.g., failed commands, data deletion requests) and verify RLS on critical tables.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A new Supabase table `security_logs` (`event_id` SERIAL PK, `user_whatsapp_id` TEXT, `event_type` TEXT, `details` JSONB, `timestamp` TIMESTAMPTZ) is created.
    2.  `core_handler.py` logs events to `security_logs` for:
        *   Data deletion request (`/delete` command) - `event_type: 'DATA_DELETE_REQUESTED'`.
        *   Data deletion confirmation (`/delete confirm`) - `event_type: 'DATA_DELETE_CONFIRMED'`.
        *   Attempt to access a non-existent/unauthorized feature based on bundle - `event_type: 'AUTHZ_FAILURE'`.
    3.  A test script `verify_rls.py` attempts to:
        *   As `user_A`, insert data into `sales_logs`. Verified by checking Supabase.
        *   As `user_B` (simulated by changing context or using a different Supabase client with user B's simulated JWT/key), attempt to read `user_A`'s sales logs. The script confirms this read attempt fails (e.g., returns 0 rows or throws a permission error logged by the Supabase client).
        *   Test script log confirms RLS policies are behaving as expected for `users`, `sales_logs`, `expense_logs`, `payment_transactions`.
*   **Relevant PRD Sections/Requirements:** PRD Section 8.5 (Security).

### Micro-task 5.4: Unit Test Suite Enhancement & Coverage Report
*   **Task Description:** Write unit tests for all key Python functions in `core_handler.py`, `language_utils.py`, etc. Aim for >70% coverage.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  Unit tests exist in the `tests/` directory for all implemented Python functions handling commands, user management, language processing, and Supabase interactions.
    2.  Executing `pytest --cov=.` (or similar command with chosen test runner and coverage tool) in the Python core logic directory.
    3.  The command completes without any test failures.
    4.  The generated coverage report (e.g., HTML or text output) shows a line coverage percentage of >= 70%.
*   **Relevant PRD Sections/Requirements:** General software quality, implicitly needed for reliable features from PRD Section 5.

### Micro-task 5.5: Automated End-to-End Test for PRD Scenario 4.4
*   **Task Description:** Create an automated test script that simulates the PRD's "New User Onboarding & Language Choice" scenario.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A Python script `e2e_test_onboarding_scenario.py` exists.
    2.  This script simulates a new WhatsApp user sending "Molo" by directly calling the `core_handler.handle_incoming_message` (or posting to the n8n webhook after clearing test user from DB).
    3.  The script then verifies:
        *   A new user record for the test `sender_id` is created in Supabase `users` table with `preferred_language` set to "xh".
        *   The log of messages prepared by `core_handler.py` (or captured from an n8n mock node) includes:
            *   The POPIA notice content (matching `popia_notice_xh.txt` or a master key).
            *   A welcome message in Xhosa (from `content/welcome_xh.txt`).
            *   A prompt to select a bundle, in Xhosa.
    4.  The script simulates the user selecting the "Street-Vendor CRM" bundle.
    5.  It verifies the `current_bundle` for the user in Supabase is updated to 'street_vendor_crm'.
    6.  The script logs "E2E Test Scenario 4.4 PASSED" if all checks are met, otherwise "FAILED" with details. Test script execution output shows "PASSED".
*   **Relevant PRD Sections/Requirements:** PRD Section 4.4.

### Micro-task 5.6: Basic Admin Dashboard Stub on Replit Web Portal
*   **Task Description:** Create a very simple web page on the Replit Reserved-VM's web portal capability to display total message count from `message_logs`.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A simple Python web framework (e.g., Flask, FastAPI) is added to `core_handler.py` or a separate `admin_portal.py`.
    2.  An HTTP endpoint `/admin/dashboard` is created.
    3.  When accessed via a web browser (or `curl`), this endpoint queries Supabase: `SELECT COUNT(*) FROM message_logs`.
    4.  It returns an HTML page (or JSON response) displaying: "Total Messages Processed: [Count]".
    5.  Accessing the Replit web portal URL followed by `/admin/dashboard` successfully displays this count.
*   **Relevant PRD Sections/Requirements:** PRD Section 9 (KPIs - message counts, for monitoring).

### Micro-task 5.7: Draft Pilot User Onboarding Documentation for Ambassadors
*   **Task Description:** Create an initial draft document for township ambassadors on how to onboard new users.
*   **AI-Verifiable Deliverable/Completion Criteria:**
    1.  A markdown file `pilot_ambassador_onboarding_guide_v0.1.md` exists in a `docs/` directory.
    2.  The document contains sections covering at least:
        *   Explaining Township Connect's purpose (from PRD 1.3).
        *   How to explain QR code scanning (referencing MT2.6).
        *   Expected first interaction flow (user sends "Hi/Molo/Hallo", language detection, POPIA notice, bundle selection).
        *   How to explain a key feature like "Payment Link Generation".
        *   How to explain language switching and data deletion.
    3.  The document is written in simple English, suitable for translation.
*   **Relevant PRD Sections/Requirements:** PRD Section 10.1 (Pilot Roadmap - ambassador recruitment needs guidance).

---

## Final Validation Approach (Post All Phases):
Successful execution of the `e2e_test_onboarding_scenario.py` (MT5.5) and additional E2E test scripts covering one core flow from each of the Business/Finance, Logistics/Info, and Learning features (e.g., generating a payment link, asking a Q&A, getting a tip). All these E2E tests must pass, confirming the system processes the request, interacts with Supabase correctly, and prepares the correct WhatsApp reply content. The system meets the NFR for data efficiency as per `test_data_efficiency.py` (MT5.1). All critical POPIA compliance mechanisms (notice, consent log, data deletion) are confirmed to be functional through their respective AI-verifiable micro-task completions. Message count KPI on the admin dashboard stub (MT5.6) correctly reflects interactions generated during E2E testing.
