#!/usr/bin/env python3
"""
Script to apply the database schema to Supabase.

This script reads the SQL schema file and executes it against the Supabase database.
It uses the Supabase client to execute the SQL commands.
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.supabase_client import get_client, execute_sql

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_schema_file(schema_path):
    """
    Read the SQL schema file.
    
    Args:
        schema_path: Path to the schema file
        
    Returns:
        The content of the schema file as a string
    """
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading schema file: {str(e)}")
        return None

def apply_schema(schema_sql):
    """
    Apply the schema to the Supabase database.
    
    Args:
        schema_sql: The SQL schema to apply
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Execute the SQL schema directly using PostgreSQL connection
        success, result = execute_sql(schema_sql)
        
        if not success:
            logger.error(f"Error applying schema: {result}")
            return False
            
        logger.info("Schema applied successfully")
        return True
    except Exception as e:
        logger.error(f"Error applying schema: {str(e)}")
        return False

def check_rls():
    """
    Check if Row-Level Security (RLS) is enabled on the users table.
    
    Returns:
        True if RLS is enabled, False otherwise
    """
    try:
        # SQL to check if RLS is enabled on the users table
        sql = """
        SELECT relrowsecurity FROM pg_class
        WHERE oid = 'users'::regclass;
        """
        success, result = execute_sql(sql)
        
        if not success:
            logger.error(f"Error checking RLS: {result}")
            return False
            
        if not result or not result[0][0]:
            logger.warning("RLS is not enabled on the users table")
            return False
            
        logger.info("RLS is properly configured")
        return True
    except Exception as e:
        logger.error(f"Error checking RLS: {str(e)}")
        return False

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Apply database schema to Supabase')
    parser.add_argument('--schema', default='db_scripts/db_schema_v1.sql', help='Path to the schema file')
    parser.add_argument('--check-only', action='store_true', help='Only check if RLS is properly configured, don\'t apply schema')
    args = parser.parse_args()
    
    schema_path = args.schema
    check_only = args.check_only
    
    try:
        if check_only:
            # Only check RLS configuration
            if check_rls():
                logger.info("RLS is properly configured")
                return 0
            else:
                logger.error("RLS is not properly configured")
                return 1
        
        # Read schema file
        schema_sql = read_schema_file(schema_path)
        if not schema_sql:
            logger.error(f"Failed to read schema file: {schema_path}")
            return 1
        
        # Apply schema
        if not apply_schema(schema_sql):
            logger.error("Failed to apply schema")
            return 1
        
        # Check RLS configuration
        if not check_rls():
            logger.warning("RLS might not be properly configured")
        
        logger.info("Schema application completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())