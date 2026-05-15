# Session 5 — Jade Identity Plugin: Design & Implementation Log

## Overview

Created a `jade-identity` plugin for the Hermes Agent framework that loads
Jade's organizational configuration and makes it available via slash commands
and the skill system.

---

## Step 1: AGENTS.md Findings

### (a) Plugin Rules
- Each plugin exposes a `register(ctx)` function
- Can register lifecycle hooks: `pre_tool_call`, `post_tool_call`,
  `pre_llm_call`, `post_llm_call`, `on_session_start`, `on_session_end`
- Can register tools via `ctx.register_tool(...)`
- Can register slash commands via `ctx.register_command(...)`
- Can register CLI subcommands via `ctx.register_cli_command(...)`
- Can register skills via `ctx.register_skill(name, path, description)`
- Must NOT modify core files (`run_agent.py`, `cli.py`, `gateway/run.py`, etc.)

### (b) Core Files We Cannot Modify
`run_agent.py`, `cli.py`, `gateway/run.py`, `hermes_cli/main.py`, and
all other top-level core modules.

### (c) Plugin Registration Guidelines
- `plugin.yaml` declares: name, version, description, author, kind, hooks, provides_commands
- `__init__.py` contains: `register(ctx)` function, hook handlers, command handlers
- Plugins are discovered from `plugins/`, `~/.hermes/plugins/`, and pip entry points
- `kind: standalone` for general-purpose plugins; `kind: backend` for provider plugins

**Source:** `AGENTS.md` lines 465-514

---

## Step 2: Existing Plugins Analyzed

### Plugin A: disk-cleanup
- **Location:** `plugins/disk-cleanup/`
- **Files:** `__init__.py`, `disk_cleanup.py`, `plugin.yaml`, `README.md`
- **Pattern:** `__init__.py` is the main entry point with `register()`.
  `disk_cleanup.py` is a helper library imported by `__init__.py`.
- **Hooks:** `post_tool_call` (auto-track temp files), `on_session_end` (cleanup)
- **Slash command:** `/disk-cleanup` with subcommands (status, dry-run, quick, etc.)
- **Registration:**
  ```python
  def register(ctx) -> None:
      ctx.register_hook("post_tool_call", _on_post_tool_call)
      ctx.register_hook("on_session_end", _on_session_end)
      ctx.register_command("disk-cleanup", handler=_handle_slash, description="...")
  ```

### Plugin B: spotify
- **Location:** `plugins/spotify/`
- **Files:** `__init__.py`, `tools.py`, `client.py`, `plugin.yaml`
- **Pattern:** `__init__.py` loops over a `_TOOLS` tuple to register each tool.
- **Hooks:** None (pure tool registration)
- **Registration:**
  ```python
  def register(ctx) -> None:
      for name, schema, handler, emoji in _TOOLS:
          ctx.register_tool(name=name, toolset="spotify", schema=schema, ...)
  ```

### Key Design Patterns Observed
1. `plugin.yaml` is minimal metadata; `__init__.py` does all the work
2. Helper code goes in separate modules (e.g., `disk_cleanup.py`, `tools.py`)
3. Hooks and commands are registered in `register(ctx)` — never outside it
4. Hook callbacks are plain functions, not class methods

---

## Revised Recommendation: SOUL.md + Plugin-Only Skills

After investigating the full system prompt assembly pipeline
(`run_agent.py:5899-6106`, `agent/prompt_builder.py:988-1456`), the token
math makes the decision clear:

### System Prompt Assembly — What Actually Happens

The system prompt is built in three tiers (see `_build_system_prompt_parts`
at `run_agent.py:5899`):

| Tier | Contents | Approx Tokens |
|------|----------|---------------|
| **stable** | SOUL.md (or DEFAULT_AGENT_IDENTITY), tool guidance, skills index, env hints | ~400-600 |
| **context** | AGENTS.md, .cursorrules, project context files | ~0-500 |
| **volatile** | Memory snapshot, user profile, timestamp | ~0-200 |

The `<available_skills>` index built by `build_skills_system_prompt()`
only contains **name + one-line description** per skill — roughly 30-50
tokens total for all 5 Oracule skills. Full skill content is NEVER
injected into the system prompt.

### Our Approach

1. **SOUL.md at `~/.hermes/SOUL.md`** — ~70 tokens, replaces the default
   identity block. This is the primary identity mechanism and is already
   wired into the stable tier.

2. **Plugin-only skills (no external_dirs)** — 0 additional tokens in
   system prompt. Skills accessible via `skill_view()` for explicit load.
   Slash commands work regardless.

3. **No external_dirs modification** — avoids polluting OTHER agents'
   system prompts with Oracule-specific content. The `<available_skills>`
   index appears in every agent's context; Oracule rules would be noise
   for general-purpose agents.

### Token Budget

```
Without SOUL.md:     ~200-400 tokens (DEFAULT_AGENT_IDENTITY + guidance)
With SOUL.md:        ~270-470 tokens (+70 for Jade identity)
Skills in index:     +50 tokens (if external_dirs added — not recommended)
Full skill content:  NEVER injected (this fear is unfounded)
```

The marginal cost of SOUL.md is trivial. The plugin handles everything
else at runtime.

### (c) How the Plugin Will Load Config

```python
JADE_CONFIG_PATH = Path.home() / ".oracule" / "agents" / "jade" / "config.yaml"

def _load_config() -> dict:
    global _jade_config
    _jade_config = yaml.safe_load(JADE_CONFIG_PATH.read_text()) or {}
    return _jade_config
```

Config is loaded at plugin registration time and on every `on_session_start`
hook (to pick up changes between sessions).

### (d) Hooks Used

- **`on_session_start`** — reloads config, re-registers skills, verifies
  `skills.external_dirs`, logs status

### (e) Slash Commands

Three commands registered via `ctx.register_command()`:

1. **`/org`** — Reads `organization` section from config.yaml, renders as
   box-drawn text tree with department heads and workers
2. **`/whoami`** — Reads `identity` section, displays name, role, org, tier,
   peers, reporting chain
3. **`/oracule-status`** — Shows config path, skill registration status,
   org summary (department count, worker count)

### (f) `register_skill()` Arguments Confirmed

From `hermes_cli/plugins.py:677-680`:
```python
def register_skill(self, name: str, path: Path, description: str = "") -> None:
```
- `name`: identifier matching `[a-zA-Z0-9_-]+`
- `path`: `Path` to a SKILL.md file (must exist)
- `description`: optional string

Skills are registered by path reference — content is read later at
`skill_view()` call time, including frontmatter parsing.

---

## Step 4: Files Written

### 1. `plugins/jade-identity/__init__.py`
- `register(ctx)` — main entry point
- `_load_config()` — loads config.yaml into module state
- `_register_skills(ctx)` — registers all *.md files from skills/core
- `_check_external_dirs()` — verifies external_dirs config, warns if missing
- `_on_session_start()` — lifecycle hook
- `_handle_org()`, `_handle_whoami()`, `_handle_oracule_status()` — command handlers

### 2. `plugins/jade-identity/plugin.yaml`
- name: jade-identity
- version: 1.0.0
- kind: standalone
- hooks: on_session_start
- provides_commands: org, whoami, oracule-status

### 3. `plugins/jade-identity/README.md`
- Documents what the plugin does
- Explains the system prompt injection limitation
- Shows the config snippet needed for system prompt integration
- References the registration pattern from disk-cleanup

---

## Remaining Action Items

1. **Create `~/.hermes/SOUL.md`** — done (identity text at ~70 tokens)
2. **Enable the plugin** in `~/.hermes/config.yaml`:
   ```yaml
   plugins:
     enabled:
       - jade-identity
   ```
3. **No `skills.external_dirs` changes needed** — SOUL.md handles identity;
   plugin skills are available via `skill_view()` for explicit load.

---

## Cross-References

- `AGENTS.md` lines 465-514: Plugin architecture docs
- `hermes_cli/plugins.py` lines 287-720: `PluginContext` and `PluginManager`
- `agent/prompt_builder.py` lines 988-1220: `build_skills_system_prompt()`
- `plugins/disk-cleanup/__init__.py`: Reference pattern for hook + command plugins
- `plugins/spotify/__init__.py`: Reference pattern for tool registration
- `~/.oracule/agents/jade/skills/core/`: Oracule skill files (from Session 4)
- `config-templates/agents/jade/skills/core/`: Backup copies of skill files