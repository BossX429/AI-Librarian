#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Librarian Configuration
Environment-based configuration for portable deployment
"""

import os
from pathlib import Path

# Base directories - use environment variables with fallbacks
AI_LIBRARIAN_HOME = Path(os.getenv(
    'AI_LIBRARIAN_HOME',
    r'C:\repos\AI-Librarian'
))

USER_HOME = Path(os.getenv('USERPROFILE', os.path.expanduser('~')))

# Component directories
LOGGER_DIR = AI_LIBRARIAN_HOME / "logger"
COMPRESSOR_DIR = AI_LIBRARIAN_HOME / "compressor"
CURATOR_DIR = AI_LIBRARIAN_HOME / "curator"
ORCHESTRATOR_DIR = AI_LIBRARIAN_HOME / "orchestrator"
QUERY_TOOLS_DIR = AI_LIBRARIAN_HOME / "query_tools"

# Data directories
RAW_LOGS_DIR = LOGGER_DIR / "raw_logs"
COMPRESSED_DIR = COMPRESSOR_DIR / "compressed"
PROCESSED_DIR = CURATOR_DIR / "processed"

# Database
DATABASE_PATH = PROCESSED_DIR / "conversations.db"

# Log files
LOGGER_LOG = LOGGER_DIR / "logger.log"
ORCHESTRATOR_LOG = ORCHESTRATOR_DIR / "orchestrator.log"

# Configuration parameters
DEFAULT_COMPRESSION_INTERVAL = int(os.getenv('AI_LIBRARIAN_COMPRESSION_INTERVAL', '300'))  # 5 minutes
DEFAULT_CHECK_INTERVAL = int(os.getenv('AI_LIBRARIAN_CHECK_INTERVAL', '30'))  # 30 seconds
DEFAULT_MIN_FILE_AGE = int(os.getenv('AI_LIBRARIAN_MIN_FILE_AGE', '60'))  # 60 seconds

# Ensure critical directories exist
def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        RAW_LOGS_DIR,
        COMPRESSED_DIR,
        PROCESSED_DIR,
        ORCHESTRATOR_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Display configuration (for debugging)
def show_config():
    """Print current configuration."""
    print("AI-Librarian Configuration")
    print("=" * 60)
    print(f"Home:           {AI_LIBRARIAN_HOME}")
    print(f"User Home:      {USER_HOME}")
    print(f"Database:       {DATABASE_PATH}")
    print(f"Raw Logs:       {RAW_LOGS_DIR}")
    print(f"Compressed:     {COMPRESSED_DIR}")
    print(f"Processed:      {PROCESSED_DIR}")
    print("=" * 60)
    print(f"Compression Interval: {DEFAULT_COMPRESSION_INTERVAL}s")
    print(f"Check Interval:       {DEFAULT_CHECK_INTERVAL}s")
    print(f"Min File Age:         {DEFAULT_MIN_FILE_AGE}s")
    print("=" * 60)

if __name__ == "__main__":
    show_config()
    ensure_directories()
    print("\nDirectories verified/created successfully!")
