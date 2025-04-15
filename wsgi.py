# wsgi.py - Special file for Gunicorn on Render
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log current directory and files for debugging
logger.debug(f"Current working directory: {os.getcwd()}")
try:
    logger.debug(f"Directory contents: {os.listdir(os.getcwd())}")
except Exception as e:
    logger.error(f"Error listing directory: {e}")

# Import the Flask app
try:
    from app import app as application
    
    # Log all routes for debugging
    logger.debug("Registered routes:")
    for rule in application.url_map.iter_rules():
        logger.debug(f"Route: {rule}, Endpoint: {rule.endpoint}, Methods: {rule.methods}")
    
except Exception as e:
    logger.error(f"Error importing application: {e}")
    raise e

# This is needed for Gunicorn
app = application