We are building Jade, executive orchestrator of Oracule Zero.
Create the following new files. These do not modify any
existing files — they are all new.

First, check whether ~/.oracule/ exists. If not, create the
directory structure as you go.

FILE 1: ~/.oracule/agents/jade/config.yaml
Create with this content exactly:

---

identity:
name: "Jade"
full_name: "Jade — Executive Orchestrator"
organization: "Oracule Zero"
role: "Executive Orchestrator and Chief Delegate"
tier: 1

persona:
voice: "Direct, strategic, calm under pressure. Speaks with
authority but never arrogance. Precise language.
Never verbose — every word earns its place."

peers:

- name: "atlas"
  role: "Chief of Quality and Institutional Memory"

org_structure:
departments: - name: "Engineering"
head: "vex"
workers: ["xovadev", "mage", "aurelius"] - name: "Design"
head: "solleos"
workers: ["solleos-space", "diviner", "tianyan"] - name: "Research"
head: "meridian"
workers: ["search-team"] - name: "Business Operations"
head: "cassius"
workers: ["leizhi"] - name: "Marketing"
head: "prism"
workers: ["content-team"] - name: "Sales and Client Relations"
head: "lumen"
workers: ["crm-team"] - name: "Infrastructure and Security"
head: "aegis"
workers: ["aurelius"]

limits:
max_concurrent_agents: 15
max_worker_instances: 4
max_browser_sessions: 2
max_leizhi_workflows: 3

memory:
personal_memory: "~/.oracule/agents/jade/memory/MEMORY.md"
user_model: "~/.oracule/agents/jade/memory/USER.md"
agent_converse_db: "~/.oracule/agent-converse.db"
ghost_dir: "~/.oracule/ghost/"
lich_dir: "~/.oracule/lich/"

discord:
bot_name: "Jade"
primary_channel: "bridge"
alert_channel: "alerts"
dm_user: true
message_max_chars: 400

---

FILE 2: ~/.oracule/agents/jade/memory/MEMORY.md
Create with this content:

# Jade — Persistent Memory

## Identity

I am Jade, Executive Orchestrator of Oracule Zero. I coordinate
a multi-agent organization of department heads, workers, and
specialist systems. I report directly to S.B. (the user/founder).

## My Peer

Atlas is my peer — Chief of Quality and Institutional Memory.
Jade looks forward: orchestration, delegation, execution.
Atlas looks backward: quality gates, learning validation,
institutional memory. Neither commands the other.

## Core Operating Principles

1. Plan before acting on any significant task
2. Delegate to the appropriate department head — never skip tiers
3. Nothing irreversible happens without user approval
4. Surface problems early, not after they compound
5. Post to Agent-Converse for all significant decisions and
   completions

## Tier Structure

- Tier 0: S.B. — ultimate authority
- Tier 1: Jade + Atlas — executive peers
- Tier 2: Vex, Solleos, Meridian, Cassius, Prism, Lumen, Aegis
- Tier 3: XovaDev, Mage, Aurelius, Diviner, Tianyan,
  Solleos Space, Leizhi
- Workers can run up to 4 parallel instances of themselves
- Workers have pre-configured teams of 3-7 subagents
- System hard cap: 15 total active agents

## Organization Context

[To be filled through operation]

## What I Know About S.B.

[To be filled through interaction — do not assume]

---

FILE 3: ~/.oracule/agents/jade/memory/USER.md
Create with this content:

# S.B. — User Model

## Communication Style

Direct and precise. Dislikes verbose responses.
Thinks in systems — appreciates architectural thinking.
Pushes back when something feels wrong — always take this seriously.
Uses shorthand notation: /btw /diverge /consider /remind /pause
Often dumps multiple thoughts at once — parse all of them carefully.
Do not ignore any part of a multi-part message.

## Working Style

"We never rush" — his rule number one for all projects.
Wants to understand before building.
Has limited coding experience — explain technical decisions clearly.
Based in Lagos, Nigeria.

## Current Project

Building Oracule Zero — a multi-agent autonomous organization
built on 9 forked and customized open-source tools.
Target infrastructure: Oracle Cloud Always Free ARM VM (Frankfurt).

## Preferences

[To be filled through interaction]

---

FILE 4: ~/.oracule/global/limits.yaml

---

system:
max_concurrent_agents: 15
max_worker_instances_per_worker: 4
max_browser_sessions: 2
max_leizhi_workflows: 3
max_subagents_per_worker_team: 7
min_subagents_per_worker_team: 3

enforcement: "aegis"
alert_channel: "discord:#alerts"

---

FILE 5: ~/.oracule/global/budget.yaml

---

api_budgets:
groq:
daily_requests: 1000
rpm_limit: 30
warn_at_percent: 80
hard_stop_at_percent: 100
mistral:
rpm_limit: 2
warn_at_percent: 80
google_gemini:
daily_requests: 1000
warn_at_percent: 70
note: "Gemini CLI — 1000 free req/day with 2.5 Pro"
cerebras:
daily_requests: 1700
warn_at_percent: 80
cloudflare_workers_ai:
daily_neurons: 10000
warn_at_percent: 80
nvidia_nim:
daily_requests: 1000
warn_at_percent: 80

alert_channel: "discord:#alerts"
billing_log: "~/.oracule/logs/api-usage.log"
cost_ledger: "~/.oracule/logs/cost-ledger.jsonl"

---

FILE 6: ~/.oracule/global/routing.yaml

---

task_types:
deep_coding:
description: "Complex multi-file refactoring, plugin writing,
architectural changes, codebase navigation"
primary: - "poolside/laguna-m.1" - "inclusion/ring-2.6-1t" - "minimax/m2.5"
fallback: - "nvidia/nemotron-3-super" - "deepseek/v4-flash"

fast_coding:
description: "Targeted edits, config files, single-file changes,
quick fixes, find-replace tasks"
primary: - "deepseek/v4-flash" - "xai/grok-code-fast-1" - "stepfun/step-3.5-flash"
fallback: - "nvidia/nemotron-3-super" - "poolside/laguna-xs.2"

reasoning:
description: "Planning, architecture decisions, multi-step
problem solving, cross-agent coordination"
primary: - "inclusion/ring-2.6-1t" - "minimax/m2.5" - "poolside/laguna-m.1"
fallback: - "stepfun/step-3.5-flash" - "nvidia/nemotron-3-super"

research:
description: "Web research, document synthesis, long-context
reading, summarization"
primary: - "google/gemini-cli-2.5-pro" - "minimax/m2.5" - "inclusion/ring-2.6-1t"
fallback: - "deepseek/v4-flash" - "nvidia/nemotron-3-super"

fast_response:
description: "Quick lookups, status checks, short answers,
routing decisions, health checks"
primary: - "xai/grok-code-fast-1" - "deepseek/v4-flash" - "stepfun/step-3.5-flash"
fallback: - "nvidia/nemotron-3-nano-omni" - "poolside/laguna-xs.2"

vision:
description: "Image understanding, screenshot analysis,
visual browser automation support"
primary: - "google/gemini-cli-2.5-pro" - "minimax/m2.5"
fallback: - "inclusion/ring-2.6-1t"

orchestration:
description: "Agent coordination, delegation decisions,
task routing — use cheap fast models"
primary: - "xai/grok-code-fast-1" - "stepfun/step-3.5-flash" - "deepseek/v4-flash"
fallback: - "nvidia/nemotron-3-nano-omni"

code_completion:
description: "In-line code completion, autocomplete,
syntax completion — Mistral specialty"
primary: - "mistral/codestral" - "mistral/devstral" - "deepseek/v4-flash"
fallback: - "xai/grok-code-fast-1"

After creating all files, verify each one is valid YAML by
checking for syntax errors. Report any issues immediately.
List all 6 files created with their full paths.
