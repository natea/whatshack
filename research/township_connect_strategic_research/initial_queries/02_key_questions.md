# Key Strategic Questions: Township Connect Research

**Version:** 1.0
**Date:** May 17, 2025

This document outlines the key strategic questions that will guide the research for the Township Connect project. These questions are derived from the Overall Project Goal, the User Blueprint ([`docs/prd.md`](docs/prd.md)), and the defined Research Scope ([`research/township_connect_strategic_research/initial_queries/01_scope_definition.md`](research/township_connect_strategic_research/initial_queries/01_scope_definition.md:1)).

## 1. Target Audience & Market Context

1.  **Needs & Pain Points:**
    *   What are the most pressing unmet needs of Cape Town township entrepreneurs (spaza shops, street vendors, service providers, delivery runners) regarding business management, financial transactions, and customer communication that can be realistically addressed via a WhatsApp assistant?
    *   What are the primary challenges faced by general township residents in accessing local services, information, and skills development opportunities?
    *   How significant are data costs and device limitations (low-RAM phones) as barriers to digital tool adoption in this demographic?
2.  **Existing Behaviors & Solutions:**
    *   How are township entrepreneurs currently managing sales, expenses, customer interactions, and payments? What informal or formal tools (digital or analog) are they using?
    *   What is the current level of WhatsApp proficiency and usage patterns among the target audience for tasks beyond basic communication?
    *   Who are the key existing players (formal or informal, digital or community-based) providing similar or complementary services, and what are their strengths and weaknesses?
3.  **Cultural & Language Considerations:**
    *   What are the specific communication preferences and cultural nuances in English, isiXhosa, and Afrikaans that should inform the assistant's tone, terminology, and interaction design?
    *   What are the trust factors and potential barriers to adopting a new digital service like Township Connect within these communities?

## 2. Technology & Platform Feasibility

4.  **Data Efficiency (≤5 KB/interaction):**
    *   What are proven techniques and best practices for designing WhatsApp interactions (text, commands, potential use of rich media placeholders) to strictly adhere to a ≤5 KB data footprint per interaction?
    *   What are the data implications of various WhatsApp message types (text, quick replies, media messages if used sparingly) and how can they be optimized?
5.  **Multilingual Support:**
    *   What are effective strategies for seamless language detection, switching, and content management for English, isiXhosa, and Afrikaans within a WhatsApp bot?
    *   What are common pitfalls in multilingual chatbot design for these specific languages?
6.  **POPIA Compliance:**
    *   What are the precise requirements for obtaining and logging POPIA-compliant consent via WhatsApp for data processing, communication, and potential data sharing (anonymized trends for corporates)?
    *   What are best practices for implementing self-service data access and erasure (`/delete` command) in a way that is auditable and user-friendly via WhatsApp?
    *   How should data residency in `af-south-1` be technically ensured and communicated for POPIA compliance?
7.  **Low-RAM Device Compatibility:**
    *   What specific design considerations and technical fallbacks are necessary to ensure a smooth user experience on low-RAM (sub-1GB) Android phones?
    *   How does WhatsApp client performance on such devices impact potential interaction complexity?
8.  **Technical Stack & Integrations:**
    *   What are the key risks and mitigation strategies associated with using Baileys for multi-session WhatsApp integration, especially concerning stability and WhatsApp's Terms of Service?
    *   How can n8n, Composio, Supabase, and Redis Streams be effectively orchestrated on a Replit Reserved-VM to meet performance, scalability (hundreds of concurrent sockets, worker scaling), and reliability requirements?
    *   What are the technical prerequisites and challenges for integrating with payment gateways like SnapScan and MoMo for link generation?

## 3. Business Model & Sustainability

9.  **SME Onboarding & Engagement (Pilot Target: 50 Active SMEs):**
    *   What are the most effective, low-cost strategies for reaching, educating, and onboarding township SMEs onto Township Connect?
    *   What features or "service bundles" (e.g., Street-Vendor CRM) are most likely to drive initial adoption and sustained active use among SMEs?
    *   How can "township ambassadors" be effectively recruited and leveraged for user acquisition and support?
10. **Corporate PoC & Value Proposition (Pilot Target: Secure 1 Paid PoC):**
    *   What specific, quantifiable value can Township Connect offer to corporate partners (e.g., retailers like Pick n Pay, financial service providers) interested in reaching or understanding the township market?
    *   What kind of "insights deck" or data (anonymized, aggregated) would be most compelling for a corporate PoC?
    *   What are the typical concerns or requirements of corporates when considering partnerships involving new technology platforms and sensitive user data (even if anonymized)?
11. **Monetization Viability:**
    *   How receptive is the target SME audience likely to be to a 2% transaction fee on digital payments (SnapScan/MoMo) after an R10,000 threshold? What is a realistic adoption rate for these payment methods through the platform?
    *   What pricing models for corporate licenses (dashboards, API access, sub-tenant sessions) are common or likely to be acceptable?
12. **Community Trust & Impact:**
    *   What are the most critical factors for building and maintaining trust with the township community?
    *   How can the platform demonstrably contribute to economic empowerment and digital inclusion beyond the core functionalities?

## 4. Pilot Program Success

13. **Achieving Pilot Metrics:**
    *   What are the key dependencies and potential roadblocks for achieving the 90-day pilot targets (ambassadors, MTN device pairings, message volume, active SMEs, corporate PoC)?
    *   What early warning indicators should be monitored to assess pilot progress and identify need for course correction?
14. **Learning & Iteration:**
    *   What mechanisms should be in place during the pilot to gather user feedback effectively for rapid iteration and improvement of the service?

These questions will serve as the foundation for formulating specific search queries and structuring the data collection and analysis phases of the research.