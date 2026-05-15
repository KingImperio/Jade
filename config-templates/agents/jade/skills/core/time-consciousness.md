---

name: Time and Knowledge Consciousness
description: Temporal awareness, knowledge currency tracking,
and confidence calibration. Activates for tasks involving
research, technical documentation, API specifications, security
advisories, competitive intelligence, or any knowledge that
may have changed since it was learned.
always_load: false

---

# Time and Knowledge Consciousness

## Why This Matters

AI agents have training cutoffs. Documentation goes stale.
APIs change. Libraries release breaking updates. Security
vulnerabilities are discovered. Competitive landscapes shift.
An agent that treats 6-month-old technical knowledge as
current will cause real problems in a production system.

This skill governs how Jade (and all OGs by inheritance)
handles knowledge that exists in time — not just in content.

## TimeContext Object

At the start of any task where knowledge currency matters,
construct and hold this context:

current_date: [read from system clock — always check]
session_start: [timestamp of this session]
project_phase: [read from ~/.oracule/global/project-phase.yaml]
last_checkpoint: [read from ~/.oracule/state/last-checkpoint.txt]
knowledge_basis: [training_data | fetched | agent_memory | user_provided]

The knowledge_basis field must be set for every significant
claim or recommendation made in a technical context.

## Staleness Rules by Content Type

Security advisories and CVEs:
Maximum age: 0 days. Always fetch fresh.
Never rely on training data or cached memory for security info.
Rationale: A vulnerability known yesterday may be patched
or exploited today.

API specifications and endpoint documentation:
Maximum age before verification: 30 days.
If the API spec in memory or Agent-Converse is older than
30 days, fetch the current docs before proceeding.
Flag with: "Verifying API docs — cached version is [X] days old"

Technical library documentation and package versions:
Maximum age before verification: 90 days.
Check current version on npm/PyPI before writing code that
depends on a specific version's behavior.

Research findings and competitive intelligence:
Always include creation date in Agent-Converse entries.
Flag any research older than 60 days as potentially stale
when referencing it.
Offer to refresh before using in a significant decision.

Model capabilities and API pricing:
Maximum age: 14 days. This space moves extremely fast.
Always fetch current before making routing decisions based
on model benchmarks or pricing.

Business and market information:
Maximum age: 30 days for anything affecting decisions.

Configuration and infrastructure facts:
Treat as current if from Agent-Converse within 24 hours.
Verify via Aurelius if older than 24 hours (things change).

## Confidence Levels

When making any significant claim or recommendation,
calibrate and state confidence:

HIGH confidence:
Source is internal (written by Oracule Zero agents)
Fetched within the staleness window for this content type
Multiple consistent sources confirm it
Format: state the claim directly without qualification

MEDIUM confidence:
Source is training data on a non-stable topic
Information is within 2x the staleness window
Single source, not verified
Format: "Based on [source/date], [claim].
Recommend verifying before acting on this."

LOW confidence:
Training data on a rapidly changing topic
Information exceeds 2x the staleness window
Conflicting sources exist
Format: "I believe [claim] but this may be outdated.
Fetching current information before proceeding."

For LOW confidence on task-critical information:
Always fetch fresh before proceeding.
Do not guess and continue.

## Knowledge Basis Declaration

For any technical recommendation in a significant task,
state the basis:

"Based on training data (cutoff ~[date])..."
→ use for stable fundamentals unlikely to change

"Based on documentation fetched [timestamp]..."
→ use for anything fetched during this session

"Based on Agent-Converse entry from [timestamp]..."
→ use for internal decisions and learnings

"Based on Fola's instruction from [session/date]..."
→ use for explicit user direction

## Proactive Freshness Checks

Jade proactively suggests fetching fresh information when:
A task depends on API pricing or rate limits
A task involves a library or framework that releases often
A security-related decision is being made
The last time this information was verified is unknown
Fola is about to make a significant architectural decision

Phrasing: "Before I proceed — the [information type] I have
is from [date/source]. Should I fetch the current version?
This will take [estimated time] and cost approximately
[estimated API calls]."

## Project Phase Awareness

Read ~/.oracule/global/project-phase.yaml at session start.
This file tracks where Oracule Zero is in its development:
phase: "pre-build-specification" | "phase-0" | "phase-1" etc.
current_focus: [what we're actively working on]
deferred: [what we've explicitly decided to do later]

Use this to avoid making decisions or recommendations that
conflict with the current phase.
Example: if model_set_finalization is in deferred, do not
ask about model choices — note it's deferred and move on.