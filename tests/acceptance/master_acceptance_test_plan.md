# Master Acceptance Test Plan: Township Connect

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Gemini)

## 1. Introduction

### 1.1 Purpose
This Master Acceptance Test Plan (MATP) outlines the strategy, scope, phases, and criteria for High-Level End-to-End Acceptance Testing (HLT) of the "Township Connect" project. The primary purpose of this MATP is to define the ultimate success criteria for the project, ensuring that the delivered system meets all user requirements, business objectives, and quality standards from an end-user perspective. All tests defined herein are designed with AI verifiable completion criteria.

### 1.2 Scope
This MATP covers the complete end-to-end functionality of the Township Connect WhatsApp-native assistant, as defined in the project's guiding documents. This includes:
*   User onboarding and account management.
*   Core business functionalities for Small and Medium Enterprises (SMEs).
*   Community service and information access features.
*   Multilingual support (English, isiXhosa, Afrikaans).
*   POPIA compliance.
*   Performance and data efficiency (≤5 KB/interaction).
*   Reliability and error handling.
*   API integrations supporting the above features.
*   Validation of pilot program objectives.

### 1.3 Reference Documents
*   Product Requirements Document (PRD): [`docs/prd.md`](docs/prd.md)
*   Township Connect Strategic Research Report - Executive Summary: [`research/township_connect_strategic_research/final_report/02_executive_summary.md`](research/township_connect_strategic_research/final_report/02_executive_summary.md)
*   Township Connect Strategic Research Report - Recommendations: [`research/township_connect_strategic_research/final_report/06_recommendations.md`](research/township_connect_strategic_research/final_report/06_recommendations.md)
*   High-Level Acceptance Test Strategy Report: [`research/high_level_test_strategy_report.md`](research/high_level_test_strategy_report.md)

## 2. Overall Test Strategy
The overall test strategy is directly derived from the High-Level Acceptance Test Strategy Report ([`research/high_level_test_strategy_report.md`](research/high_level_test_strategy_report.md)). Key tenets include:

*   **User-Centric Scenarios:** Tests are based on real-life user stories and scenarios from the PRD.
*   **End-to-End Validation:** Tests cover complete user journeys, verifying all system integrations.
*   **Multilingual & Cultural Accuracy:** Rigorous testing of English, isiXhosa, and Afrikaans interactions.
*   **POPIA Compliance by Design:** Explicit verification of all POPIA requirements.
*   **Performance & Data Efficiency Under Constraint:** Strict testing of the ≤5KB data limit and system responsiveness.
*   **API Integration Robustness:** Verification of all external API integrations.
*   **Launch Readiness & Pilot Objective Validation:** Tests directly support pilot program goals.
*   **AI Verifiability:** All HLTs have clearly defined, AI-verifiable completion criteria, enabling programmatic or semi-programmatic validation of test outcomes. This involves checking system responses, database states, logs, and network traffic against expected results.

## 3. Test Phases and High-Level Tests
The HLTs are organized into logical phases. Each test listed below will have a corresponding detailed HLT document in the [`tests/acceptance/high_level_tests/`](tests/acceptance/high_level_tests/) directory.

### Phase 1: User Onboarding & Account Management
*   **HLT-TC-001:** New User Onboarding, Language Auto-Detection, and POPIA Consent
    *   **AI Verifiable Completion Criterion:** System logs show successful pairing, correct language detection (e.g., "Molo" results in isiXhosa session), POPIA consent recorded with timestamp, and user presented with service bundle options. WhatsApp response matches expected welcome and consent flow in the detected language.
*   **HLT-TC-002:** Manual Language Switching
    *   **AI Verifiable Completion Criterion:** After user sends `/lang [target_language]`, subsequent system responses are consistently in the target language. User's language preference is updated in the database.
*   **HLT-TC-003:** User Self-Service Data Erasure (POPIA Right to be Forgotten)
    *   **AI Verifiable Completion Criterion:** After user sends `/delete` and confirms, system sends a confirmation message. Subsequent checks (e.g., database queries, API calls for user data) confirm all personally identifiable information for that user is anonymized or deleted.
*   **HLT-TC-004:** Service Bundle Selection during Onboarding
    *   **AI Verifiable Completion Criterion:** User's selection of a service bundle is recorded in the database. User receives confirmation and access to features within the selected bundle.

### Phase 2: Core Business Functionality (SME Focus)
*   **HLT-TC-005:** Payment Link Generation (SnapScan)
    *   **AI Verifiable Completion Criterion:** User sends "SnapScan [amount]". System responds with a correctly formatted, valid SnapScan payment link or QR code data. Transaction attempt is logged.
*   **HLT-TC-006:** Payment Link Generation (MoMo)
    *   **AI Verifiable Completion Criterion:** User sends "MoMo link [amount]". System responds with a correctly formatted, valid MoMo payment link. Transaction attempt is logged.
*   **HLT-TC-007:** Sales Logging
    *   **AI Verifiable Completion Criterion:** User sends "Sale [amount] [item]". System confirms sale logging. Database reflects the new sales entry associated with the user.
*   **HLT-TC-008:** Expense Tracking
    *   **AI Verifiable Completion Criterion:** User sends "Expense [amount] [item]". System confirms expense logging. Database reflects the new expense entry associated with the user.
*   **HLT-TC-009:** SME Customer Communication (Basic Order Update)
    *   **AI Verifiable Completion Criterion:** (Assuming a basic feature where SME can trigger a pre-defined update) SME sends a command to update an order. System sends a pre-defined WhatsApp message to a test customer number. Log confirms message dispatch.

### Phase 3: Community Services & Information Access
*   **HLT-TC-010:** Data-Light Directions Request
    *   **AI Verifiable Completion Criterion:** User asks "Directions to [test location]". System responds with concise, text-based directions. Response payload size verified to be ≤5KB.
*   **HLT-TC-011:** Q&A Capability (Knowledge Base Query)
    *   **AI Verifiable Completion Criterion:** User asks a predefined question (e.g., "How to register my business?"). System responds with accurate, relevant information from the knowledge base in the user's language.
*   **HLT-TC-012:** Accessing Bite-Sized Business Tips
    *   **AI Verifiable Completion Criterion:** User requests business tips. System delivers a relevant, concise tip in the user's language.
*   **HLT-TC-013:** Accessing Compliance Guides
    *   **AI Verifiable Completion Criterion:** User requests a compliance guide (e.g., "POPIA info"). System delivers a simplified guide in the user's language.

### Phase 4: Multilingual Support Verification
*   **HLT-TC-014:** End-to-End User Journey in English
    *   **AI Verifiable Completion Criterion:** Completion of a multi-step scenario (e.g., onboarding, log sale, ask question) entirely in English. All system prompts and responses are verified to be accurate and natural English.
*   **HLT-TC-015:** End-to-End User Journey in isiXhosa
    *   **AI Verifiable Completion Criterion:** Completion of a multi-step scenario entirely in isiXhosa. All system prompts and responses are verified to be accurate and natural isiXhosa.
*   **HLT-TC-016:** End-to-End User Journey in Afrikaans
    *   **AI Verifiable Completion Criterion:** Completion of a multi-step scenario entirely in Afrikaans. All system prompts and responses are verified to be accurate and natural Afrikaans.
*   **HLT-TC-017:** Consistent Language Context Maintenance
    *   **AI Verifiable Completion Criterion:** Throughout a user session involving multiple interactions, the language context remains consistent with the user's selected or auto-detected language. Verified by checking system responses.
*   **HLT-TC-018:** Error Message Handling in All Supported Languages
    *   **AI Verifiable Completion Criterion:** Triggering a known error condition (e.g., invalid command) results in a clear, helpful, and correctly translated error message in English, isiXhosa, and Afrikaans, depending on the user's language setting.

### Phase 5: POPIA Compliance Verification
*   **HLT-TC-019:** Audit Trail for POPIA Consent Logging
    *   **AI Verifiable Completion Criterion:** Database query confirms that each user's opt-in consent is logged with a timestamp and the specific version of the notice they agreed to.
*   **HLT-TC-020:** Verification of Data Erasure from Backend (Supabase)
    *   **AI Verifiable Completion Criterion:** After a `/delete` command is processed, direct database queries against Supabase confirm that all PII related to the user ID is either removed or fully anonymized.
*   **HLT-TC-021:** Data Segregation (Row-Level Security)
    *   **AI Verifiable Completion Criterion:** Authenticating as User A and attempting to query/access data belonging to User B via simulated API calls or database queries (with appropriate permissions for testing RLS) results in access denied or no data returned, as per RLS rules.
*   **HLT-TC-022:** Data Residency Verification (af-south-1)
    *   **AI Verifiable Completion Criterion:** Configuration check of the Supabase instance (via Supabase dashboard or API if available) confirms it is hosted in the `af-south-1` region.

### Phase 6: Performance and Data Efficiency
*   **HLT-TC-023:** Data Payload per Interaction (≤5KB)
    *   **AI Verifiable Completion Criterion:** Using network monitoring tools (or simulated analysis if direct monitoring is complex for AI), the data size of WhatsApp message payloads (both incoming and outgoing) for typical interactions is verified to be ≤5KB.
*   **HLT-TC-024:** System Response Time for Critical Actions (<10s)
    *   **AI Verifiable Completion Criterion:** Timestamp logs for critical actions (e.g., payment link generation, initial response to query) show that the duration from message receipt by the system to response dispatch is less than 10 seconds.
*   **HLT-TC-025:** System Performance under Concurrent Load (Simulated)
    *   **AI Verifiable Completion Criterion:** Using a load testing tool/script to simulate N concurrent users performing typical actions, system response times remain within acceptable thresholds (e.g., average <10s for critical, <5s for non-critical), and error rates are below X%.
*   **HLT-TC-026:** Functionality on Simulated Low-RAM Device Environment
    *   **AI Verifiable Completion Criterion:** (May require manual observation aided by AI for log analysis) Key user flows are executable without crashes or significant degradation when tested on actual low-spec devices or emulators configured to simulate low RAM and CPU. System logs show no excessive resource consumption warnings.

### Phase 7: API Integration Robustness
*   **HLT-TC-027:** Baileys Connection Stability and Message Reliability
    *   **AI Verifiable Completion Criterion:** System maintains a stable WhatsApp connection via Baileys over an extended test period (e.g., 1 hour) with periodic keep-alive messages. Test messages sent to and from the system are reliably delivered. Logs show no unexpected disconnects.
*   **HLT-TC-028:** Supabase CRUD Operations and RLS Enforcement
    *   **AI Verifiable Completion Criterion:** Standard user actions triggering Create, Read, Update, Delete operations in Supabase result in correct data state changes. Database queries verify RLS is correctly applied for each operation.
*   **HLT-TC-029:** n8n Workflow Execution and Outcome Verification
    *   **AI Verifiable Completion Criterion:** Triggering an n8n workflow (e.g., a scheduled task or a webhook-triggered flow from a user action) results in the n8n execution log showing successful completion, and any expected outcomes (e.g., a database update, a message sent via WhatsApp) are verified.
*   **HLT-TC-030:** Redis Message Queuing and Processing
    *   **AI Verifiable Completion Criterion:** Messages sent to Redis streams by one part of the system are successfully picked up and processed by worker components. Redis monitoring (if available) or application logs confirm queue depth changes and message processing.
*   **HLT-TC-031:** Composio Integration for Payment Link Generation
    *   **AI Verifiable Completion Criterion:** A payment link generation request involving Composio results in a valid link. Composio logs (if accessible) or system logs show successful API interaction with the payment provider via Composio.

### Phase 8: Reliability and Error Handling
*   **HLT-TC-032:** Unrecognized Command Handling
    *   **AI Verifiable Completion Criterion:** User sends an unrecognized command. System responds with a standardized, user-friendly error message in the user's current language, guiding them on valid commands.
*   **HLT-TC-033:** Graceful Handling of External API Failures
    *   **AI Verifiable Completion Criterion:** Simulating a failure from an external API (e.g., payment gateway via Composio returns an error). System logs the error, informs the user gracefully in their language about the issue, and provides alternative steps if applicable (e.g., "Please try again later").
*   **HLT-TC-034:** Session Recovery/Guidance on Network Interruption
    *   **AI Verifiable Completion Criterion:** (Challenging for full AI verification, may need observation) Simulating a brief network drop. System attempts to resend/receive messages upon reconnection or provides guidance. Logs indicate recovery attempts.

### Phase 9: Pilot Program Objective Validation
*   **HLT-TC-035:** SME User Onboarding and Core Tool Access for Pilot
    *   **AI Verifiable Completion Criterion:** A new SME user successfully completes onboarding, selects an SME-relevant bundle, and can successfully use core tools like sales logging and payment link generation. Database reflects the user as an SME. (Supports "50 active SMEs" goal).
*   **HLT-TC-036:** Corporate PoC Feature Validation
    *   **AI Verifiable Completion Criterion:** (Depends on defined PoC scope) If PoC involves specific data views or sub-tenant features, these are tested and verified to work as specified for a corporate test user. Access to anonymized trend data dashboard (if part of MVP) shows expected aggregated data.

## 4. Test Execution and Reporting

### 4.1 Test Environment
A dedicated, stable staging/testing environment that mirrors the production setup (Replit Reserved-VM, Supabase, Upstash Redis, n8n, Composio) as closely as possible is required. This environment must be isolated from development and production.

### 4.2 Test Data Management
*   Diverse, realistic test user profiles (SMEs, community members) with varied language preferences will be created.
*   Predefined sets of common business transactions, service requests, and queries in all supported languages will be used.
*   Test data will be managed securely, adhering to POPIA principles even in non-production environments. Data will be reset or cleaned up between major test runs as needed.

### 4.3 Pass/Fail Criteria
*   **Pass:** All test steps within an HLT are completed successfully, and all AI verifiable completion criteria are met. The observed behavior and system state match the expected outcomes.
*   **Fail:** Any test step fails, or any AI verifiable completion criterion is not met. The observed behavior or system state deviates from the expected outcomes.

### 4.4 Reporting
Test execution results will be tracked, and a summary report will be generated upon completion of each test phase and the overall HLT cycle. The report will include:
*   Number of tests executed.
*   Number of tests passed/failed.
*   Details of any failures, including steps to reproduce and variance from expected outcomes.
*   Overall assessment of system readiness based on HLT results.

## 5. AI Verifiability Approach
AI verifiability is central to this MATP. It will be achieved through:

*   **Parsing System Responses:** AI scripts will analyze WhatsApp messages received from Township Connect, checking for specific keywords, content structure, language accuracy, and presence/absence of expected information (e.g., payment links, error messages).
*   **Database State Verification:** AI-driven scripts will execute predefined SQL queries against the Supabase instance (via secure API or direct connection in the test environment) to confirm data creation, updates, deletions, RLS enforcement, and consistency.
*   **Log Analysis:** AI tools will parse application logs (from Node.js, n8n, Baileys) and potentially system logs to check for specific event occurrences, error codes, processing completion, and performance metrics (e.g., response times).
*   **Network Traffic Analysis (Simulated/Tool-Assisted):** For verifying data payload sizes (≤5KB), AI may analyze outputs from network monitoring tools or proxy logs, or use estimations based on message content and encoding if direct packet inspection is overly complex for automated scripting.
*   **API Interaction Simulation & Verification:** AI scripts can simulate API calls to Township Connect's endpoints (if any are exposed for testing) or interact with its components to verify integration points, sending specific inputs and validating outputs.
*   **File System Checks (Where Applicable):** In scenarios like data erasure, AI could verify (if architecturally relevant) the absence of user-specific files or data artifacts in storage.

This multi-faceted approach allows for a high degree of confidence in test outcomes, making the acceptance testing process more rigorous and efficient.