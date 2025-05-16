# n8n Instance Details for Township Connect

This document provides instructions and details for setting up, accessing, and managing the self-hosted n8n instance for the Township Connect project. This instance is intended to be run on the project's Replit Reserved-VM as per the project requirements.

## 1. Setting up n8n on Replit Reserved-VM

### Prerequisites:
*   Access to the Township Connect Replit project with a Reserved-VM.
*   Node.js and npm/npx available in the Replit environment (usually standard).

### Installation and Running:
n8n can be started using `npx`. This command will download the latest version of n8n and run it.

1.  **Configure Replit Run Command:**
    In your Replit project, set the "Run" command in the `.replit` file or Replit's UI to:
    ```sh
    npx n8n
    ```
    Alternatively, you can run this command directly in the Replit Shell to start n8n.

2.  **Set Up Authentication (Recommended):**
    It is highly recommended to secure your n8n instance with basic authentication.
    *   Go to the "Secrets" tab in your Replit project.
    *   Add the following secrets:
        *   `N8N_BASIC_AUTH_ACTIVE`: `true`
        *   `N8N_BASIC_AUTH_USER`: `your_chosen_admin_username` (Replace with a strong, unique username)
        *   `N8N_BASIC_AUTH_PASSWORD`: `your_chosen_strong_password` (Replace with a strong, unique password)
    *   **Important**: Choose strong credentials.

3.  **Start n8n:**
    Run the Repl (using the "Run" button if configured) or execute `npx n8n` in the Replit Shell. n8n will start, typically on port 5678. Replit should automatically make this port accessible via a public URL.

## 2. Access URL

Once n8n is running, it will be accessible via a public URL provided by Replit. The format is typically:

`https://YOUR_REPLIT_PROJECT_NAME.YOUR_REPLIT_USERNAME.repl.co`

*   **Replace `YOUR_REPLIT_PROJECT_NAME` with your actual Replit project's name.**
*   **Replace `YOUR_REPLIT_USERNAME` with your Replit username.**

If Replit assigns a specific path for n8n or uses a different URL structure, adjust accordingly. Check the Replit interface for the exact URL once the application is running.

## 3. Credentials Management

*   **Basic Authentication Credentials:**
    If you configured basic authentication as described in Step 1.2, the username and password are the values you set for `N8N_BASIC_AUTH_USER` and `N8N_BASIC_AUTH_PASSWORD` Replit Secrets. These are used to log in to the n8n UI.

*   **n8n API Keys (for programmatic access):**
    For other components or scripts to interact with n8n programmatically, you should generate an API key from within the n8n UI:
    1.  Log in to your n8n instance using the basic authentication credentials.
    2.  Navigate to "Settings" (usually a gear icon or user menu).
    3.  Find the "API" section.
    4.  Generate a new API key.
    5.  **Crucial:** Copy this API key immediately and store it securely, for example, as a new Replit Secret named `N8N_API_KEY`. This key will not be shown again.

    This `N8N_API_KEY` can then be used by other services that need to interact with your n8n workflows via its API.

## 4. Verification Command

To verify that the n8n instance is running and accessible, open the Replit Shell and use the following `curl` command. Remember to replace the placeholders with your actual Replit project name and username.

**Without Basic Authentication (not recommended for long-term use):**
```sh
curl https://YOUR_REPLIT_PROJECT_NAME.YOUR_REPLIT_USERNAME.repl.co/healthz
```

**With Basic Authentication Enabled:**
```sh
curl -u "your_chosen_admin_username:your_chosen_strong_password" https://YOUR_REPLIT_PROJECT_NAME.YOUR_REPLIT_USERNAME.repl.co/healthz
```
(Replace `your_chosen_admin_username` and `your_chosen_strong_password` with the credentials you set in Replit Secrets.)

A successful response (e.g., HTTP status 200 OK, often with the text "OK" or a simple JSON response) indicates that n8n is running and healthy. If `/healthz` is not found or gives an error, you can try accessing the base URL:
```sh
curl https://YOUR_REPLIT_PROJECT_NAME.YOUR_REPLIT_USERNAME.repl.co/
```
(or its authenticated version).

## 5. Further Configuration (Optional)

n8n supports various other configurations via environment variables (e.g., database, timezone, execution modes). Refer to the [official n8n documentation](https://docs.n8n.io/hosting/configuration/) for more advanced settings. Any such environment variables should also be managed as Replit Secrets.