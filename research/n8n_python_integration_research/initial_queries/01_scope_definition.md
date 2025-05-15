# Research Scope Definition: n8n Setup and Python Application Integration

## 1. Overall Research Objective
To conduct comprehensive research on establishing and integrating n8n (a workflow automation tool) with a Python-based application, specifically focusing on the requirements and context of the "Township Connect" project.

## 2. Key Research Areas

The research will cover the following core areas:

### 2.1. n8n Deployment Options
*   **Self-Hosted n8n:**
    *   Methods and requirements for self-hosting (e.g., Docker, Node.js direct install).
    *   Considerations for hosting on platforms like Replit (as mentioned in project context).
    *   Pros and cons (cost, control, maintenance).
*   **n8n Cloud:**
    *   Features and limitations of the managed n8n cloud service.
    *   Pricing models.
    *   Pros and cons (ease of use, scalability, cost).

### 2.2. n8n Workflow Creation for External Triggers
*   Designing n8n workflows that can be initiated by external events.
*   **Webhook Node:** Configuration and usage of the n8n Webhook node to receive HTTP requests.
*   Other potential trigger mechanisms relevant to the project (e.g., message queues, specific n8n nodes for services like Twilio or WAHA if available).

### 2.3. Python Application Triggering n8n Workflows
*   Methods for a Python application to initiate an n8n workflow.
*   Making HTTP requests from Python to an n8n webhook URL.
    *   Sending data/payloads.
    *   Handling responses from n8n.
*   Authentication and security considerations for this interaction.

### 2.4. n8n Workflow Interacting with Python Applications
*   Methods for an n8n workflow to execute or communicate with Python logic.
*   **Execute Command Node:**
    *   Running Python scripts directly from n8n.
    *   Passing data to scripts and retrieving output.
    *   Environment and dependency management for Python scripts executed by n8n.
*   **HTTP Request Node:**
    *   Calling HTTP endpoints exposed by a Python application (e.g., a Flask/FastAPI server).
    *   Sending data to the Python API and processing its response within n8n.
*   Security considerations for these interactions.

### 2.5. Security Best Practices
*   Securing n8n instances (self-hosted and cloud).
    *   Access control, user management.
    *   Network security (firewalls, HTTPS).
    *   Managing credentials securely within n8n.
*   Securing n8n workflows.
    *   Input validation.
    *   Error handling.
    *   Preventing unauthorized access to webhook URLs.
    *   Securing data in transit and at rest within workflows.

### 2.6. Project-Specific Contextual Considerations ("Township Connect")
*   Integration with WhatsApp gateways (WAHA, Twilio) via n8n for receiving incoming messages.
*   n8n calling the Python core logic (`core_handler.py`).
*   Python core logic potentially triggering other n8n workflows.
*   Use of Supabase for the database.
*   Potential hosting on Replit for n8n and the Python application.
*   Data-light communication requirements.
*   POPIA compliance implications for data handled by n8n.

## 3. Out of Scope
*   Detailed comparison of every possible WhatsApp gateway beyond WAHA and Twilio, unless directly relevant to n8n integration patterns.
*   In-depth financial cost-benefit analysis of self-hosting vs. cloud beyond general pros/cons, unless readily available.
*   Implementation of the entire "Township Connect" application; the focus is on the n8n-Python interface.

This scope will guide the subsequent stages of research, including data collection, analysis, and synthesis, ensuring that the findings are relevant and actionable for the "Township Connect" project.