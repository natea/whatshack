#!/bin/bash
# Script to run Supabase tests with environment variables set

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check if environment variables are set
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_KEY" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "Error: SUPABASE_URL, SUPABASE_SERVICE_KEY, and SUPABASE_ANON_KEY environment variables must be set."
    echo "Please set these environment variables before running this script."
    echo "Example:"
    echo "  export SUPABASE_URL=https://your-project-id.supabase.co"
    echo "  export SUPABASE_SERVICE_KEY=your-service-key"
    echo "  export SUPABASE_ANON_KEY=your-anon-key"
    exit 1
fi

# Run the tests
echo "Running Supabase tests..."
python -m pytest tests/test_supabase_setup.py::test_users_table_exists tests/test_supabase_setup.py::test_service_bundles_table_exists tests/test_supabase_setup.py::test_message_logs_table_exists -v