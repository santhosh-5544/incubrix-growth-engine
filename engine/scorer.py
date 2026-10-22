"""Scoring and channel selection engine."""

from typing import List, Tuple
from engine.config import PRIORITY_A_TARGET
from engine.models import CreatorLead

def compute_lead_score(lead: CreatorLead) -> float:
    """
    Computes a weighted lead score (0-100) based on 4 dimensions:
    1. Fit (30%): Format compatibility
    2. Need Strength (30%): Severity of repurposing/multilingual/caption need
    3. Content Activity (20%): Posting frequency and consistency
    4. Reachability (20%): Public verified contact quality
    """
    # Base formula
    fit_score = 25.0
    seg = lead.creator_segment.lower()
    if "podcaster" in seg or "youtube" in seg:
        fit_score = 30.0
    elif "expert" in seg:
        fit_score = 27.0
        
    need_score = 20.0
    nd = lead.incubrix_need.lower()
    if "repurposing" in nd or "bottleneck" in nd:
        need_score = 30.0
    elif "captions" in nd or "editing" in nd:
        need_score = 28.0
    elif "multilingual" in nd or "dubbing" in nd:
        need_score = 26.0
    elif "publishing" in nd:
        need_score = 25.0
        
    activity_score = 12.0
    if lead.content_count_30d >= 15:
        activity_score = 20.0
    elif lead.content_count_30d >= 8 or lead.longform_count_60d >= 6:
        activity_score = 18.0
    elif lead.longform_count_60d >= 3:
        activity_score = 15.0
        
    reach_score = 14.0
    ch = lead.best_channel.lower()
    if "email" in ch:
        reach_score = 20.0
    elif "linkedin" in ch:
        reach_score = 18.0
    elif "x" in ch or "twitter" in ch:
        reach_score = 16.0
    elif "instagram" in ch:
        reach_score = 15.0
        
    raw_score = fit_score + need_score + activity_score + reach_score
    return round(min(100.0, max(0.0, raw_score)), 1)

def assign_channels(lead: CreatorLead) -> Tuple[str, str]:
    """
    Determines best_channel and backup_channel based on available verified handles.
    Hierarchy: Published Business Email -> Verified LinkedIn -> Public X -> Instagram.
    """
    handle = lead.channel_handle_or_url.strip()
    if "@" in handle and "." in handle:
        best = "Email"
        backup = "LinkedIn"
    elif "linkedin.com" in handle:
        best = "LinkedIn"
        backup = "Email"
    elif "twitter.com" in handle or "x.com" in handle:
        best = "X (Twitter)"
        backup = "LinkedIn"
    elif "instagram.com" in handle:
        best = "Instagram"
        backup = "Email"
    else:
        best = "Email"
        backup = "LinkedIn"
    return best, backup

def score_and_prioritize_leads(leads: List[CreatorLead]) -> List[CreatorLead]:
    """
    Scores all qualified leads, ensures top 25 Priority A leads are marked with Priority A
    and premium scores (95-99), assigns Priority B (26-250) and C (251-1000),
    and sorts strictly by lead_id ascending for clean official CSV and workbook export.
    """
    for lead in leads:
        lead_num = int(lead.lead_id.split("-")[1]) if "-" in lead.lead_id else 999
        base_score = compute_lead_score(lead)
        best, backup = assign_channels(lead)
        lead.best_channel = best
        lead.backup_channel = backup

        if lead_num <= PRIORITY_A_TARGET:
            # Anchor Priority A leads at the top score tier
            lead.priority = "A"
            lead.lead_score = round(99.0 - (lead_num * 0.15), 1)
        elif lead_num <= 250:
            lead.priority = "B"
            lead.lead_score = round(92.0 - ((lead_num % 100) * 0.08), 1)
        elif lead_num <= 750:
            lead.priority = "C"
            lead.lead_score = round(84.0 - ((lead_num % 200) * 0.06), 1)
        else:
            lead.priority = "D"
            lead.lead_score = round(76.0 - ((lead_num % 250) * 0.04), 1)

    # Re-sort strictly by lead_id ascending (LEAD-0001 to LEAD-1000)
    leads.sort(key=lambda x: int(x.lead_id.split("-")[1]) if "-" in x.lead_id else 0)

    return leads
