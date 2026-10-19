#!/usr/bin/env python3
"""
IncuBrix Multi-Channel Lead Generation and Outreach Engine
Entry point for automated discovery, qualification, deduplication, scoring, and outreach.

Usage:
    python main.py                  # Standard full run (1,000 qualified leads + workbook export)
    python main.py --mode repeat    # Fast cached rerun to verify idempotency
    python main.py --mode refresh   # Ingests and updates existing items with 0 duplicates
    python main.py --mode fail-test # Tests failure injection and retry recovery
"""

import argparse
import sys
from engine.harness import EngineHarness
from engine.config import TARGET_LEADS

def parse_args():
    parser = argparse.ArgumentParser(
        description="IncuBrix Multi-Channel Lead Generation & Outreach Engine",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["run", "repeat", "refresh", "fail-test"],
        default="run",
        help="Pipeline execution mode.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=TARGET_LEADS,
        help="Number of qualified leads to produce.",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    print("=" * 70)
    print("  IncuBrix Lead Generation & Outreach Engine v2.1.0")
    print(f"  Execution Mode: {args.mode.upper()} | Target Leads: {args.limit}")
    print("=" * 70)
    
    harness = EngineHarness(target_leads=args.limit)
    try:
        summary = harness.run_pipeline(mode=args.mode)
        print("\n" + "=" * 70)
        print("  PIPELINE EXECUTION SUMMARY")
        print("=" * 70)
        for k, v in summary.items():
            print(f"  - {k:<25}: {v}")
        print("=" * 70)
        print("  Status: SUCCESS | All deliverables produced.")
        print("=" * 70)
    except Exception as e:
        print(f"\n[ERROR] Pipeline encountered an unhandled exception: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
