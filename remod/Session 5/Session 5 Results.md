# Session 5 Results

## Completed Tasks

### 1. AGENTS.md Analysis
- Read and extracted plugin rules (what plugins can/cannot do)
- Identified core files that cannot be modified
- Documented plugin registration guidelines

### 2. Plugin Research
- Read `plugins/disk-cleanup/` — pattern: hook + slash command plugin
- Read `plugins/spotify/` — pattern: tool registration plugin
- Read all `__init__.py` files, `plugin.yaml` files, helper modules

### 3. Plugin Design (Documented in Design Decisions.md)
- Filed under `plugins/jade-identity/`
- Uses `register(ctx)` entry point following disk-cleanup pattern
- Uses `on_session_start` lifecycle hook
- Provides 3 slash commands: `/org`, `/whoami`, `/oracule-status`
- Registers skill files via `ctx.register_skill()`

### 4. Plugin Written — 3 Files

| File | Lines | Purpose |
|------|-------|---------|
| `__init__.py` | 419 | Plugin entry: register(), hooks, slash command handlers |
| `plugin.yaml` | 11 | Metadata: name, version, description, hooks |
| `README.md` | 77 | Documentation for maintainers |

### 5. Critical Discovery — System Prompt Injection
- `ctx.register_skill()` does NOT inject into the system prompt
- It stores skills in a **separate plugin registry** accessible only via `skill_view()`
- The system prompt's `<available_skills>` index is built by `build_skills_system_prompt()` which only scans `~/.hermes/skills/` and `skills.external_dirs`
- **No plugin mechanism exists** to append arbitrary text to the system prompt
- **Solution chosen:** SOUL.md at `~/.hermes/SOUL.md` (~70 tokens, replaces DEFAULT_AGENT_IDENTITY)
- Full investigation documented in `Design Decisions.md`

### 6. SOUL.md Created
- Written to `~/.hermes/SOUL.md`
- Contains Jade's identity text at ~70 tokens
- Replaces `DEFAULT_AGENT_IDENTITY` in the stable tier of the system prompt
- Zero impact on other agents — only affects this HERMES_HOME

### 6. Design Decisions Log Created
- `remod/Session 5/Design Decisions.md` — full step-by-step reasoning with code references

## Files Created (All Locations)
```
plugins/jade-identity/__init__.py     — plugin entry point (419 lines)
plugins/jade-identity/plugin.yaml     — metadata
plugins/jade-identity/README.md       — documentation
remod/Session 5/Design Decisions.md   — design log
remod/Session 5/Session 5 Results.md  — this file
```

## Optional User Steps (Not Code)
1. Enable the plugin in `~/.hermes/config.yaml`:
   ```yaml
   plugins:
     enabled:
       - jade-identity
   ```
2. Add skills to system prompt (either option):
   ```yaml
   # Option A: external_dirs (auto-indexing)
   skills:
     external_dirs:
       - ~/.oracule/agents/jade/skills/core
   ```
   Or rename skills to SKILL.md subdirectories for auto-discovery.

### Cross-References
- `AGENTS.md` lines 465-514: Plugin architecture docs
- `hermes_cli/plugins.py` lines 287-720: PluginContext class
- `agent/prompt_builder.py` lines 988-1220: Skill system prompt builder
- `plugins/disk-cleanup/__init__.py`: Reference plugin pattern
- `plugins/spotify/__init__.py`: Reference tool registration pattern
- `~/.oracule/agents/jade/skills/core/`: Oracule skill files (Session 4)