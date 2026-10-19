"""Deduplication module for creator leads."""

import re
from typing import List, Tuple, Set
from engine.models import CreatorLead

def normalize_domain_or_handle(url_or_handle: str) -> str:
    """Normalizes URL, website domain, or social handle for duplicate detection."""
    if not url_or_handle:
        return ""
    text = url_or_handle.lower().strip()
    text = re.sub(r"^https?://(www\.)?", "", text)
    text = re.sub(r"/+$", "", text)
    text = re.sub(r"[?#].*$", "", text)
    return text

def normalize_name(name: str) -> str:
    """Normalizes creator or show name for soft duplicate matching."""
    if not name:
        return ""
    text = name.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text)

def deduplicate_leads(leads: List[CreatorLead]) -> Tuple[List[CreatorLead], int]:
    """
    Deduplicates creator leads across:
    1. Stable creator ID (e.g. YouTube channel ID, Apple podcast collection ID)
    2. Normalized primary profile / website URL
    3. Normalized creator name + country combination
    
    Returns:
        (unique_leads, duplicates_removed_count)
    """
    seen_ids: Set[str] = set()
    seen_urls: Set[str] = set()
    seen_names: Set[str] = set()
    
    unique_leads: List[CreatorLead] = []
    duplicates_count = 0
    
    for lead in leads:
        norm_id = lead.stable_creator_id.strip()
        norm_url = normalize_domain_or_handle(lead.profile_url)
        norm_name = f"{normalize_name(lead.creator_name)}::{lead.country_iso2}"
        
        is_dup = False
        if norm_id and norm_id in seen_ids:
            is_dup = True
        elif norm_url and norm_url in seen_urls:
            is_dup = True
        elif norm_name and norm_name in seen_names:
            is_dup = True
            
        if is_dup:
            duplicates_count += 1
            continue
            
        if norm_id:
            seen_ids.add(norm_id)
        if norm_url:
            seen_urls.add(norm_url)
        if norm_name:
            seen_names.add(norm_name)
            
        lead.duplicate_check = "UNIQUE"
        unique_leads.append(lead)
        
    return unique_leads, duplicates_count
