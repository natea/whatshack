# Township Connect: System Architecture
**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Architect

## 1. Introduction

### 1.1 Purpose
This document outlines the high-level system architecture for "Township Connect," a WhatsApp-native assistant designed to empower Cape Town township residents. The architecture aims to provide a robust, scalable, and maintainable foundation for delivering accessible, data-light tools for business, services, and skills development.

### 1.2 Scope
This architecture covers all major components of the Township Connect system, including user interaction via WhatsApp, backend processing, data storage, external service integrations, and core functionalities as defined in the Product Requirements Document ([`docs/prd.md`](docs/prd.md)), Master Project Plan ([`docs/project_plan.md`](docs/project_plan.md)), and Master Acceptance Test Plan ([`tests/acceptance/master_acceptance_test_plan.md`](tests/acceptance/master_acceptance_test_plan.md)).

### 1.3 Guiding Principles
The architecture is designed with the following principles in mind:
*   **User-Centricity:** Prioritizing ease of use and accessibility for township residents via WhatsApp.
*   **Data-Light:** Ensuring all interactions adhere to the ≤5 KB data limit.
*   **Multilingual:** Native support for English, isiXhosa, and Afrikaans.
*   **POPIA Compliance:** Adherence to data privacy and protection regulations.
*   **Scalability:** Ability to handle a growing user base and transaction volume.
*   **Modularity:** Components designed for independent development, deployment, and scaling.
*   **Cost-Effectiveness:** Leveraging managed services and efficient design to meet cost targets.
*   **Maintainability:** Clear separation of concerns and well-defined interfaces.
*   **AI Verifiability:** Architecture designed to support the AI-verifiable tasks outlined in the Master Project Plan.

## 2. Architectural Goals
The system architecture is designed to achieve the following key goals, derived from project requirements:
*   **Reliable WhatsApp Communication:** Seamless and stable message exchange with users.
*   **Efficient Core Logic Processing:** Fast and accurate handling of user requests and business logic in Python.
*   **Robust Orchestration:** Effective management of complex workflows and integrations by n8n.
*   **Secure and Compliant Data Management:** Ensuring data integrity, privacy (POPIA), and residency using Supabase.
*   **Asynchronous Task Handling:** Utilizing Redis Streams for decoupling and background processing.
*   **Seamless External Service Integration:** Abstracting and managing connections to services like payment gateways via Composio.
*   **Data Efficiency:** Minimizing data payload for all user interactions (≤5 KB).
*   **Multilingual Support:** Delivering all content and interactions in the user's preferred language.
*   **Support for Pilot Program Objectives:** Enabling features critical for onboarding SMEs and corporate PoC.

## 3. High-Level System Diagram

```mermaid
graph TD
    User[User via WhatsApp] -->|Messages| WG[WhatsApp Gateway (e.g., Twilio)]
    WG -->|Webhook: Inbound Message| N8N[Orchestration Layer (n8n)]
    N8N -->|HTTP Request/Execute Command| PL[Python Core Logic Service (Replit VM)]
    PL -->|Publish| MQ[Message Queue (Upstash Redis Streams)]
    PL -->|CRUD Operations| DB[Data Persistence (Supabase PostgreSQL)]
    PL -->|Read| CF[Content Files (Static Text)]
    N8N -->|API Calls| ES[External Services (Composio for Payments, etc.)]
    N8N -->|Webhook: Send Reply| WG
    Admin[Admin User] -->|HTTP| AdminPortal[Admin Portal (on Replit VM, part of PL)]
    AdminPortal -->|Read| DB

    subgraph "Replit Reserved VM"
        direction LR
        PL
        AdminPortal
        %% Potentially n8n self-hosted, or n8n Cloud calls Python on Replit
    end

    style User fill:#lightgrey,stroke:#333,stroke-width:2px
    style WG fill:#lightblue,stroke:#333,stroke-width:2px
    style N8N fill:#lightgreen,stroke:#333,stroke-width:2px
    style PL fill:#orange,stroke:#333,stroke-width:2px
    style MQ fill:#pink,stroke:#333,stroke-width:2px
    style DB fill:#purple,stroke:#fff,stroke-width:2px,color:#fff
    style CF fill:#yellow,stroke:#333,stroke-width:2px
    style ES fill:#cyan,stroke:#333,stroke-width:2px
    style AdminPortal fill:#orange,stroke:#333,stroke-width:2px
```

**Diagram Legend:**
*   **User via WhatsApp:** End-user interacting with the system.
*   **WhatsApp Gateway (e.g., Twilio):** Interface for sending/receiving WhatsApp messages.
*   **Orchestration Layer (n8n):** Manages workflows, routes messages, integrates services.
*   **Python Core Logic Service (Replit VM):** Main application logic, command processing, business rules.
*   **Message Queue (Upstash Redis Streams):** For asynchronous tasks and decoupling.
*   **Data Persistence (Supabase PostgreSQL):** Database for all persistent application data.
*   **Content Files (Static Text):** Stores multilingual static content (prompts, notices, Q&A).
*   **External Services (Composio):** Integration point for third-party APIs.
*   **Admin Portal:** Simple web interface for basic monitoring.

## 4. Component Breakdown

### 4.1 WhatsApp Gateway (e.g., Twilio)
*   **Description:** The primary interface for receiving messages from and sending messages to users on WhatsApp. Managed service preferred for reliability and ease of setup (e.g., Twilio).
*   **Responsibilities:**
    *   Authenticating with the WhatsApp platform.
    *   Receiving inbound messages and forwarding them to the n8n layer via webhooks.
    *   Accepting outbound message requests from the n8n layer and dispatching them to users.
*   **Key Interactions:** User, n8n Orchestration Layer.
*   **MPP/HLT Support:** Critical for all user interactions (MPP MT1.3, HLT-TC-027).

### 4.2 Orchestration Layer (n8n)
*   **Description:** A workflow automation tool that acts as the central orchestrator for message routing and service integration. Can be n8n Cloud or self-hosted on Replit (if feasible).
*   **Responsibilities:**
    *   Receiving inbound messages from the WhatsApp Gateway via webhook.
    *   Calling the Python Core Logic Service for message processing and business logic execution.
    *   Orchestrating complex workflows involving multiple steps or external services (e.g., payment link generation via Composio).
    *   Handling error conditions and retries for external calls.
    *   Formatting replies and passing them to the WhatsApp Gateway for delivery.
*   **Key Interactions:** WhatsApp Gateway, Python Core Logic Service, External Services (Composio).
*   **MPP/HLT Support:** MPP MT1.3, MT1.4, MT3.1; HLT-TC-029, HLT-TC-031.

### 4.3 Python Core Logic Service
*   **Description:** The main application backend, developed in Python and hosted on a Replit Reserved-VM. This aligns with the Master Project Plan's focus on Python for core tasks and existing `src/*.py` files.
*   **Responsibilities:**
    *   Receiving deserialized message data from n8n (e.g., via an HTTP endpoint).
    *   User identification, authentication (implicit via WhatsApp ID), and session management.
    *   Parsing user commands and natural language input (basic).
    *   Implementing all business logic for features:
        *   Account Management (onboarding, language, POPIA, bundles - MPP Phase 2).
        *   Business & Finance Tools (payments, sales, expenses - MPP Phase 3).
        *   Logistics & Info Access (tracking, directions, Q&A - MPP Phase 4).
        *   Learning Tools (tips, guides - MPP Phase 4).
    *   Interacting with Supabase for all data persistence needs.
    *   Publishing messages/tasks to Upstash Redis Streams for asynchronous processing.
    *   Reading static multilingual content from Content Files.
    *   Constructing responses and returning them to n8n.
    *   Logging interactions and security events.
    *   Enforcing data-light principles in response construction.
*   **Key Interactions:** n8n Orchestration Layer, Data Persistence (Supabase), Message Queue (Redis), Content Files.
*   **MPP/HLT Support:** Core to almost all MPP tasks (e.g., MT1.4, Phase 2, 3, 4, 5) and HLTs.

### 4.4 Message Queue (Upstash Redis Streams)
*   **Description:** A managed Redis service used for message queuing to decouple components and enable asynchronous processing.
*   **Responsibilities:**
    *   Receiving messages/tasks published by the Python Core Logic Service (e.g., `incoming_whatsapp_messages` stream).
    *   Holding messages until they are consumed by worker processes (future scalability for background tasks).
*   **Key Interactions:** Python Core Logic Service.
*   **MPP/HLT Support:** MPP MT1.5; HLT-TC-030.

### 4.5 Data Persistence Layer (Supabase - PostgreSQL)
*   **Description:** A managed PostgreSQL database service with BaaS features, hosted in `af-south-1` for data residency.
*   **Responsibilities:**
    *   Storing all application data: user profiles, message logs, service bundles, business transactions, reminders, security logs.
    *   Enforcing data integrity through schemas and constraints.
    *   Providing Row-Level Security (RLS) for user data segregation (POPIA compliance).
    *   Executing SQL functions for complex operations (e.g., `hard_delete_user_data`).
*   **Key Interactions:** Python Core Logic Service, Admin Portal.
*   **MPP/HLT Support:** MPP MT1.2, MT3.2, MT5.3; HLT-TC-021, HLT-TC-022, HLT-TC-028.

### 4.6 External Services Integration Layer (Composio)
*   **Description:** A service integration platform used to connect to third-party SaaS tools (e.g., payment gateways like SnapScan, MoMo) without managing individual OAuth flows.
*   **Responsibilities:**
    *   Providing a unified interface for n8n (or Python Core Logic) to interact with external services.
    *   Handling authentication and API calls to connected services.
*   **Key Interactions:** n8n Orchestration Layer.
*   **MPP/HLT Support:** MPP MT3.1; HLT-TC-031.

### 4.7 Content Management (File-based)
*   **Description:** A directory structure within the project repository (`content/`) storing static text files for multilingual content.
*   **Responsibilities:**
    *   Holding predefined text for POPIA notices, welcome messages, command prompts, Q&A answers, business tips, compliance guides, etc.
    *   Organized by language (e.g., `content/en/`, `content/xh/`, `content/af/`).
*   **Key Interactions:** Python Core Logic Service (reads content).
*   **MPP/HLT Support:** MPP MT2.2, MT2.4, MT4.4, MT4.5.

### 4.8 Admin Portal
*   **Description:** A simple web interface, potentially built with Flask/FastAPI as part of the Python Core Logic service on Replit.
*   **Responsibilities:**
    *   Providing basic monitoring capabilities (e.g., displaying total message count from `message_logs`).
    *   (Future) Basic administrative functions.
*   **Key Interactions:** Admin User (via browser), Data Persistence (Supabase).
*   **MPP/HLT Support:** MPP MT5.6.

## 5. Data Model Overview
The primary data will be stored in Supabase (PostgreSQL). Key tables include:

*   **`users`**: Stores user-specific information.
    *   `whatsapp_id` (TEXT, PK): User's WhatsApp identifier.
    *   `preferred_language` (TEXT): User's chosen language (en, xh, af).
    *   `current_bundle` (TEXT, FK to `service_bundles`): Currently selected service bundle.
    *   `popia_consent_given` (BOOLEAN): Status of POPIA consent.
    *   `created_at`, `last_active_at` (TIMESTAMPTZ).
    *   Other user-specific flags or settings.
*   **`message_logs`**: Logs all inbound and outbound messages.
    *   `log_id` (SERIAL, PK).
    *   `user_whatsapp_id` (TEXT, FK to `users`).
    *   `direction` (TEXT: 'inbound'/'outbound').
    *   `message_content` (TEXT).
    *   `timestamp` (TIMESTAMPTZ).
    *   `data_size_kb` (FLOAT): Calculated size of the message payload.
*   **`service_bundles`**: Defines available service bundles.
    *   `bundle_id` (TEXT, PK).
    *   `bundle_name_en`, `bundle_name_xh`, `bundle_name_af` (TEXT).
    *   `description_en`, `description_xh`, `description_af` (TEXT).
*   **`payment_transactions`**: Logs payment link generation attempts and status.
    *   `transaction_id` (SERIAL, PK).
    *   `user_whatsapp_id` (TEXT, FK).
    *   `provider` (TEXT: 'SnapScan', 'MoMo').
    *   `amount` (DECIMAL).
    *   `link_generated` (TEXT).
    *   `status` (TEXT: 'pending', 'paid', 'failed').
*   **`sales_logs`**: Records sales logged by users.
    *   `sale_id` (SERIAL, PK).
    *   `user_whatsapp_id` (TEXT, FK).
    *   `description` (TEXT).
    *   `amount` (DECIMAL).
    *   `sale_date` (TIMESTAMPTZ).
*   **`expense_logs`**: Records expenses logged by users.
    *   `expense_id` (SERIAL, PK).
    *   `user_whatsapp_id` (TEXT, FK).
    *   `description` (TEXT).
    *   `amount` (DECIMAL).
    *   `expense_date` (TIMESTAMPTZ).
*   **`security_logs`**: Logs security-relevant events.
    *   `event_id` (SERIAL, PK).
    *   `user_whatsapp_id` (TEXT, nullable).
    *   `event_type` (TEXT).
    *   `details` (JSONB).
    *   `timestamp` (TIMESTAMPTZ).
*   **`reminders`**: Stores user-created reminders.
    *   `reminder_id` (SERIAL, PK).
    *   `user_whatsapp_id` (TEXT, FK).
    *   `item_description` (TEXT).
    *   `reminder_time_text` (TEXT).
    *   `status` (TEXT: 'pending', 'sent', 'cancelled').

(These align with MPP MT1.2, MT3.2, MT4.3, MT5.1, MT5.3)

## 6. Interaction Flows (Examples)

### 6.1 New User Onboarding (e.g., "Molo")
1.  **User** sends "Molo" via WhatsApp.
2.  **WhatsApp Gateway (Twilio)** receives and sends to **n8n** webhook.
3.  **n8n** workflow calls **Python Core Logic** (`handle_incoming_message` endpoint).
4.  **Python Core Logic**:
    a.  Identifies new user by querying `users` table in **Supabase**.
    b.  Creates new user record in `users` table.
    c.  Calls `language_utils.detect_initial_language("Molo")` -> "xh".
    d.  Updates `preferred_language` to "xh" in **Supabase**.
    e.  Retrieves POPIA notice (`popia_notice_xh.txt`), welcome message (`welcome_xh.txt`), bundle prompt (`bundle_select_prompt_xh.txt`) from **Content Files**.
    f.  Queries `service_bundles` from **Supabase** for bundle list.
    g.  Logs inbound/outbound messages to `message_logs` in **Supabase** (with `data_size_kb`).
    h.  Publishes message data to **Redis Stream** `incoming_whatsapp_messages`.
    i.  Returns structured multi-message reply (POPIA, Welcome, Bundle Prompt in isiXhosa) to **n8n**.
5.  **n8n** uses Twilio node to send messages via **WhatsApp Gateway** to User.
*Supports HLT-TC-001, MPP Phase 2 tasks.*

### 6.2 Generate Payment Link (e.g., "SnapScan 75")
1.  **User** (existing, consented, bundle selected) sends "SnapScan 75".
2.  **WhatsApp Gateway (Twilio)** -> **n8n** -> **Python Core Logic**.
3.  **Python Core Logic**:
    a.  Identifies user, retrieves `user_whatsapp_id` and `preferred_language` from **Supabase**.
    b.  Parses command: provider="SnapScan", amount=75.
    c.  Prepares payload for n8n payment workflow.
    d.  (Option 1: Python calls n8n payment workflow) Makes HTTP request to a dedicated n8n webhook for `Generate_Payment_Link_n8n`.
    e.  (Option 2: n8n calls Python, Python responds, n8n calls Composio) Returns data to main n8n workflow, which then calls Composio. Option 1 is cleaner if Python needs to await the link. Let's assume Python triggers a specific n8n workflow for payment.
    f.  Logs inbound message to `message_logs` in **Supabase**.
    g.  Publishes to **Redis Stream**.
    h.  Returns instruction to n8n to trigger payment workflow.
4.  **n8n** (main workflow) triggers `Generate_Payment_Link_n8n` workflow.
5.  **n8n** (`Generate_Payment_Link_n8n` workflow):
    a.  Receives `amount`, `provider`, `user_id`.
    b.  Calls **Composio** "Generate SnapScan Link" action.
    c.  **Composio** interacts with SnapScan API.
    d.  **Composio** returns payment link to **n8n**.
    e.  **n8n** workflow returns payment link to the **Python Core Logic** (if Python awaits) or directly prepares reply. For simplicity, assume n8n gets link and calls Python again or Python polls/n8n calls back Python with result.
    *Alternative: Python makes a direct call to a payment link generation endpoint on n8n, and n8n returns the link synchronously if possible, or via a callback mechanism.*
    Let's refine: Python calls n8n which calls Composio and returns link to Python.
6.  **Python Core Logic** (receives link from n8n):
    a.  Inserts record into `payment_transactions` in **Supabase**.
    b.  Formats reply message with the payment link.
    c.  Logs outbound message to `message_logs` in **Supabase**.
    d.  Returns reply to main **n8n** workflow.
7.  **n8n** (main workflow) sends reply via **WhatsApp Gateway** to User.
*Supports HLT-TC-005, MPP MT3.1, MT3.3.*

## 7. Technology Stack Summary
*   **WhatsApp Gateway:** Twilio API (managed via n8n).
*   **Orchestration:** n8n (Cloud or Self-Hosted on Replit).
*   **Core Logic:** Python (Flask/FastAPI for HTTP interface) on Replit Reserved-VM.
*   **Database:** Supabase (PostgreSQL) - `af-south-1` region.
*   **Message Queue:** Upstash Redis Streams.
*   **External Service Integration:** Composio.
*   **Content:** Static files in Git repository.
*   **Hosting:** Replit Reserved-VM (for Python app, n8n if self-hosted, Admin Portal).

## 8. Alignment with Master Project Plan
This architecture directly supports the AI-verifiable tasks in the [`docs/project_plan.md`](docs/project_plan.md):
*   **Phase 1 (Foundation):** All components (Replit, Supabase, n8n+Twilio, Python core, Redis) are defined.
*   **Phase 2 (User Mgmt & POPIA):** Python core logic interacting with Supabase and Content Files handles user lifecycle, language, and POPIA.
*   **Phase 3 (Business Tools):** Python core logic, n8n, Composio, and Supabase enable payment, sales, and expense features.
*   **Phase 4 (Info & Learning):** Python core logic and Content Files provide Q&A and static learning materials.
*   **Phase 5 (NFRs & Pilot Prep):**
    *   Data efficiency is a design principle for Python core logic.
    *   Low-RAM strategy is a consideration for message construction.
    *   Security logging and RLS are handled by Python core and Supabase.
    *   Admin dashboard is a small web component within the Python service.

## 9. Alignment with High-Level Acceptance Tests
The architecture is designed to pass the tests in [`tests/acceptance/master_acceptance_test_plan.md`](tests/acceptance/master_acceptance_test_plan.md):
*   **User Onboarding (HLT-TC-001-004):** Covered by Gateway -> n8n -> Python -> Supabase/Content flow.
*   **Business Functionality (HLT-TC-005-009):** Involves Python, n8n, Composio, Supabase.
*   **Community Services (HLT-TC-010-013):** Python, Content Files, Supabase. Data-light directions (HLT-TC-010) are a key output of Python logic.
*   **Multilingual (HLT-TC-014-018):** Python (`language_utils.py`), Supabase (lang pref), Content Files.
*   **POPIA (HLT-TC-019-022):** Python, Supabase (logging, RLS, SQL functions for deletion).
*   **Performance & Data Efficiency (HLT-TC-023-026):** Data payload (HLT-TC-023) is a core constraint. Response times (HLT-TC-024) depend on component efficiency.
*   **API Robustness (HLT-TC-027-031):** Each component (Gateway, Supabase, n8n, Redis, Composio) has HLTs.
*   **Reliability & Error Handling (HLT-TC-032-034):** Handled by Python and n8n.
*   **Pilot Objectives (HLT-TC-035-036):** System-wide goals supported by the integrated architecture.

## 10. Security Considerations
*   **Data Segregation:** Supabase Row-Level Security (RLS) is critical to ensure users can only access their own data.
*   **POPIA Compliance:**
    *   Explicit user consent for data processing.
    *   Secure storage of consent logs.
    *   Data residency in `af-south-1`.
    *   Self-service data erasure (`/delete` command triggering `hard_delete_user_data` SQL function).
    *   Purpose limitation in data usage.
*   **Secrets Management:** API keys, database credentials, and other secrets stored securely in Replit environment variables/secrets.
*   **Input Validation:** The Python Core Logic Service must validate all inputs received from n8n (originating from users) to prevent injection attacks or unexpected behavior.
*   **Dependency Security:** Regularly update dependencies for Python, n8n nodes, and other tools.
*   **Secure Communication:** HTTPS for all external communication (Replit to n8n, n8n to Composio, Python to Supabase/Redis uses TLS).
*   **Rate Limiting:** Consider rate limiting at the n8n webhook or Python API endpoint level to prevent abuse.
*   **Audit Trails:** `message_logs` and `security_logs` provide basic audit capabilities.

## 11. Scalability and Performance Considerations
*   **Stateless Python Core Logic:** The Python application should be designed to be as stateless as possible, relying on Supabase and Redis for state, allowing for horizontal scaling of Python workers if Replit supports it or if migrated.
*   **Asynchronous Processing:** Redis Streams allow for deferring non-critical tasks or handling spikes in load by queuing messages for background workers (future enhancement beyond initial MPP focus on publishing).
*   **Database Performance:** Supabase (PostgreSQL) is scalable. Efficient queries and proper indexing in Supabase are crucial.
*   **n8n Performance:** n8n Cloud offers scalability. If self-hosted, resource allocation on Replit needs monitoring.
*   **Data-Light Interactions:** This is a primary performance goal. Message construction in Python must be optimized for size (≤5KB).
*   **Caching:** Redis can be used for caching frequently accessed, non-sensitive data (e.g., service bundle lists, popular Q&A) to reduce Supabase load and improve response times.
*   **Connection Pooling:** Ensure database and Redis clients in Python use connection pooling.

## 12. Deployment View
*   **User Interface:** WhatsApp application on user devices.
*   **WhatsApp Gateway:** Twilio (Cloud Service).
*   **Orchestration:** n8n (Cloud Service, or self-hosted on Replit VM).
*   **Core Application Logic:** Python application (Flask/FastAPI) running on Replit Reserved-VM.
*   **Database:** Supabase Cloud (PostgreSQL) in `af-south-1`.
*   **Message Queue:** Upstash Redis Cloud.
*   **External Service Connector:** Composio Cloud.
*   **Static Content:** Served from the file system of the Replit VM, deployed via Git.

## 13. Identified Scaffolding Needs (Foundational Step)
To implement this architecture, the following initial scaffolding is required:

1.  **Repository Setup:**
    *   Standard project structure: `src/`, `n8n_workflows/`, `db_scripts/`, `content/`, `tests/`, `docs/`.
    *   `requirements.txt` for Python.
    *   Replit configuration (`.replit`, `replit.nix`).
2.  **Python Core Logic Service (Replit):**
    *   Basic Flask/FastAPI application with an HTTP endpoint for n8n.
    *   Initial `core_handler.py` with `handle_incoming_message` stub.
    *   Supabase client (`supabase-py`) setup and configuration.
    *   Redis client (`redis-py`) setup and configuration.
    *   Directory structure for `language_utils.py`, etc.
3.  **n8n Workflows:**
    *   `Incoming_WhatsApp_Webhook_Twilio`: Receives Twilio webhook, calls Python endpoint, receives Python response, sends reply via Twilio node.
    *   (Placeholder) `Generate_Payment_Link_n8n`: Triggerable by Python, calls Composio.
4.  **Supabase (Database):**
    *   Project created in `af-south-1`.
    *   `db_scripts/db_schema_v1.sql` with initial tables (`users`, `message_logs`, `service_bundles`).
    *   `db_scripts/functions/hard_delete_user_data.sql` placeholder.
    *   RLS enabled on key tables.
    *   Secrets (URL, anon key, service role key) configured in Replit.
5.  **Upstash Redis (Message Queue):**
    *   Instance created.
    *   Connection details (host, port, password) configured in Replit secrets.
6.  **Content Files:**
    *   Directory structure: `content/en/`, `content/xh/`, `content/af/`.
    *   Initial placeholder files (e.g., `popia_notice_en.txt`, `welcome_en.txt`).
7.  **Twilio Setup:**
    *   WhatsApp-enabled number.
    *   Webhook configured to point to the n8n `Incoming_WhatsApp_Webhook_Twilio` URL.
    *   Credentials configured in n8n.
8.  **Composio Setup (Basic):**
    *   Account created.
    *   (Placeholder) SnapScan/MoMo connectors explored.
9.  **Basic CI/CD (Replit/GitHub):**
    *   Linting (e.g., Flake8) for Python code.
    *   Placeholder for running `pytest`.

This foundational setup will enable iterative development of features as outlined in the Master Project Plan.