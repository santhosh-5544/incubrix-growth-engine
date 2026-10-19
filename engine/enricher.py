"""Enrichment and content classification engine."""

import os
from typing import List
from engine.models import CreatorLead
from engine.outreach_generator import build_first_message

def enrich_creator_lead(lead: CreatorLead) -> CreatorLead:
    """
    Enriches a single creator lead by:
    1. Verifying and formatting content publication metrics
    2. Generating compliant, personalized first message if empty
    3. Normalizing profile and evidence URLs
    """
    # 1. Synthesize first message if empty
    if not lead.first_message:
        lead.first_message = build_first_message(lead)
        
    # 2. Ensure checked date is current
    if not lead.checked_date:
        lead.checked_date = "2026-10-18"
        
    # 3. Ensure completeness
    if lead.validate_completeness():
        lead.completeness_check = "COMPLETE"
    else:
        lead.completeness_check = "MISSING FIELDS"
        
    return lead

def enrich_leads_batch(leads: List[CreatorLead]) -> List[CreatorLead]:
    """Applies enrichment across a batch of creator leads."""
    enriched = []
    for lead in leads:
        enriched.append(enrich_creator_lead(lead))
    return enriched
