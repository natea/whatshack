#!/bin/bash
# Script to run Supabase tests with environment variables set

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
pytest tests/test_supabase_setup.py -v