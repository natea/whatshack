# Supabase MCP

## Getting Started with Supabase MCP

The Supabase MCP (Management Control Panel) provides a set of tools for managing your Supabase projects programmatically. This guide will help you use these tools effectively.

### How to Use MCP Services

1. **Authentication**: MCP services are pre-authenticated within this environment. No additional login is required.

2. **Basic Workflow**:
   - Start by listing projects (`list_projects`) or organizations (`list_organizations`)
   - Get details about specific resources using their IDs
   - Always check costs before creating resources
   - Confirm costs with users before proceeding
   - Use appropriate tools for database operations (DDL vs DML)
--remote-debugging-port=9222
3. **Best Practices**:
   - Always use `apply_migration` for DDL operations (schema changes)
   - Use `execute_sql` for DML operations (data manipulation)
   - Check project status after creation with `get_project`
   - Verify database changes after applying migrations
   - Use development branches for testing changes before production

4. **Working with Branches**:
   - Create branches for development work
   - Test changes thoroughly on branches
   - Merge only when changes are verified
   - Rebase branches when production has newer migrations

5. **Security Considerations**:
   - Never expose API keys in code or logs
   - Implement proper RLS policies for all tables
   - Test security policies thoroughly

### Current Project

```json
{"id":"replace_with_your","organization_id":"replace_with_your","name":"replace_with_your-v2","region":"us-west-1","created_at":"2025-04-22T17:22:14.786709Z","status":"ACTIVE_HEALTHY"}
```

## Available Commands

### Project Management

#### `list_projects`
Lists all Supabase projects for the user.

#### `get_project`
Gets details for a Supabase project.

**Parameters:**
- `id`* - The project ID

#### `get_cost`
Gets the cost of creating a new project or branch. Never assume organization as costs can be different for each.

**Parameters:**
- `type`* - No description
- `organization_id`* - The organization ID. Always ask the user.

#### `confirm_cost`
Ask the user to confirm their understanding of the cost of creating a new project or branch. Call `get_cost` first. Returns a unique ID for this confirmation which should be passed to `create_project` or `create_branch`.

**Parameters:**
- `type`* - No description
- `recurrence`* - No description
- `amount`* - No description

#### `create_project`
Creates a new Supabase project. Always ask the user which organization to create the project in. The project can take a few minutes to initialize - use `get_project` to check the status.

**Parameters:**
- `name`* - The name of the project
- `region` - The region to create the project in. Defaults to the closest region.
- `organization_id`* - No description
- `confirm_cost_id`* - The cost confirmation ID. Call `confirm_cost` first.

#### `pause_project`
Pauses a Supabase project.

**Parameters:**
- `project_id`* - No description

#### `restore_project`
Restores a Supabase project.

**Parameters:**
- `project_id`* - No description

#### `list_organizations`
Lists all organizations that the user is a member of.

#### `get_organization`
Gets details for an organization. Includes subscription plan.

**Parameters:**
- `id`* - The organization ID

### Database Operations

#### `list_tables`
Lists all tables in a schema.

**Parameters:**
- `project_id`* - No description
- `schemas` - Optional list of schemas to include. Defaults to all schemas.

#### `list_extensions`
Lists all extensions in the database.

**Parameters:**
- `project_id`* - No description

#### `list_migrations`
Lists all migrations in the database.

**Parameters:**
- `project_id`* - No description

#### `apply_migration`
Applies a migration to the database. Use this when executing DDL operations.

**Parameters:**
- `project_id`* - No description
- `name`* - The name of the migration in snake_case
- `query`* - The SQL query to apply

#### `execute_sql`
Executes raw SQL in the Postgres database. Use `apply_migration` instead for DDL operations.

**Parameters:**
- `project_id`* - No description
- `query`* - The SQL query to execute

### Monitoring & Utilities

#### `get_logs`
Gets logs for a Supabase project by service type. Use this to help debug problems with your app. This will only return logs within the last minute. If the logs you are looking for are older than 1 minute, re-run your test to reproduce them.

**Parameters:**
- `project_id`* - No description
- `service`* - The service to fetch logs for

#### `get_project_url`
Gets the API URL for a project.

**Parameters:**
- `project_id`* - No description

#### `get_anon_key`
Gets the anonymous API key for a project.

**Parameters:**
- `project_id`* - No description

#### `generate_typescript_types`
Generates TypeScript types for a project.

**Parameters:**
- `project_id`* - No description

### Development Branches

#### `create_branch`
Creates a development branch on a Supabase project. This will apply all migrations from the main project to a fresh branch database. Note that production data will not carry over. The branch will get its own project_id via the resulting project_ref. Use this ID to execute queries and migrations on the branch.

**Parameters:**
- `project_id`* - No description
- `name` - Name of the branch to create
- `confirm_cost_id`* - The cost confirmation ID. Call `confirm_cost` first.

#### `list_branches`
Lists all development branches of a Supabase project. This will return branch details including status which you can use to check when operations like merge/rebase/reset complete.

**Parameters:**
- `project_id`* - No description

#### `delete_branch`
Deletes a development branch.

**Parameters:**
- `branch_id`* - No description

#### `merge_branch`
Merges migrations and edge functions from a development branch to production.

**Parameters:**
- `branch_id`* - No description

#### `reset_branch`
Resets migrations of a development branch. Any untracked data or schema changes will be lost.

**Parameters:**
- `branch_id`* - No description
- `migration_version` - Reset your development branch to a specific migration version.

#### `rebase_branch`
Rebases a development branch on production. This will effectively run any newer migrations from production onto this branch to help handle migration drift.

**Parameters:**
- `branch_id`* - No description
