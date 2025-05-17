# HLT-TC-012: Accessing Bite-Sized Business Tips

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that users can request and receive relevant, concise business tips through Township Connect in their preferred language.

## 2. User Story / Scenario
* **Feature (PRD 5.4):** Bite-Sized Business Tips: Regularly pushed or on-demand advice.
* **Scenario:** A user requests business tips and receives relevant, concise advice in their preferred language.

## 3. Preconditions
* The user is onboarded and has an active session with Township Connect.
* User's language preference is set (English, isiXhosa, or Afrikaans).
* The system's business tips database is populated with various categories of tips in all supported languages.

## 4. Test Steps

| Step | User Action (via WhatsApp) | Expected System Response (WhatsApp Message & Backend) |
|------|----------------------------|------------------------------------------------------|
| 1 | Send the message: "Business tip" or "Give me a business tip" (in English) | System responds with a concise, relevant business tip in English. The tip should be practical and applicable to township entrepreneurs. Response must be data-light (≤5KB). |
| 2 | Send the message: "Besigheidswenk" (in Afrikaans) | System responds with a business tip in Afrikaans. The tip may be the same as in Step 1 or different, but must be in correct Afrikaans. Response must be data-light (≤5KB). |
| 3 | Send the message: "Icebo leshishini" (in isiXhosa) | System responds with a business tip in isiXhosa. The tip may be the same as in previous steps or different, but must be in correct isiXhosa. Response must be data-light (≤5KB). |
| 4 | Send a message requesting a specific category of tip: "Marketing tip" (in English) | System responds with a relevant marketing-focused business tip in English. Response must be data-light (≤5KB). |

## 5. Acceptance Criteria (AI Verifiable)
* The system correctly identifies the user's request for a business tip.
* Tips are provided in the language of the request (or the user's set language preference).
* Tips are concise, practical, and relevant to township entrepreneurs.
* All responses are data-light (≤5KB per interaction).
* If category-specific tips are supported, the system correctly filters tips based on the requested category.
* The system logs the tip request and delivery for analytics purposes.

## 6. References
* PRD Section 5.4: Learning & Upskilling features
* Master Acceptance Test Plan Section 3, Phase 3: Community Services & Information Access

## 7. Notes
* This test focuses on on-demand business tips. If the system also supports scheduled/pushed tips, a separate test or additional steps should verify that functionality.
* For AI verification purposes, a set of expected tip categories and formats should be prepared in advance to verify that responses match the expected structure and relevance.
* The test should verify that tips are appropriate for the target audience (township entrepreneurs) and provide practical, actionable advice rather than generic business platitudes.