**Product Requirements Document: Township Connect**

**Version:** 1.0
**Date:** May 14, 2025
**Author:** AI Assistant (Gemini), based on User Blueprint
**Status:** Draft

**1. Introduction**

*   **1.1 Product Name:** Township Connect: Cape Town's WhatsApp Assistant
*   **1.2 Brief Description:** Township Connect is a WhatsApp-native assistant designed to empower Cape Town township residents by providing easy-to-use, data-light tools for running daily businesses, accessing vital services, and learning new skills directly through the WhatsApp application they already use and trust.
*   **1.3 Purpose:** The core purpose of Township Connect is to lower the barriers to digital and economic participation for township residents. It aims to achieve this by offering accessible, affordable, and multilingual functionalities for financial transactions, business management, logistics, information access, and skill development.

**2. Goals and Objectives**

*   **2.1 Problem Statement:** Township residents in Cape Town face significant challenges in accessing digital tools and participating fully in the economy due to:
    *   Lack of affordable and user-friendly business management tools.
    *   Prohibitive mobile data costs and device limitations.
    *   Language and digital literacy barriers.
    *   Inefficient access to local services and crucial information.
    *   Limited opportunities for relevant upskilling.
*   **2.2 Key Benefits:**
    *   **Economic Empowerment:** Enables users to earn and manage money more effectively.
    *   **Increased Accessibility & Inclusivity:** Saves costs, overcomes device and language barriers.
    *   **Enhanced Productivity & Efficiency:** Saves time by automating tasks.
    *   **Skills Development:** Raises digital fluency and business acumen.
    *   **Community Connection & Data Sovereignty:** Facilitates local commerce and keeps data control within the community.
*   **2.3 Specific Objectives:**
    *   Provide a free or low-cost tier for essential services for township users.
    *   Ensure all interactions are highly data-efficient (≤5 KB per text interaction).
    *   Support low-RAM Android phones with graceful fallbacks.
    *   Offer full functionality in English, isiXhosa, and Afrikaans with easy language switching.
    *   Achieve 100% POPIA compliance, including self-service data erasure.
    *   Onboard at least 50 active Small and Medium Enterprises (SMEs) within the first 60 days of pilot.
    *   Facilitate a measurable increase in digital payment adoption among users.
    *   Secure a paid Proof of Concept (PoC) with a corporate partner within 90 days.

**3. Target Audience**

*   **3.1 Primary Users:**
    *   **Township Entrepreneurs & Side-Hustlers:** Individuals running formal or informal businesses such as spaza-shop owners, street vendors, home-based service providers (e.g., tutors), and local delivery runners in Cape Town.
    *   **Local Community Members:** General residents of Cape Town townships requiring easy, low-data access to local information, essential services, or quick assistance for daily needs.

**4. User Stories / Use Cases**

*   **4.1 User Onboarding & Setup:**
    *   *As a new user, I want to scan a QR code from a flyer to easily pair my phone with Township Connect so I can start using its services quickly.*
    *   *As a user whose primary language is isiXhosa, I want the system to detect my language when I send "Molo" so that all further interactions are in isiXhosa.*
    *   *As a user, I want to be able to choose a "Street-Vendor CRM" bundle upon setup so I can immediately access relevant tools for my business.*
    *   *As a user, I want to view a clear POPIA notice and provide opt-in consent so I understand how my data is used.*
    *   *As a user, I want to use a simple command like "/lang afrikaans" to switch my preferred language at any time.*
    *   *As a user, I want to be able to send `/delete` to erase my data so I have control over my personal information.*
*   **4.2 Business & Finance (Entrepreneurs):**
    *   *As a spaza shop owner (Maria), when a customer wants to pay, I want to type "SnapScan 75" or "MoMo link 75" into Township Connect so I can quickly receive a payment link or QR code to share with my customer.*
    *   *As a street vendor, after making a sale, I want to easily log "Sale 75 sweets" so I can keep track of my income through WhatsApp.*
    *   *As a tutor, I want to track my expenses by sending "Expense R50 airtime" so I have a simple record.*
    *   *As a delivery runner, I want to send order confirmations and status updates to my customers via the assistant to keep them informed.*
*   **4.3 Logistics & Information (Community Members & Entrepreneurs):**
    *   *As a community member, I want to ask "Directions to Khayelitsha Clinic" so I can receive simple, data-light directions.*
    *   *As a user expecting a delivery, I want to request its real-time location through the assistant.*
    *   *As a user, I want to ask "How to register my small business?" in Afrikaans and receive a concise guide so I can learn about compliance.*
*   **4.4 Example Scenario (Definition of Done):**
    *   **New User Onboarding & Language Choice:** A new user in Khayelitsha scans a QR code at a kiosk and sends "Molo" via WhatsApp to Township Connect. The system detects isiXhosa and replies with a welcome message and service options in isiXhosa. The user is presented with the POPIA notice and opts in. The user successfully selects the "Street-Vendor CRM" bundle. The entire interaction is data-light.

**5. Product Features**

*   **5.1 Account Management & Onboarding:**
    *   **QR Code Phone Pairing:** Simple onboarding via QR scan.
    *   **Language Auto-Detection:** Detects language from initial greeting (e.g., "Hi," "Molo," "Hallo").
    *   **Manual Language Switching:** User-initiated language change via command (e.g., `/lang [en|xh|af]`).
    *   **Service Bundle Selection:** Users can choose pre-defined "bundles" of features (e.g., Street-Vendor CRM).
    *   **POPIA Compliance Module:** Opt-in notice presentation and consent logging.
    *   **Self-Service Data Erasure:** `/delete` command to wipe user data.
*   **5.2 Business & Finance Tools:**
    *   **Payment Link Generation:** Auto-generate SnapScan / MoMo payment links via simple commands.
    *   **Sales Logging:** Simple command to log sales transactions.
    *   **Expense Tracking:** Simple command to track business expenses.
    *   **Customer Communication:** Tools to reply to orders, send status updates, and broadcast promotions via WhatsApp.
*   **5.3 Logistics & Information Access:**
    *   **Parcel Location Tracking:** Real-time parcel location (integration dependent).
    *   **Map Directions:** Provides text-based or data-light map directions.
    *   **Pickup Reminders:** Automated reminders for logistical coordination.
    *   **Q&A Capability:** Access to a knowledge base for common queries.
*   **5.4 Learning & Upskilling:**
    *   **Bite-Sized Business Tips:** Regularly pushed or on-demand advice.
    *   **Compliance Guides:** Simple explanations of local business regulations.
    *   **Multi-Language Content:** All learning materials available in supported languages.

**6. Design and User Experience (UX)**

*   **6.1 Overall Style:** Simple & Intuitive, Clean & Uncluttered, Trustworthy & Reliable, Accessible & Inclusive, Helpful & Supportive.
*   **6.2 Interface:**
    *   **WhatsApp-Native:** All interactions occur within the WhatsApp chat interface.
    *   **Clarity:** Well-formatted, concise messages. Use of bold/italics for emphasis. Sparing, meaningful emoji use.
    *   **Simplicity:** Primarily relies on simple text commands. Potential for WhatsApp quick reply buttons where appropriate.
    *   **Branding:** Subtle, through the bot's profile picture and standardized greeting/closing messages.
*   **6.3 Onboarding Flow:** Scan QR at kiosk/flyer -> Phone pairs -> User sends first text (e.g., "Hi") -> Bot replies in detected language (or default) -> User selects a free "bundle" -> Chat commands trigger background workflows.

**7. Platform and Technical Requirements**

*   **7.1 Primary Platform:** WhatsApp, running on users' mobile devices (primarily Android, also iOS), WhatsApp Web, and WhatsApp Desktop.
*   **7.2 Technology Stack:**
    *   **WhatsApp Integration:** Baileys multi-session library.
    *   **Core Logic & Workers:** Node.js.
    *   **Orchestration/Automation:** n8n.
    *   **External Service Integration:** Composio (for SaaS tool connections without custom OAuth).
    *   **Database:** Supabase (PostgreSQL) for Auth, Row-Level Security, vector memory.
    *   **Message Queuing:** Redis Streams (Upstash) for message movement and worker scaling.
    *   **Hosting:** One Replit Reserved-VM for Node WhatsApp hub, worker pool, n8n, and tiny web portal.
*   **7.3 Data Residency:** All user data to be stored in the `af-south-1` (Cape Town) region via Supabase.

**8. Non-Functional Requirements**

*   **8.1 Performance:**
    *   **Data Efficiency:** Each text interaction must consume ≤5 KB of data. Optional media to be compressed.
    *   **Response Time:** Critical actions like payment link generation should complete in <10 seconds.
*   **8.2 Scalability:**
    *   System must support hundreds of concurrent WhatsApp sockets on a single Baileys process.
    *   Worker pool must auto-scale based on Redis Streams queue depth (e.g., queueDepth/10).
*   **8.3 Reliability:**
    *   **Uptime:** Replit Reserved-VM ensures no hibernation. Watchdog process for auto-reconnecting Baileys sockets.
*   **8.4 Usability & Accessibility:**
    *   **Device Compatibility:** Graceful fallback and optimal performance for sub-1GB RAM Android phones.
    *   **Language Support:** Full support for English, isiXhosa, Afrikaans.
    *   **Interaction Model:** Simple, intuitive chat commands; no complex menus or jargon.
*   **8.5 Security:**
    *   **Data Segregation:** Supabase Row-Level Security to lock each user's data.
    *   **Credential Encryption:** Baileys credentials encrypted with user-specific keys before storage.
    *   **Secure Integrations:** Secure handling of API keys for Composio/n8n.
*   **8.6 Compliance:**
    *   Full POPIA compliance: Opt-in consent, data residency, purpose limitation, user data access/deletion rights (`/delete` for right-to-be-forgotten).
*   **8.7 Cost-Effectiveness:**
    *   Operational cost targeted at < US$0.15 per active user per month (beyond the first 10 free users).

**9. Success Metrics and KPIs**

*   **User Adoption & Growth:**
    *   Number of unique users onboarded (phone pairings).
    *   Number of active township ambassadors recruited.
    *   Number of MTN devices paired during pilot.
*   **Engagement:**
    *   Total messages processed per day/week/month.
    *   Average number of interactions per active user.
    *   Number of active SMEs (target: 50 by Day 60).
    *   Popular commands and feature usage rates (tracked via dashboard).
*   **Community Impact:**
    *   Percentage of users on low-RAM devices.
    *   Distribution of language usage (English, isiXhosa, Afrikaans).
*   **Monetization (Post-Threshold/Pilot):**
    *   Revenue from the 2% fee on SnapScan/MoMo transactions (after R10,000 threshold).
    *   Number of corporate licenses for dashboards and priority API slots.
*   **Pilot Program Success (as per Roadmap):**
    *   Day 0-30: 3 township ambassadors, 50 MTN devices paired, 300 messages processed.
    *   Day 31-60: Three bundles launched, weekly voice-note clinics run, 50 active SMEs.
    *   Day 61-90: First corporate onboarded (e.g., Pick n Pay township stores), insights deck presented, paid PoC signed.

**10. Future Considerations (Roadmap)**

*   **10.1 Pilot Roadmap (90 days):**
    *   **Day 0-30:** Recruit 3 township ambassadors, pair 50 MTN devices, hit 300 messages.
    *   **Day 31-60:** Launch three bundles, run weekly voice-note clinics, reach 50 active SMEs.
    *   **Day 61-90:** Onboard first corporate (e.g., Pick n Pay township stores), present insights deck, sign paid PoC.
*   **10.2 Nice-to-Haves (Post-Pilot):** Voice interaction (voice notes to text/speech), expanded "Bundle" marketplace, basic inventory management, ultra-light e-commerce (mini-catalog via link), automated customer follow-ups, deeper financial literacy tools, local job/gig matching (simple), integration with local municipal services, peer-to-peer support groups, offline access for specific learning content.
*   **10.3 Long-Term Vision:** Evolve into the dominant digital OS for SA township economies; a "township-in-a-box" platform; create a community-centric data cooperative; replicate the model globally; potential transition to a co-operative/community-owned governance model.

**11. Monetization Strategy**

*   **11.1 Free Tier:** Free access to text-based interactions and three starter bundles for all township users.
*   **11.2 Transaction Fees:** A 2% fee on SnapScan / MoMo transactions processed through the platform, applied after a user exceeds an R10,000 cumulative transaction threshold.
*   **11.3 Corporate Licenses:** Paid licenses for corporate clients to access:
    *   Opt-in dashboards of anonymized user trends (language mix, hot commands, ZIP clusters).
    *   Priority API slots for their specific service integrations.
    *   Ability to run their own WhatsApp number as a sub-tenant session.
*   **11.4 Revenue Reinvestment:** Revenue generated will be used to fund additional low-cost MTN smartphones for township users, further expanding the user base and impact.

**12. Corporate Value Proposition**

*   **12.1 Reach Township Customers:** Enables corporates to run their own WhatsApp number as a sub-tenant session on the platform, providing a direct channel to township consumers.
*   **12.2 Customer Insight:** Offers access to opt-in dashboards of anonymized, aggregated trends (language mix, popular commands, ZIP code clusters) for market understanding.
*   **12.3 ESG & Digital Inclusion:** Provides transparent KPIs on low-RAM device usage and language localization, contributing to corporate ESG goals and demonstrating commitment to digital inclusion.
