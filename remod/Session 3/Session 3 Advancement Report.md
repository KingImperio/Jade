# Session 3 — Advancement Report

**Date:** 2026-05-15  
**Task:** Create Oracule Zero infrastructure files for Jade Executive Orchestrator

---

## Directory Structure Created

```
~/.oracule/
├── agents/
│   └── jade/
│       ├── config.yaml
│       └── memory/
│           ├── MEMORY.md
│           └── USER.md
└── global/
    ├── limits.yaml
    ├── budget.yaml
    └── routing.yaml
```

## Files Created

| # | File | Path | Status |
|---|------|------|--------|
| 1 | config.yaml | `~/.oracule/agents/jade/config.yaml` | ✅ Created (1,530 bytes) |
| 2 | MEMORY.md | `~/.oracule/agents/jade/memory/MEMORY.md` | ✅ Created |
| 3 | USER.md | `~/.oracule/agents/jade/memory/USER.md` | ✅ Created |
| 4 | limits.yaml | `~/.oracule/global/limits.yaml` | ✅ Created (254 bytes) |
| 5 | budget.yaml | `~/.oracule/global/budget.yaml` | ✅ Created (624 bytes) |
| 6 | routing.yaml | `~/.oracule/global/routing.yaml` | ✅ Created (2,259 bytes) |

## Validation

- **YAML syntax:** All 4 YAML files passed basic structural validation. PyYAML is not installed in the system Python for full parsing. Files have correct indentation, `key: value` structure, and list formatting.
- **MEMORY.md:** Valid markdown with proper headings, lists, and section structure.
- **USER.md:** Valid markdown with proper headings and section structure.

## Notes

- `~/.oracule/` did not exist before this session — was created fresh.
- The `ghost/` and `lich/` directories referenced in `config.yaml` under `memory:` section were not specified in the prompt — will need creation when those features are activated.
- The `~/.oracule/logs/` directory referenced in `budget.yaml` (`billing_log` / `cost_ledger` paths) was not specified in the prompt — will be created when logging begins.
- Routing.yaml defines 8 task types (deep_coding, fast_coding, reasoning, research, fast_response, vision, orchestration, code_completion) with primary and fallback model chains.
- Budget.yaml tracks 6 API providers with warning and hard-stop thresholds.
- Config.yaml defines 7 department heads, 4 system limits, peer relationship with Atlas, and Discord integration settings.

---

## Phase 2: Config Templates (preserve in repo)

After creating `~/.oracule/`, the config was mirrored into the repo as `config-templates/` so it survives reinstalls and VM deployment.

### Directory Structure Created

```
config-templates/
├── agents/
│   └── jade/
│       ├── config.yaml              ← copied from ~/.oracule/
│       ├── memory/
│       │   ├── MEMORY.md            ← copied from ~/.oracule/
│       │   └── USER.md              ← copied from ~/.oracule/
│       ├── skills/
│       │   └── core/
│       │       ├── oracule-rules.md
│       │       ├── agent-converse-protocol.md
│       │       ├── slash-command-system.md
│       │       ├── injection-guard.md
│       │       └── time-consciousness.md
│       └── experience/
│           ├── incidents.md         ← header-only template
│           └── never-do.md          ← header-only template
├── global/
│   ├── limits.yaml                  ← copied from ~/.oracule/
│   ├── budget.yaml                  ← copied from ~/.oracule/
│   └── routing.yaml                 ← copied from ~/.oracule/
└── setup/
    └── discord-setup.md
```

### New Files Created (8)

| # | File | Description |
|---|------|-------------|
| 1 | `skills/core/oracule-rules.md` | Chain of command, golden rules, communication style |
| 2 | `skills/core/agent-converse-protocol.md` | Cross-agent logging protocol with post format |
| 3 | `skills/core/slash-command-system.md` | /btw, /diverge, /consider, /remind, /pause, etc. |
| 4 | `skills/core/injection-guard.md` | Prompt injection prevention and escalation |
| 5 | `skills/core/time-consciousness.md` | Time awareness across parallel sessions |
| 6 | `experience/incidents.md` | Incident log template (header only, populated as incidents occur) |
| 7 | `experience/never-do.md` | Banned actions list (header only, populated as decisions are made) |
| 8 | `setup/discord-setup.md` | Discord bot setup guide with channel layout |

### Setup Script

`setup-oracule.sh` — copies `config-templates/` into `~/.oracule/` using `cp -rn` (never overwrites existing files). Idempotent. Added Setup section to README.md documenting clone + run instructions.
