import logging
import os
import sys
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

def load_configuration(config: Dict[str, str]) -> Dict[str, str]:
    return config


CONFIG = {
    'LOG_LEVEL': logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO')),
    'PORT': os.environ.get('PORT', 5001),
    'CATALOG_DATA': os.environ.get('CATALOG_DATA', './data/data.csv'),
    'DATABASE': os.environ.get('DATABASE', 'postgresql://localhost:5432/allisone'),
}

# Parse keyvaults env var
CONFIG = load_configuration(CONFIG)
