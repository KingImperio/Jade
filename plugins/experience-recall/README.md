# Experience Recall Plugin

Manages Jade's permanent incident documentation and experience recall system.

## Features

- **Auto-detection**: Monitors tool results for error signals and logs potential incidents.
- **Incident logging**: Writes structured incident reports to `~/.oracule/agents/jade/experience/incidents.md`.
- **Never-do rules**: Automatically derives and appends prevention rules to `~/.oracule/agents/jade/experience/never-do.md`.
- **Experience search**: Keyword-based search across past incidents.
- **Auto-sequencing**: Incident IDs auto-increment (INC-2026-001, INC-2026-002, ...).

## Incident Format

Each incident in `incidents.md`:

```
## INC-2026-001 | 2026-05-16 | Jade

**Situation:** [what was happening]
**Initial assumption:** [what was assumed — mark WRONG if incorrect]
**What made it worse:** [if applicable, else omitted]
**Root cause:** [actual cause]
**Resolution steps:** [numbered list]
**Escalated to:** [who, or "No"]
**Time lost to wrong path:** [if applicable]
**Never do:** [rule derived from this]
**Prevention:** [how to catch this earlier]
```

## Never-Do Format

Rules in `never-do.md`:

```
# Jade — Never Do List
- [Rule] (ref: INC-2026-001)
```

## Slash Commands

- `/incident` — Manually trigger incident documentation. Use with key=value arguments or get a template.
- `/recall-experience <query>` — Search past incidents. Returns top 3 most relevant matches.

## Usage

### Manual incident:

```
/incident situation="API returned 500 on retry" assumption="Retry would succeed" root_cause="Rate limit exceeded" resolution="1. Added exponential backoff 2. Reduced request frequency" never_do="Retry without backoff on rate-limited APIs" prevention="Check rate limit headers before retrying"
```

### Search past incidents:

```
/recall-experience rate limit retry
```

## Files

- `~/.oracule/agents/jade/experience/incidents.md` — Running incident log (auto-created).
- `~/.oracule/agents/jade/experience/never-do.md` — Distilled prevention rules (auto-created).
