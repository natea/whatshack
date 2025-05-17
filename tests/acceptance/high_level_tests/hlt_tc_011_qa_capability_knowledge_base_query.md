# HLT-TC-011: Q&A Capability (Knowledge Base Query)

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that users can ask common questions and receive accurate, concise information from Township Connect's knowledge base in their preferred language.

## 2. User Story / Scenario
* **User Story (PRD 4.3):** *As a user, I want to ask "How to register my small business?" in Afrikaans and receive a concise guide so I can learn about compliance.*
* **Feature (PRD 5.3):** Q&A Capability: Access to a knowledge base for common queries.
* **Scenario (HLT Strategy 4.3):** A user asks a common question (e.g., "How to register my small business?"). System provides a concise, accurate guide in the user's selected language.

## 3. Preconditions
* The user is onboarded and has an active session with Township Connect.
* User's language preference is set (English, isiXhosa, or Afrikaans).
* The system's knowledge base is populated with common questions and answers, including business registration information in all supported languages.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | Send the message: "How to register my small business?" (in English) | System responds with a concise, accurate guide on business registration in English. The response should include key steps, required documents, and relevant government offices or websites. Response must be data-light (≤5KB). |
| 2 | Send the message: "Hoe om my klein besigheid te registreer?" (in Afrikaans) | System responds with the same information but in Afrikaans, maintaining accuracy and cultural relevance. Response must be data-light (≤5KB). |
| 3 | Send the message: "Ndingabhalisela njani ishishini lam elincinci?" (in isiXhosa) | System responds with the same information but in isiXhosa, maintaining accuracy and cultural relevance. Response must be data-light (≤5KB). |
| 4 | Send a different knowledge base query: "What permits do I need for a food business?" (in English) | System responds with relevant information about food business permits in English. Response must be data-light (≤5KB). |

## 5. Acceptance Criteria (AI Verifiable)
* The system correctly identifies the user's question as a knowledge base query.
* Responses are provided in the language of the query (or the user's set language preference if query language detection is not implemented).
* Responses contain accurate, relevant information that directly answers the user's question.
* All responses are concise and data-light (≤5KB per interaction).
* The system logs the query and response for analytics purposes.
* If the knowledge base doesn't contain an answer to the user's question, the system provides a graceful "I don't know" response with suggestions for alternative sources of information.

## 6. References
* PRD Section 4.3: User Stories for Logistics & Information
* PRD Section 5.3: Q&A Capability feature description
* High-Level Test Strategy Report Section 4.3: Community Services & Information Access

## 7. Notes
* This test focuses on the system's ability to provide accurate information from its knowledge base, not on its ability to generate new information or provide real-time data.
* The test should be expanded to include a variety of common questions that township entrepreneurs and community members might ask, based on the knowledge base content.
* For AI verification purposes, a set of expected responses for test questions should be prepared in advance to compare against actual system responses.