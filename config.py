"""
Shared configuration for Personal Agents Research Team.

This file contains common setup for model, database, and tools.
"""

import logging
import os
from typing import List, Any

from dotenv import load_dotenv
load_dotenv()

# Core Agno imports with error handling
AGNO_AVAILABLE = False
try:
    from agno.agent import Agent
    from agno.models.google import Gemini
    from agno.team import Team
    AGNO_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Core Agno components not available: {e}")
    Agent = None
    Gemini = None
    Team = None

# Optional DB import
MongoDb = None
if AGNO_AVAILABLE:
    try:
        from agno.db.mongo import MongoDb
    except ImportError as e:
        logging.warning(f"MongoDb not available (DB optional): {e}")
        MongoDb = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_db(db_url: str = None):
    """Get MongoDB database instance. Uses env DB_URL or default."""
    if db_url is None:
        db_url = os.getenv('DB_URL', 'mongodb://mongoadmin:secret@localhost:27017')
    
    if not MongoDb:
        logger.warning("MongoDb not available - install agno with DB support. Using no DB.")
        return None
    
    try:
        db = MongoDb(db_url=db_url)
        logger.info(f"MongoDB initialized with URL: {db_url}")
        return db
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB: {e}")
        return None


def check_agno_available():
    """Check if core Agno is available."""
    if not AGNO_AVAILABLE:
        raise ImportError("Core Agno framework is required. Install with: pip install agno")
    return True