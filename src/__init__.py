"""
PDB — geopolitical intelligence monitoring and briefing system.
"""

from pathlib import Path
from dotenv import load_dotenv

# Load .env before any other imports that read environment variables
load_dotenv(Path(__file__).parent.parent / ".env")
