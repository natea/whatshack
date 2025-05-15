"""
Township Connect - WhatsApp Assistant

Main entry point for the Township Connect WhatsApp Assistant application.
This module initializes the application and sets up the necessary components.
"""

import logging
from src.core_handler import handle_incoming_message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to initialize and run the Township Connect application.
    """
    logger.info("Starting Township Connect WhatsApp Assistant...")
    # Application initialization code will go here
    logger.info("Township Connect WhatsApp Assistant is running.")

if __name__ == "__main__":
    main()