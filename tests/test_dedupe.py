"""Unit tests for deduplication module."""

import pytest
from engine.models import CreatorLead
from engine.dedupe import deduplicate_leads, normalize_domain_or_handle, normalize_name

def test_normalize_domain_or_handle():
    assert normalize_domain_or_handle("https://www.youtube.com/@mkbhd/") == "youtube.com/@mkbhd"
    assert normalize_domain_or_handle("http://aliabdaal.com/contact?ref=top") == "aliabdaal.com/contact"
    assert normalize_domain_or_handle("") == ""

def test_normalize_name():
    assert normalize_name("Ali Abdaal") == "ali abdaal"
    assert normalize_name("Colin & Samir!") == "colin samir"

def test_deduplicate_leads():
    lead1 = CreatorLead(
        lead_id="LEAD-0001",
        creator_name="Ali Abdaal",
        creator_segment="YouTuber",
        country_iso2="GB",
        primary_language="English",
        primary_platform="YouTube",
        profile_url="https://youtube.com/@aliabdaal",
        stable_creator_id="UCo_IB5145EVNcf8hw1Kku7w",
        followers_or_subscribers="5.8M",
        last_content_date="2026-10-14",
        recent_content_url="https://youtube.com/watch?v=test1",
        content_count_30d=10,
        longform_count_60d=20,
        monetization_signal="Course",
        monetization_evidence_url="https://pacademy.com",
        incubrix_need="Shorts Repurposing Bottleneck",
        need_evidence_url="https://youtube.com/@aliabdaal/shorts",
        best_channel="Email",
        channel_handle_or_url="ali@aliabdaal.com",
        channel_evidence_url="https://aliabdaal.com/contact",
        backup_channel="LinkedIn",
        personalization_hook="productivity frameworks",
        first_message="Hi Ali...",
        checked_date="2026-10-18",
        priority="A",
        lead_score=98.0,
        candidate_status="Qualified",
    )
    # Duplicate lead with same stable ID
    lead2 = CreatorLead(
        lead_id="LEAD-0002",
        creator_name="Ali Abdaal Secondary",
        creator_segment="YouTuber",
        country_iso2="GB",
        primary_language="English",
        primary_platform="YouTube",
        profile_url="https://youtube.com/@aliabdaal",
        stable_creator_id="UCo_IB5145EVNcf8hw1Kku7w",
        followers_or_subscribers="5.8M",
        last_content_date="2026-10-14",
        recent_content_url="https://youtube.com/watch?v=test2",
        content_count_30d=10,
        longform_count_60d=20,
        monetization_signal="Course",
        monetization_evidence_url="https://pacademy.com",
        incubrix_need="Shorts Repurposing Bottleneck",
        need_evidence_url="https://youtube.com/@aliabdaal/shorts",
        best_channel="Email",
        channel_handle_or_url="ali@aliabdaal.com",
        channel_evidence_url="https://aliabdaal.com/contact",
        backup_channel="LinkedIn",
        personalization_hook="productivity frameworks",
        first_message="Hi Ali...",
        checked_date="2026-10-18",
        priority="A",
        lead_score=98.0,
        candidate_status="Qualified",
    )
    # Distinct lead
    lead3 = CreatorLead(
        lead_id="LEAD-0003",
        creator_name="Lenny Rachitsky",
        creator_segment="Podcaster",
        country_iso2="US",
        primary_language="English",
        primary_platform="Apple Podcasts",
        profile_url="https://podcasts.apple.com/us/podcast/lennys/id1627920305",
        stable_creator_id="AP-1627920305",
        followers_or_subscribers="620k",
        last_content_date="2026-10-16",
        recent_content_url="https://lennysnewsletter.com/podcast",
        content_count_30d=8,
        longform_count_60d=16,
        monetization_signal="Newsletter Subscription",
        monetization_evidence_url="https://lennysnewsletter.com",
        incubrix_need="Missing Video Captions & Retention Clips",
        need_evidence_url="https://youtube.com/@LennysPodcast",
        best_channel="LinkedIn",
        channel_handle_or_url="https://linkedin.com/in/lenny",
        channel_evidence_url="https://lennysnewsletter.com/about",
        backup_channel="Email",
        personalization_hook="growth loops",
        first_message="Hi Lenny...",
        checked_date="2026-10-18",
        priority="A",
        lead_score=97.0,
        candidate_status="Qualified",
    )

    unique_leads, dupes_removed = deduplicate_leads([lead1, lead2, lead3])
    assert dupes_removed == 1
    assert len(unique_leads) == 2
    assert unique_leads[0].stable_creator_id == "UCo_IB5145EVNcf8hw1Kku7w"
    assert unique_leads[1].stable_creator_id == "AP-1627920305"
