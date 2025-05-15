# Potential Information Sources: n8n Setup and Python Application Integration

This document lists potential information sources that will be consulted to answer the key research questions outlined in `02_key_questions.md`. The primary method of information gathering will be through targeted queries to an advanced AI search tool (e.g., Perplexity AI via MCP).

## 1. Official Documentation

*   **n8n Official Documentation:**
    *   **Website:** `docs.n8n.io`
    *   **Focus Areas:** Installation guides (Docker, Node.js), n8n Cloud features, Node documentation (Webhook, Execute Command, HTTP Request, PostgreSQL, etc.), security best practices, API usage, workflow examples, credential management.
*   **Python Official Documentation:**
    *   **Website:** `docs.python.org`
    *   **Focus Areas:** `requests` library (for HTTP calls), `subprocess` module (if considering direct script execution from Python, though less likely for n8n interaction), standard library features relevant to API development.
*   **Flask/FastAPI Documentation (if Python exposes an API):**
    *   **Websites:** `flask.palletsprojects.com`, `fastapi.tiangolo.com`
    *   **Focus Areas:** API endpoint creation, request/response handling, authentication methods.
*   **Supabase Documentation:**
    *   **Website:** `supabase.com/docs`
    *   **Focus Areas:** PostgreSQL integration, REST API, authentication, security.
*   **Twilio Documentation:**
    *   **Website:** `www.twilio.com/docs`
    *   **Focus Areas:** WhatsApp API, n8n integration guides (if any), webhook configurations.
*   **WAHA (WhatsApp HTTP API) Documentation (if available/applicable):**
    *   **Focus Areas:** API endpoints, authentication, n8n integration patterns.
*   **Replit Documentation:**
    *   **Website:** `docs.replit.com`
    *   **Focus Areas:** Reserved-VM capabilities, environment variables, hosting limitations, deploying Node.js/Python applications.

## 2. Community Forums and Discussions

*   **n8n Community Forum:**
    *   **Website:** `community.n8n.io`
    *   **Focus Areas:** User experiences with self-hosting, specific node configurations, workflow examples, troubleshooting common issues, Python integration discussions, security advice.
*   **Stack Overflow:**
    *   **Website:** `stackoverflow.com`
    *   **Focus Areas:** Tagged questions for `n8n`, `python`, `webhooks`, `api-integration`, `docker`, `replit`, `supabase`.
*   **Reddit Communities:**
    *   e.g., `r/n8n`, `r/selfhosted`, `r/Python`, `r/devops`
    *   **Focus Areas:** Practical advice, user reviews, deployment stories, security tips.
*   **GitHub Issues and Discussions:**
    *   For n8n repository, relevant Python libraries, or gateway projects.
    *   **Focus Areas:** Bug reports, feature requests, specific technical challenges.

## 3. Tutorials, Blog Posts, and Articles

*   **Technical Blogs:** Search for articles on platforms like Medium, Dev.to, Smashing Magazine, personal developer blogs.
    *   **Keywords for AI Search:** "n8n python integration tutorial", "secure n8n webhook", "n8n execute python script", "deploy n8n docker replit", "n8n best practices security", "n8n twilio whatsapp", "n8n waha setup".
*   **YouTube Channels:** Search for video tutorials demonstrating n8n setup, workflow creation, and integrations.
*   **n8n Blog:** Official blog posts from the n8n team.

## 4. AI Search Tool (Primary Method)

*   **Tool:** General AI Search (e.g., Perplexity AI via MCP tool).
*   **Strategy:**
    *   Formulate specific queries based on the `02_key_questions.md`.
    *   Iteratively refine queries based on initial findings.
    *   Request sources and citations for all significant claims or technical procedures.
    *   Prioritize recent information (n8n is an evolving platform).
    *   Cross-reference information from multiple AI-retrieved sources if possible.

## 5. Project-Specific Documents (Context)

*   [`docs/project_plan.md`](docs/project_plan.md)
*   [`docs/prd.md`](docs/prd.md)
    *   These documents provide the context for "Township Connect" and will help tailor the research to specific project needs and constraints (e.g., Replit hosting, WAHA/Twilio, Supabase).

By leveraging these sources, particularly through systematic AI-powered searches, the research aims to gather comprehensive and accurate information to address all key questions.