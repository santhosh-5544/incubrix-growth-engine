"""Unit tests for outreach sequence generation and compliance."""

import pytest
from engine.models import CreatorLead
from engine.outreach_generator import (
    build_first_message,
    build_follow_up_1,
    build_follow_up_2,
    generate_segment_sequences,
    generate_priority_a_outreach,
)

@pytest.fixture
def test_lead():
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
        content_count_30d=9,
        longform_count_60d=18,
        monetization_signal="Course",
        monetization_evidence_url="https://pacademy.com/",
        incubrix_need="Shorts Repurposing Bottleneck",
        need_evidence_url="https://youtube.com/@aliabdaal/shorts",
        best_channel="Email",
        channel_handle_or_url="ali@aliabdaal.com",
        channel_evidence_url="https://aliabdaal.com/contact/",
        backup_channel="LinkedIn",
        personalization_hook="evidence-based productivity systems",
        first_message="",
        checked_date="2026-10-18",
        priority="A",
        lead_score=98.8,
        candidate_status="Qualified",
    )

def test_first_message_compliance(test_lead):
    msg = build_first_message(test_lead)
    
    # 1. Must mention specific content hook
    assert test_lead.personalization_hook in msg
    # 2. Must state who is sending
    assert "Santhosh" in msg
    assert "IncuBrix" in msg
    # 3. Must include opt-out
    assert "pass" in msg.lower() or "opt out" in msg.lower()
    # 4. Must tailor to need
    assert test_lead.incubrix_need in msg

def test_follow_ups_progression(test_lead):
    f1 = build_follow_up_1(test_lead)
    f2 = build_follow_up_2(test_lead)
    
    assert test_lead.personalization_hook in f1
    assert "not interested" in f1.lower() or "opt out" in f1.lower()
    
    assert "app.incubrix.com" in f2
    assert "300" in f2  # Mentions free trial credits

def test_segment_sequences_generation():
    seqs = generate_segment_sequences()
    assert len(seqs) >= 4
    assert "podcaster_email" in seqs
    assert "podcaster_linkedin" in seqs
    assert "youtuber_email" in seqs
    assert "expert_email" in seqs
