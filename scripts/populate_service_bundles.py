#!/usr/bin/env python3
"""
Script to populate the service_bundles table in Supabase from JSON files.

This script reads service bundle definitions from JSON files in the data/service_bundles directory
and inserts or updates them in the service_bundles table in Supabase.
"""

import json
import os
import glob
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.supabase_client import get_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_service_bundles_from_json() -> List[Dict[str, Any]]:
    """
    Load service bundle definitions from JSON files.
    
    Returns:
        A list of service bundle dictionaries
    """
    bundles = []
    bundle_dir = Path("data/service_bundles")
    
    # Get all JSON files in the service_bundles directory
    json_files = glob.glob(str(bundle_dir / "*.json"))
    
    logger.info(f"Found {len(json_files)} service bundle JSON files")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                bundle_data = json.load(f)
                
                # Extract the core bundle data (exclude features for now)
                core_bundle_data = {
                    "bundle_id": bundle_data.get("bundle_id"),
                    "bundle_name_en": bundle_data.get("bundle_name_en"),
                    "bundle_name_xh": bundle_data.get("bundle_name_xh"),
                    "bundle_name_af": bundle_data.get("bundle_name_af"),
                    "description_en": bundle_data.get("description_en"),
                    "description_xh": bundle_data.get("description_xh"),
                    "description_af": bundle_data.get("description_af"),
                    "price_tier": bundle_data.get("price_tier", "free"),
                    "active": bundle_data.get("active", True)
                }
                
                bundles.append(core_bundle_data)
                logger.info(f"Loaded bundle: {core_bundle_data['bundle_id']}")
                
                # TODO: Handle features in a separate function
                
        except Exception as e:
            logger.error(f"Error loading bundle from {json_file}: {str(e)}")
    
    return bundles

def populate_service_bundles_table(client, bundles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Populate the service_bundles table with the provided bundles.
    
    Args:
        client: A Supabase client instance
        bundles: A list of service bundle dictionaries
        
    Returns:
        The result of the database operation
    """
    if not bundles:
        logger.warning("No bundles to populate")
        return {"data": [], "error": "No bundles to populate"}
    
    try:
        # Check if we're using the mock client
        if hasattr(client, '__class__') and client.__class__.__name__ == 'MockSupabaseClient':
            # Mock client doesn't have upsert, use insert instead
            result = client.table("service_bundles").insert(bundles).execute()
        else:
            # Real client - use upsert to insert or update bundles
            result = client.table("service_bundles").upsert(bundles).execute()
        
        logger.info(f"Successfully populated {len(bundles)} service bundles")
        return result
    except Exception as e:
        logger.error(f"Error populating service bundles: {str(e)}")
        return {"data": [], "error": str(e)}

def main():
    """Main function to run the script."""
    try:
        # Get Supabase client
        client = get_client()
        if not client:
            logger.error("Failed to get Supabase client")
            return
        
        # Load bundles from JSON files
        bundles = load_service_bundles_from_json()
        
        # Populate the service_bundles table
        result = populate_service_bundles_table(client, bundles)
        
        if result.get("error"):
            logger.error(f"Error: {result['error']}")
        else:
            logger.info(f"Successfully populated {len(result.get('data', []))} service bundles")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()