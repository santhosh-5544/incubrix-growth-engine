"""Unit tests for scoring and channel selection module."""

import pytest
from engine.models import CreatorLead
from engine.scorer import compute_lead_score, assign_channels, score_and_prioritize_leads

@pytest.fixture
def sample_lead():
    return CreatorLead(
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
        recent_content_url="https://youtube.com/watch?v=kYv_3j3i5hM",
        content_count_30d=10,
        longform_count_60d=20,
        monetization_signal="Course",
        monetization_evidence_url="https://pacademy.com/",
        incubrix_need="Shorts Repurposing Bottleneck",
        need_evidence_url="https://youtube.com/@aliabdaal/shorts",
        best_channel="Email",
        channel_handle_or_url="ali@aliabdaal.com",
        channel_evidence_url="https://aliabdaal.com/contact/",
        backup_channel="LinkedIn",
        personalization_hook="evidence-based productivity",
        first_message="",
        checked_date="2026-10-18",
        priority="A",
        lead_score=0.0,
        candidate_status="Qualified",
    )

def test_compute_lead_score_bounds(sample_lead):
    score = compute_lead_score(sample_lead)
    assert 0.0 <= score <= 100.0
    assert score >= 90.0  # High fit, high need, active, email reachability

def test_assign_channels_hierarchy():
    # 1. Email
    l_email = CreatorLead(
        lead_id="L1", creator_name="T1", creator_segment="YouTuber", country_iso2="US",
        primary_language="English", primary_platform="YouTube", profile_url="", stable_creator_id="1",
        followers_or_subscribers="10k", last_content_date="", recent_content_url="",
        content_count_30d=10, longform_count_60d=10, monetization_signal="Sponsor",
        monetization_evidence_url="http://x", incubrix_need="Need", need_evidence_url="http://x",
        best_channel="", channel_handle_or_url="contact@creator.com", channel_evidence_url="http://x",
        backup_channel="", personalization_hook="", first_message="", checked_date="", priority="C",
        lead_score=80.0, candidate_status="Qualified"
    )
    best, backup = assign_channels(l_email)
    assert best == "Email"
    assert backup == "LinkedIn"

    # 2. LinkedIn
    l_li = CreatorLead(
        lead_id="L2", creator_name="T2", creator_segment="Expert-Led Creator", country_iso2="US",
        primary_language="English", primary_platform="LinkedIn", profile_url="", stable_creator_id="2",
        followers_or_subscribers="10k", last_content_date="", recent_content_url="",
        content_count_30d=10, longform_count_60d=10, monetization_signal="Course",
        monetization_evidence_url="http://x", incubrix_need="Need", need_evidence_url="http://x",
        best_channel="", channel_handle_or_url="https://linkedin.com/in/creatorprofile", channel_evidence_url="http://x",
        backup_channel="", personalization_hook="", first_message="", checked_date="", priority="C",
        lead_score=80.0, candidate_status="Qualified"
    )
    best, backup = assign_channels(l_li)
    assert best == "LinkedIn"
    assert backup == "Email"

def test_score_and_prioritize_leads():
    leads = []
    for i in range(1, 35):
        leads.append(CreatorLead(
            lead_id=f"LEAD-{i:04d}", creator_name=f"Creator {i}", creator_segment="YouTuber", country_iso2="US",
            primary_language="English", primary_platform="YouTube", profile_url=f"http://c{i}.com", stable_creator_id=f"ID-{i}",
            followers_or_subscribers="100k", last_content_date="2026-10-15", recent_content_url="http://x",
            content_count_30d=10, longform_count_60d=15, monetization_signal="Sponsor",
            monetization_evidence_url="http://x", incubrix_need="Shorts Repurposing Bottleneck", need_evidence_url="http://x",
            best_channel="Email", channel_handle_or_url=f"contact@c{i}.com", channel_evidence_url="http://x",
            backup_channel="LinkedIn", personalization_hook="hook", first_message="", checked_date="2026-10-18",
            priority="C", lead_score=0.0, candidate_status="Qualified"
        ))

    scored = score_and_prioritize_leads(leads)
    assert len(scored) == 34
    
    # Check that first 25 are Priority A
    priority_a_leads = [l for l in scored if l.priority == "A"]
    assert len(priority_a_leads) == 25
    for l in priority_a_leads:
        assert l.lead_score >= 95.0
        
    # Check that sorting is strictly by lead_id ascending
    assert scored[0].lead_id == "LEAD-0001"
    assert scored[24].lead_id == "LEAD-0025"
    assert scored[25].lead_id == "LEAD-0026"
    assert scored[25].priority == "B"
