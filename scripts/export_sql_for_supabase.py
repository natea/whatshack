#!/usr/bin/env python3
"""
Script to export SQL commands for execution in Supabase Studio SQL Editor.

This script reads the SQL schema file and outputs the SQL commands that need to be
executed in the Supabase Studio SQL Editor to apply the schema and configure RLS.
"""

import os
import sys
import logging
import argparse
from pathlib import Path

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

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Export SQL commands for Supabase Studio SQL Editor')
    parser.add_argument('--schema', default='db_scripts/db_schema_v1.sql', help='Path to the schema file')
    parser.add_argument('--output', default='supabase_schema.sql', help='Path to the output file')
    args = parser.parse_args()
    
    schema_path = args.schema
    output_path = args.output
    
    try:
        # Read schema file
        schema_sql = read_schema_file(schema_path)
        if not schema_sql:
            logger.error(f"Failed to read schema file: {schema_path}")
            return 1
        
        # Write the SQL to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("-- Township Connect WhatsApp Assistant Database Schema\n")
            f.write("-- Execute this SQL in the Supabase Studio SQL Editor\n\n")
            f.write(schema_sql)
        
        logger.info(f"SQL commands exported to {output_path}")
        logger.info("Execute these SQL commands in the Supabase Studio SQL Editor to apply the schema and configure RLS.")
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())