# HLT-TC-013: Accessing Compliance Guides

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that users can request and receive simplified compliance guides through Township Connect in their preferred language, helping them understand local business regulations.

## 2. User Story / Scenario
* **Feature (PRD 5.4):** Compliance Guides: Simple explanations of local business regulations.
* **Scenario:** A user requests information about a specific regulation or compliance requirement and receives a simplified guide in their preferred language.

## 3. Preconditions
* The user is onboarded and has an active session with Township Connect.
* User's language preference is set (English, isiXhosa, or Afrikaans).
* The system's compliance guide database is populated with information about common regulations (e.g., POPIA, business registration, tax compliance) in all supported languages.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | Send the message: "POPIA info" or "Tell me about POPIA" (in English) | System responds with a simplified guide about POPIA (Protection of Personal Information Act) in English. The guide should explain key requirements in simple terms relevant to small businesses. Response must be data-light (≤5KB). |
| 2 | Send the message: "Inligting oor besigheidsbelasting" (Business tax information in Afrikaans) | System responds with a simplified guide about business taxation in Afrikaans. Response must be data-light (≤5KB). |
| 3 | Send the message: "Iimfuno zokubhalisa ishishini" (Business registration requirements in isiXhosa) | System responds with a simplified guide about business registration requirements in isiXhosa. Response must be data-light (≤5KB). |
| 4 | Send a message requesting information about a different compliance area: "Health regulations for food business" (in English) | System responds with relevant information about health regulations for food businesses in English. Response must be data-light (≤5KB). |

## 5. Acceptance Criteria (AI Verifiable)
* The system correctly identifies the user's request for compliance information.
* Guides are provided in the language of the request (or the user's set language preference).
* Compliance guides are simplified, accurate, and relevant to township entrepreneurs.
* Information is presented in clear, non-technical language appropriate for users with varying levels of education.
* All responses are data-light (≤5KB per interaction).
* The system logs the compliance guide request and delivery for analytics purposes.

## 6. References
* PRD Section 5.4: Learning & Upskilling features
* Master Acceptance Test Plan Section 3, Phase 3: Community Services & Information Access

## 7. Notes
* This test focuses on the system's ability to provide simplified compliance information, not on providing legal advice.
* For AI verification purposes, a set of expected compliance topics and formats should be prepared in advance to verify that responses match the expected structure and accuracy.
* The test should verify that guides include practical next steps or resources where users can find more detailed information if needed.
* Special attention should be paid to ensuring that simplified explanations remain legally accurate while being accessible to users with varying levels of education and business experience.