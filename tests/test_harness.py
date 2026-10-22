"""Integration tests for pipeline harness execution modes."""

import pytest
from engine.harness import EngineHarness

def test_harness_failover_recovery():
    harness = EngineHarness(target_leads=50)
    summary = harness.run_pipeline(mode="fail-test")
    
    assert summary["mode"] == "fail-test"
    assert summary["status"] == "RECOVERED"
    assert summary["items_produced"] == 100
    assert summary["retries_handled"] == 3

def test_harness_small_run():
    harness = EngineHarness(target_leads=100, export=False)
    summary = harness.run_pipeline(mode="run")
    
    assert summary["mode"] == "run"
    assert summary["items_produced"] == 100
    assert summary["priority_a_count"] == 25
    assert summary["country_compliance"] is True
