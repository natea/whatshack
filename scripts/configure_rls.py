#!/usr/bin/env python3
"""
Script to configure Row-Level Security (RLS) on Supabase tables.

This script enables RLS on the specified tables and creates policies to restrict
access to a user's own data. It's designed to be run after the schema has been applied.
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

def enable_rls_on_table(table_name):
    """
    Enable Row-Level Security on a table.
    
    Args:
        table_name: The name of the table to enable RLS on
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # SQL to enable RLS on the table
        sql = f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;"
        success, result = execute_sql(sql)
        
        if not success:
            logger.error(f"Error enabling RLS on {table_name}: {result}")
            return False
            
        logger.info(f"RLS enabled on {table_name}")
        return True
    except Exception as e:
        logger.error(f"Error enabling RLS on {table_name}: {str(e)}")
        return False

def create_rls_policy(table_name, policy_name, using_clause):
    """
    Create an RLS policy on a table.
    
    Args:
        table_name: The name of the table to create the policy on
        policy_name: The name of the policy
        using_clause: The USING clause for the policy
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # SQL to create the policy
        sql = f"""
        CREATE POLICY {policy_name} ON {table_name}
            USING ({using_clause});
        """
        success, result = execute_sql(sql)
        
        if not success:
            logger.error(f"Error creating policy {policy_name} on {table_name}: {result}")
            return False
            
        logger.info(f"Policy {policy_name} created on {table_name}")
        return True
    except Exception as e:
        logger.error(f"Error creating policy {policy_name} on {table_name}: {str(e)}")
        return False

def check_rls_enabled(table_name):
    """
    Check if RLS is enabled on a table.
    
    Args:
        table_name: The name of the table to check
        
    Returns:
        True if RLS is enabled, False otherwise
    """
    try:
        # SQL to check if RLS is enabled
        sql = f"""
        SELECT relrowsecurity FROM pg_class
        WHERE oid = '{table_name}'::regclass;
        """
        success, result = execute_sql(sql)
        
        if not success:
            logger.error(f"Error checking RLS on {table_name}: {result}")
            return False
            
        if not result or not result[0][0]:
            logger.warning(f"RLS is not enabled on {table_name}")
            return False
            
        logger.info(f"RLS is enabled on {table_name}")
        return True
    except Exception as e:
        logger.error(f"Error checking RLS on {table_name}: {str(e)}")
        return False

def configure_all_rls():
    """
    Configure RLS on all relevant tables.
    
    Returns:
        True if successful, False otherwise
    """
    # Tables that need RLS
    tables = ['users', 'message_logs', 'security_logs']
    success = True
    
    for table in tables:
        # Enable RLS on the table
        if not enable_rls_on_table(table):
            success = False
            continue
        
        # Create the appropriate policy based on the table
        if table == 'users':
            policy_name = 'users_isolation_policy'
            using_clause = "whatsapp_id = current_setting('app.current_user_id', TRUE)::TEXT"
        else:
            policy_name = f"{table}_isolation_policy"
            using_clause = "user_whatsapp_id = current_setting('app.current_user_id', TRUE)::TEXT"
        
        if not create_rls_policy(table, policy_name, using_clause):
            success = False
    
    return success

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Configure Row-Level Security on Supabase tables')
    parser.add_argument('--table', help='Specific table to configure RLS on')
    parser.add_argument('--check-only', action='store_true', help='Only check if RLS is enabled, don\'t configure it')
    args = parser.parse_args()
    
    try:
        if args.check_only:
            # Check if RLS is enabled on the specified table or all tables
            if args.table:
                if check_rls_enabled(args.table):
                    logger.info(f"RLS is enabled on {args.table}")
                else:
                    logger.warning(f"RLS is not enabled on {args.table}")
                    return 1
            else:
                all_enabled = True
                for table in ['users', 'message_logs', 'security_logs']:
                    if not check_rls_enabled(table):
                        all_enabled = False
                
                if all_enabled:
                    logger.info("RLS is enabled on all tables")
                else:
                    logger.warning("RLS is not enabled on all tables")
                    return 1
        else:
            # Configure RLS on the specified table or all tables
            if args.table:
                if enable_rls_on_table(args.table):
                    logger.info(f"RLS configured on {args.table}")
                else:
                    logger.error(f"Failed to configure RLS on {args.table}")
                    return 1
            else:
                if configure_all_rls():
                    logger.info("RLS configured on all tables")
                else:
                    logger.error("Failed to configure RLS on all tables")
                    return 1
        
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())