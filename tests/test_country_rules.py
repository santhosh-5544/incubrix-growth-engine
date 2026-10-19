"""Unit tests for country mix and qualification compliance."""

import pytest
from engine.collector import generate_leads_database
from engine.verifier import evaluate_country_distribution, check_activity_rules, check_exclusion_rules

def test_full_dataset_country_distribution():
    leads = generate_leads_database(target_count=1000)
    dist = evaluate_country_distribution(leads)
    
    assert dist["total"] == 1000
    # Rule 1: At least 80% from approved markets
    assert dist["approved_ratio"] >= 0.80, f"Approved ratio too low: {dist['approved_ratio']}"
    # Rule 2: At least 3 countries
    assert dist["country_count"] >= 3, f"Not enough countries: {dist['country_count']}"
    # Rule 3: No country may exceed 60%
    assert dist["max_country_ratio"] <= 0.60, f"Max country {dist['max_country']} exceeded 60%: {dist['max_country_ratio']}"
    # Combined flag
    assert dist["is_compliant"] is True

def test_check_activity_rules():
    # Active: >= 8 items in 30d
    valid_30d, _ = check_activity_rules(content_count_30d=8, longform_count_60d=1)
    assert valid_30d is True

    # Active: >= 2 longform in 60d
    valid_60d, _ = check_activity_rules(content_count_30d=1, longform_count_60d=2)
    assert valid_60d is True

    # Inactive
    inactive, _ = check_activity_rules(content_count_30d=7, longform_count_60d=1)
    assert inactive is False

def test_check_exclusion_rules():
    # Agency / brand exclusion
    is_ex1, reason1 = check_exclusion_rules("Apex Media Group", "https://apex.com")
    assert is_ex1 is True
    assert "agency/brand/publication" in reason1

    is_ex2, reason2 = check_exclusion_rules("BBC Technology News", "https://bbc.com")
    assert is_ex2 is True

    is_ex3, reason3 = check_exclusion_rules("Ali Abdaal Fanpage", "https://instagram.com/fan")
    assert is_ex3 is True

    # Legitimate creator
    is_ex4, _ = check_exclusion_rules("Ali Abdaal", "https://youtube.com/@aliabdaal")
    assert is_ex4 is False
