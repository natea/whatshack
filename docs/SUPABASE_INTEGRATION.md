# Supabase Integration and Verification

This document provides instructions for integrating and verifying the Supabase setup for the Township Connect WhatsApp Assistant.

## Prerequisites

- A Supabase project created in the `af-south-1` region
- Supabase credentials (URL, service key, and anon key)

## Step 1: Apply the Database Schema

The database schema needs to be applied to the Supabase project. This can be done using the Supabase Studio SQL Editor.

1. Log in to the Supabase dashboard and navigate to your project
2. Go to the SQL Editor
3. Copy the contents of the `supabase_schema.sql` file (or open the file directly)
4. Paste the SQL commands into the SQL Editor
5. Execute the SQL commands

The `supabase_schema.sql` file was generated using the `scripts/export_sql_for_supabase.py` script and contains all the necessary SQL commands to create the tables, indexes, RLS policies, and functions as specified in the requirements.

## Step 2: Set Environment Variables

The Supabase credentials need to be set as environment variables for the scripts and tests to use.

```bash
export SUPABASE_URL=https://your-project-id.supabase.co
export SUPABASE_SERVICE_KEY=your-service-key
export SUPABASE_ANON_KEY=your-anon-key
```

Alternatively, you can add these credentials to the `.env` file:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_ANON_KEY=your-anon-key
```

## Step 3: Run the Tests

Run the tests to verify the Supabase setup:

```bash
./scripts/run_supabase_tests.sh
```

This script will check if the environment variables are set and then run the tests to verify that the tables exist and are properly configured.

## Troubleshooting

If you encounter any issues, check the following:

- Make sure the Supabase project is created in the `af-south-1` region
- Make sure the Supabase credentials are correct
- Make sure the SQL commands were executed successfully in the Supabase Studio SQL Editor
- Make sure the environment variables are set correctly

## Next Steps

Once the Supabase integration and verification is complete, you can proceed with the next steps in the project, such as implementing the Core Message Handler.