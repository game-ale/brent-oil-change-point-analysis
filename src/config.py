import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data Paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
BRENT_PRICES_FILE = RAW_DATA_DIR / "BrentOilPrices.csv"
EVENTS_FILE = PROCESSED_DATA_DIR / "events.csv"

# Docs/Outputs
DOCS_DIR = PROJECT_ROOT / "docs"
IMAGES_DIR = DOCS_DIR / "images"
SUMMARY_FILE = DOCS_DIR / "eda_summary.txt"

# Ensure directories exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
