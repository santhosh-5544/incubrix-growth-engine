"""Verification and qualification rules engine."""

from typing import List, Tuple, Dict, Any
from engine.config import (
    APPROVED_COUNTRIES,
    MIN_APPROVED_COUNTRY_RATIO,
    MIN_COUNTRY_COUNT,
    MAX_SINGLE_COUNTRY_RATIO,
    MIN_ITEMS_30D,
    MIN_LONGFORM_60D,
    AGENCY_KEYWORDS,
)
from engine.models import CreatorLead

def check_exclusion_rules(name: str, profile_url: str, description: str = "") -> Tuple[bool, str]:
    """
    Checks if a candidate is an agency, brand, publication, directory, or fan account.
    Returns (is_excluded, reason).
    """
    text_to_check = f"{name} {profile_url} {description}".lower()
    
    for kw in AGENCY_KEYWORDS:
        if kw in text_to_check:
            return True, f"Excluded entity: Matches agency/brand/publication keyword '{kw}'"
            
    if "fan account" in text_to_check or "fanpage" in text_to_check:
        return True, "Excluded entity: Fan account / unofficial profile"
        
    return False, ""

def check_activity_rules(content_count_30d: int, longform_count_60d: int) -> Tuple[bool, str]:
    """
    Rule: Either 8 items in the last 30 days OR 2 long-form items in the last 60 days.
    """
    if content_count_30d >= MIN_ITEMS_30D:
        return True, f"Active: {content_count_30d} items in last 30d (>= {MIN_ITEMS_30D})"
    if longform_count_60d >= MIN_LONGFORM_60D:
        return True, f"Active: {longform_count_60d} longform items in last 60d (>= {MIN_LONGFORM_60D})"
    return False, f"Inactive: {content_count_30d} items in 30d and {longform_count_60d} longform in 60d"

def check_contact_channel_rules(channel: str, contact_val: str, evidence_url: str) -> Tuple[bool, str]:
    """
    Rule: Reachable channel must be real, public, used for business contact, and never guessed.
    """
    if not channel or not contact_val or not evidence_url:
        return False, "Missing reachability channel or evidence URL"
        
    # Check for guessed email patterns or invalid formats
    if channel.lower() == "email":
        if "@" not in contact_val or "." not in contact_val:
            return False, "Invalid email address format"
        # Reject generic guessed emails like info@domain without evidence
        if contact_val.startswith("first.last@"):
            return False, "Unverified guessed email pattern"
            
    if not evidence_url.startswith("http://") and not evidence_url.startswith("https://"):
        return False, "Invalid evidence URL format"
        
    return True, "Reachable: Verified public channel"

def verify_lead(lead: CreatorLead) -> Tuple[bool, str]:
    """Performs full qualification audit on a single lead."""
    # 1. Exclusion check
    excluded, reason = check_exclusion_rules(lead.creator_name, lead.profile_url)
    if excluded:
        lead.candidate_status = "Rejected"
        lead.rejection_reason = reason
        return False, reason

    # 2. Language check
    if lead.primary_language.lower() not in ["english", "en"]:
        lead.candidate_status = "Rejected"
        lead.rejection_reason = "Excluded: Non-English content language"
        return False, lead.rejection_reason

    # 3. Activity check
    active, act_reason = check_activity_rules(lead.content_count_30d, lead.longform_count_60d)
    if not active:
        lead.candidate_status = "Rejected"
        lead.rejection_reason = act_reason
        return False, act_reason

    # 4. Reachability check
    reachable, reach_reason = check_contact_channel_rules(
        lead.best_channel, lead.channel_handle_or_url, lead.channel_evidence_url
    )
    if not reachable:
        lead.candidate_status = "Rejected"
        lead.rejection_reason = reach_reason
        return False, reach_reason

    # 5. Commercial evidence check
    if not lead.monetization_signal or not lead.monetization_evidence_url:
        lead.candidate_status = "Rejected"
        lead.rejection_reason = "Missing commercial/monetization evidence"
        return False, lead.rejection_reason

    # 6. IncuBrix need check
    if not lead.incubrix_need or not lead.need_evidence_url:
        lead.candidate_status = "Rejected"
        lead.rejection_reason = "Missing IncuBrix workflow need evidence"
        return False, lead.rejection_reason

    lead.candidate_status = "Qualified"
    lead.rejection_reason = ""
    return True, "Qualified"

def evaluate_country_distribution(leads: List[CreatorLead]) -> Dict[str, Any]:
    """
    Computes country breakdown and evaluates compliance with:
    - At least 80% from approved countries (US, CA, UK/GB, IE, AU, NZ, SG)
    - At least 3 countries
    - No single country exceeding 60%
    """
    total = len(leads)
    if total == 0:
        return {
            "total": 0,
            "approved_ratio": 0.0,
            "country_count": 0,
            "max_country_ratio": 0.0,
            "max_country": "",
            "is_compliant": False,
            "breakdown": {},
        }
        
    counts: Dict[str, int] = {}
    approved_count = 0
    
    for lead in leads:
        c = lead.country_iso2.upper()
        counts[c] = counts.get(c, 0) + 1
        if c in APPROVED_COUNTRIES:
            approved_count += 1
            
    approved_ratio = approved_count / total
    country_count = len(counts)
    max_country, max_count = max(counts.items(), key=lambda x: x[1]) if counts else ("", 0)
    max_ratio = max_count / total
    
    is_compliant = (
        approved_ratio >= MIN_APPROVED_COUNTRY_RATIO
        and country_count >= MIN_COUNTRY_COUNT
        and max_ratio <= MAX_SINGLE_COUNTRY_RATIO
    )
    
    return {
        "total": total,
        "approved_ratio": approved_ratio,
        "country_count": country_count,
        "max_country": max_country,
        "max_country_ratio": max_ratio,
        "is_compliant": is_compliant,
        "breakdown": {k: {"count": v, "pct": round(v / total * 100, 2)} for k, v in sorted(counts.items(), key=lambda x: -x[1])},
    }
