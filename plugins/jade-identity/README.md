# Jade Identity Plugin

Provides Jade's organizational identity, slash commands for org visualization,
and runtime skill registration for the Oracule Zero agent.

## What It Does

1. **Loads config at startup** — reads `~/.oracule/agents/jade/config.yaml`
2. **Registers skill files** via `ctx.register_skill()` so they're accessible
   via `skill_view("jade-identity:<name>")`
3. **Provides three slash commands:**
   - `/org` — displays the org structure as a box-drawn tree
   - `/whoami` — shows Jade's identity, role, and reporting chain
   - `/oracule-status` — shows loaded skills, config status, org summary
4. **Warns on misconfiguration** — logs a warning if `skills.external_dirs`
   doesn't include the Oracule skills directory

## System Prompt Injection — Important Note

This plugin framework **does not support** arbitrary text injection into the
system prompt. The available mechanisms are:

- **`~/.hermes/SOUL.md`** — loaded as the agent's primary identity block
  (replaces `DEFAULT_AGENT_IDENTITY` in `run_agent.py:5924-5928`).
  This is the simplest and most effective way to inject Jade's identity.
- **`skills.external_dirs`** in `~/.hermes/config.yaml` — auto-indexes skill
  files into the `<available_skills>` block (compact index only, ~50 tokens).
- **`MemoryProvider.system_prompt_block()`** — reserved for memory providers.

**We use SOUL.md** (~70 tokens). The identity text has been written to
`~/.hermes/SOUL.md`. This gives the agent Jade's identity in the stable
tier of the system prompt. Zero config changes needed.

The plugin still registers skills via `ctx.register_skill()` for explicit
`skill_view()` access and provides the `/org`, `/whoami`, and `/oracule-status`
slash commands.

## Files

| File | Purpose |
|------|---------|
| `__init__.py` | Plugin entry point — registers hooks, commands, and skills |
| `plugin.yaml` | Metadata — name, version, hooks, provided commands |
| `README.md` | This file |

## Registration Pattern

Follows the same pattern as `plugins/disk-cleanup/`:

1. `register(ctx)` function is the sole entry point
2. `ctx.register_hook()` for the `on_session_start` lifecycle hook
3. `ctx.register_command()` for each slash command
4. `ctx.register_skill()` for each skill file

## Skill Files

Skill files live in `~/.oracule/agents/jade/skills/core/` and use this
frontmatter format:

```yaml
---
name: Skill Name
description: Semantic trigger — when to activate this skill
always_load: true/false
---
```

See `config-templates/agents/jade/skills/core/` for backup copies.