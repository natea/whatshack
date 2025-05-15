# Key Research Questions: n8n Setup and Python Application Integration

This document outlines the key questions that this research aims to answer, categorized by the research areas defined in the `01_scope_definition.md` document.

## 1. n8n Deployment Options

*   **Q1.1:** What are the step-by-step procedures for self-hosting n8n using Docker? What are the typical resource requirements (CPU, RAM, disk)?
*   **Q1.2:** What are the considerations and potential challenges of self-hosting n8n on a platform like Replit, given its environment and limitations?
*   **Q1.3:** What are the primary advantages and disadvantages of self-hosting n8n versus using n8n Cloud, specifically concerning cost, control, maintenance, and scalability for a project like "Township Connect"?
*   **Q1.4:** What are the current pricing tiers for n8n Cloud, and what features are included/excluded at different levels relevant to the project's needs (e.g., number of active workflows, execution limits)?

## 2. n8n Workflow Creation for External Triggers

*   **Q2.1:** How is an n8n Webhook node configured to securely receive POST requests with JSON payloads from an external application (e.g., a Python script or a WhatsApp gateway)?
*   **Q2.2:** What are best practices for structuring an n8n workflow that is triggered by a webhook, including initial data validation, error handling, and logging?
*   **Q2.3:** Are there specific n8n nodes or recommended patterns for integrating with WhatsApp gateways like WAHA or Twilio to receive incoming messages? How is authentication handled with these gateways within n8n?

## 3. Python Application Triggering n8n Workflows

*   **Q3.1:** What is the recommended method for a Python application to securely send an HTTP POST request to an n8n webhook URL, including passing a JSON payload?
*   **Q3.2:** How can a Python application handle responses (synchronous or asynchronous acknowledgments) from an n8n workflow after triggering it?
*   **Q3.3:** What authentication mechanisms can be used to secure the n8n webhook endpoint when being called from a Python application (e.g., API keys, token authentication)?

## 4. n8n Workflow Interacting with Python Applications

*   **Q4.1:** How can the n8n "Execute Command" node be used to run a Python script?
    *   How are arguments/data passed from n8n to the Python script?
    *   How is output (stdout, stderr, exit codes) from the Python script captured and used in the n8n workflow?
    *   What are the security implications and best practices for using the "Execute Command" node, especially concerning script paths and permissions?
    *   How should Python environments and dependencies be managed for scripts executed this way, particularly in a Replit-like environment?
*   **Q4.2:** How can the n8n "HTTP Request" node be configured to call an API endpoint exposed by a Python application (e.g., built with Flask or FastAPI)?
    *   How is data passed from n8n to the Python API?
    *   How is the response from the Python API processed within the n8n workflow?
    *   What authentication methods are suitable for n8n to securely call a Python API?
*   **Q4.3:** What are the pros and cons of using the "Execute Command" node versus the "HTTP Request" node for n8n-to-Python communication in the context of "Township Connect" (considering factors like performance, scalability, ease of development, security)?

## 5. Security Best Practices

*   **Q5.1:** What are the essential security measures for a self-hosted n8n instance (e.g., HTTPS setup, firewall rules, regular updates, secure credential management)?
*   **Q5.2:** What security features and practices are provided by n8n Cloud?
*   **Q5.3:** How can n8n workflow credentials (for accessing external services like Supabase or Python APIs) be stored and managed securely?
*   **Q5.4:** What are best practices for securing n8n webhook URLs to prevent unauthorized access or abuse?
*   **Q5.5:** How can input validation be implemented within n8n workflows to protect against common vulnerabilities (e.g., injection attacks if data is passed to scripts)?
*   **Q5.6:** What are the specific security considerations for n8n when handling potentially sensitive user data from WhatsApp, in line with POPIA requirements?

## 6. Project-Specific Contextual Considerations ("Township Connect")

*   **Q6.1:** What is the most effective way to architect the flow where n8n receives a WhatsApp message (via WAHA/Twilio), then calls the `core_handler.py` Python logic, considering data-light principles and potential Replit hosting?
*   **Q6.2:** How can the Python `core_handler.py` trigger a *different* n8n workflow (e.g., for a background task like generating a report, or as part of the payment link generation flow mentioned in the project plan)?
*   **Q6.3:** Are there any specific n8n configurations or workflow patterns that are particularly well-suited for interactions with Supabase (e.g., using n8n's PostgreSQL node or calling Supabase REST API)?
*   **Q6.4:** What are the performance implications of running n8n (self-hosted) and the Python application on the same Replit Reserved-VM, particularly regarding resource contention?

Answering these questions will provide a solid foundation for understanding how to effectively and securely implement n8n within the "Township Connect" project architecture.