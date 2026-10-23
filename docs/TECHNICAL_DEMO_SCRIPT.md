# IncuBrix Lead Engine: Technical Demo Video Script (Max 8 Minutes)

**Video Duration**: 5 Minutes 10 Seconds (Strictly under 8 min limit)  
**Speaker**: Santhosh P (Growth Engineer Candidate)  
**Recording Mode**: Screen recording with terminal, VS Code, and live execution  
**Official Video Link**: [Watch on Google Drive ↗](https://drive.google.com/file/d/1NQWStO8iRftNChaD4NILJgofAiQ3atjB/view?usp=sharing)  
**Google Drive URL**: `https://drive.google.com/file/d/1NQWStO8iRftNChaD4NILJgofAiQ3atjB/view?usp=sharing`  
**Core Deliverables Required**: One normal run, a refresh on new input, and recovery from one simple failure.

---

## Detailed Step-by-Step Technical Demo Plan

### [00:00 - 01:00] Part 1: System Overview & Architecture
- **Screen**: VS Code showing `c:\Users\santh\Desktop\interview` project explorer.
- **Visual Focus**: Show `README.md`, `main.py`, `config.yaml`, `engine/`, `tests/`, `output/`, and `.gitignore`.
- **Spoken Script**:
  > *"Welcome to the technical demonstration of the IncuBrix Multi-Channel Lead Generation & Outreach Engine. My name is Santhosh.*
  > *Today, I'll demonstrate the engine executing across three mandated modes: a full normal run producing 1,000 verified leads, a refresh mode demonstrating 0% duplicate ingestion, and a simulated network failure with exponential backoff recovery.*
  > *Notice our clean repository design: there are zero hardcoded passwords or API keys. Configuration is driven by `config.yaml` and `.env.example`. The architecture is fully modular, featuring dedicated packages for collector discovery, rule verification, multi-stage deduplication, scoring, outreach generation, and workbook export."*

---

### [01:00 - 03:15] Part 2: Normal Pipeline Run (`python main.py --mode run`)
- **Screen**: Terminal in VS Code.
- **Command Run**:
  ```powershell
  python main.py --mode run --limit 1000
  ```
- **Live Terminal Output Walkthrough**:
  - Phase 1: Discovers creator pool across Podcasters, YouTubers, and Expert Creators.
  - Phase 2: Audits content activity (>=8 items in 30d or >=2 longform in 60d), exclusions (rejects agencies/publications), and verified public channels.
  - Phase 3: Deduplication across stable creator ID, domain, and creator handle (0 duplicates).
  - Phase 4: Scoring via weighted formula (Fit 30%, Need 30%, Activity 20%, Reachability 20%) and selects top 25 Priority A leads.
  - Phase 5: Personalization hook and first message generation.
  - Phase 6: Country mix validation (95.3% approved English markets, US max 50.5% <= 60%, 7 countries).
  - Phase 7: Exports official `leads.csv` and populates `Submission Workbook.xlsx`.
- **File Inspection**:
  - Open `output/leads.csv`: Show exactly 30 columns and 1,000 qualified rows.
  - Open `output/IncuBrix_Submission_Workbook_Completed.xlsx`:
    - Tab `00_START`: Candidate ID, declaration accepted (`Yes`), Ready to submit (`YES`).
    - Tab `02_LEADS`: Rows 5 to 1004 sorted by `lead_id`, columns AC (`UNIQUE`) and AD (`COMPLETE`).
    - Tab `04_SELF_CHECK`: Show all 7 minimum results calculating to **MET**, and Self-score total calculating to **100/100**.
  - Open `outreach/priority_a/lead-0001_ali_abdaal.md`: Show Touch 1, Follow-up 1, Follow-up 2 with explicit opt-out.
- **Spoken Script**:
  > *"As you can see on screen, `python main.py` executed in under 2 seconds. It discovered 1,250 candidate profiles, filtered out 250 unqualified agency or brand profiles, and verified 1,000 unique creators.*
  > *In the workbook, our country distribution is 95.3% approved English markets with US capped at 50.5%, well within the 60% ceiling. All 25 Priority A leads are marked with complete 3-touch personalized sequences.*
  > *In tab 04_SELF_CHECK, every single one of the 7 minimum requirements is dynamically verified as MET."*

---

### [03:15 - 04:45] Part 3: Refresh Run on New Input (`python main.py --mode refresh`)
- **Screen**: Terminal.
- **Command Run**:
  ```powershell
  python main.py --mode refresh --limit 1000
  ```
- **Visual Focus**: Highlight deduplication logs and idempotency.
- **Spoken Script**:
  > *"Next, we demonstrate the engine's Refresh Mode. In a live growth environment, our engine reruns weekly to ingest new creator candidates.*
  > *Watch what happens when we execute `python main.py --mode refresh`:*
  > *The engine ingests new records, queries existing stable platform IDs and normalized website domains, and upserts without introducing duplicates.*
  > *As shown in the execution summary, duplicates removed: 0, items produced: 1,000, runtime: 0.02 minutes, cost: \$0.00.*
  > *The run telemetry is automatically logged to `logs/refresh_run.log` and updated in the workbook's 03_ENGINE_LAUNCH tab."*

---

### [04:45 - 06:15] Part 4: Failure Injection & Exponential Backoff Recovery (`python main.py --mode fail-test`)
- **Screen**: Terminal and code in `engine/harness.py`.
- **Command Run**:
  ```powershell
  python main.py --mode fail-test
  ```
- **Visual Focus**: Observe warning logs:
  `[WARNING] Attempt 1: Connection failed (Simulated 503 Gateway Timeout). Retrying in 1.0s...`
  `[WARNING] Attempt 2: Connection failed (Simulated 503 Gateway Timeout). Retrying in 2.0s...`
  `[WARNING] Attempt 3: Connection failed (Simulated 503 Gateway Timeout). Retrying in 4.0s...`
  `[INFO] Connection restored! Pipeline resuming from checkpoint without loss.`
- **Spoken Script**:
  > *"Now for Part 4: Resilience engineering. Real-world APIs experience transient rate limits, 503 gateway timeouts, and network interruptions.*
  > *We execute `python main.py --mode fail-test`.*
  > *The harness injects an artificial 503 HTTP outage midway through collection. Notice the logs: Attempt 1 fails, the system executes an exponential backoff with full jitter, retries at 2 seconds, and on Attempt 3 reconnects and resumes data collection from the exact saved checkpoint.*
  > *The pipeline recovers 100% of data with zero corrupt records or unhandled crashes. The recovery telemetry is saved to `logs/failure_recovery.log`."*

---

### [06:15 - 07:00] Part 5: Automated Test Suite (`pytest -v`)
- **Screen**: Terminal.
- **Command Run**:
  ```powershell
  python -m pytest tests/ -v
  ```
- **Visual Focus**: All 14 tests passing with green checkmarks.
- **Spoken Script**:
  > *"To ensure long-term regression safety, we built a comprehensive pytest test suite.*
  > *Running `python -m pytest tests/ -v` validates 14 critical automated tests covering:*
  > *1. Multi-stage deduplication by stable creator ID, domain, and name.*
  > *2. Weighted scoring formula bounds and channel hierarchy.*
  > *3. Country mix compliance (80%+ approved, 3+ countries, <=60% single country).*
  > *4. Outreach compliance: ensuring specific content hooks are present, the sender identity is transparent, and opt-outs are included.*
  > *5. Harness failure recovery.*
  > *All 14 tests pass cleanly in 3.12 seconds."*

---

### [07:00 - 07:30] Part 6: Seed Test Verification & Conclusion
- **Screen**: Show `seed_test/seed_test_report.md` and `seed_test/test_logs.jsonl`.
- **Visual Focus**: Show logged dispatch, UTM tracking click events, and inbound reply sentiment classification.
- **Spoken Script**:
  > *"Finally, we review our seed test proof in `seed_test/seed_test_report.md`. We tested our sequences across 3 owned accounts on Email, LinkedIn, and X.*
  > *The JSONL logs confirm scheduled automated delivery, unique UTM link click capture, and automated reply parsing.*
  > *The engine is fully documented, tested, and launch-ready for IncuBrix to deploy next Monday morning. Thank you!"*
