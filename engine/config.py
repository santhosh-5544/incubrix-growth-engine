"""Configuration loader and constants for IncuBrix Lead Generation Engine."""

import os
from pathlib import Path
from typing import Any, Dict, List
import yaml
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CONFIG_PATH = BASE_DIR / "config.yaml"

def load_config() -> Dict[str, Any]:
    """Loads configuration from YAML with sensible fallbacks."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

CFG = load_config()

# Approved markets
APPROVED_COUNTRIES: List[str] = CFG.get("compliance", {}).get(
    "approved_countries", ["US", "GB", "CA", "AU", "SG", "IE", "NZ"]
)
MIN_APPROVED_COUNTRY_RATIO: float = CFG.get("compliance", {}).get("min_approved_country_ratio", 0.80)
MIN_COUNTRY_COUNT: int = CFG.get("compliance", {}).get("min_country_count", 3)
MAX_SINGLE_COUNTRY_RATIO: float = CFG.get("compliance", {}).get("max_single_country_ratio", 0.60)

# Activity requirements
MIN_ITEMS_30D: int = CFG.get("activity_rules", {}).get("min_items_last_30d", 8)
MIN_LONGFORM_60D: int = CFG.get("activity_rules", {}).get("min_longform_last_60d", 2)

# Exclusions
AGENCY_KEYWORDS: List[str] = CFG.get("exclusions", {}).get("agency_and_brand_keywords", [])

# Target limits
TARGET_LEADS: int = int(os.getenv("DEFAULT_LEAD_LIMIT", CFG.get("engine", {}).get("target_leads", 1000)))
PRIORITY_A_TARGET: int = int(os.getenv("PRIORITY_A_LIMIT", CFG.get("engine", {}).get("priority_a_target", 25)))

# Output paths
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "output")
LOG_DIR = BASE_DIR / os.getenv("LOG_DIR", "logs")
OUTREACH_DIR = BASE_DIR / "outreach"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
OUTREACH_DIR.mkdir(parents=True, exist_ok=True)

# 30 official workbook column headers in exact sequence
OFFICIAL_COLUMNS = [
    "lead_id",
    "creator_name",
    "creator_segment",
    "country_iso2",
    "primary_language",
    "primary_platform",
    "profile_url",
    "stable_creator_id",
    "followers_or_subscribers",
    "last_content_date",
    "recent_content_url",
    "content_count_30d",
    "longform_count_60d",
    "monetization_signal",
    "monetization_evidence_url",
    "incubrix_need",
    "need_evidence_url",
    "best_channel",
    "channel_handle_or_url",
    "channel_evidence_url",
    "backup_channel",
    "personalization_hook",
    "first_message",
    "checked_date",
    "priority",
    "lead_score",
    "candidate_status",
    "rejection_reason",
    "duplicate_check",
    "completeness_check",
]
