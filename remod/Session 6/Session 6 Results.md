# Session 6: Oracule ADZ Routing Plugin - Implementation Summary

## Files Created

### 1. `plugins/oracule-adz-routing/__init__.py`

Plugin entry point. Registers slash commands (`/routing-status`, `/routing-override`) and exposes router functions via `ctx.oracule_routing` namespace.

### 2. `plugins/oracule-adz-routing/plugin.yaml`

Plugin metadata: name, version, description, author, and registered commands.

### 3. `plugins/oracule-adz-routing/router.py`

Core routing logic:

- `RateLimiter` class: Tracks per-provider API usage, resets at midnight UTC, enforces warn/hard-stop thresholds, thread-safe via `threading.Lock`
- `Router` class: Model selection with primary/fallback fallback chain, session-scoped overrides, JSONL decision logging
- Public API: `get_model()`, `set_override()`, `clear_override()`, `get_routing_status()`

### 4. `plugins/oracule-adz-routing/README.md`

Documentation covering features, usage, warning threshold alerting, configuration, and environment variables.

## Design Decisions & Fixes Applied

### Issue 1: Thread Safety — `threading.Lock` in `RateLimiter`

**What changed:**

- Added `import threading` to `router.py`
- Added `self._lock = threading.Lock()` in `RateLimiter.__init__`
- Wrapped `get_usage()`, `increment_usage()`, and `is_provider_available()` with `with self._lock:`
- Updated docstrings on `_check_reset()` and `_save_usage()` to note they must be called under the lock

**Why:**
Concurrent tool calls (parallel tool execution is a Jade feature) could call `increment_usage()` simultaneously. Without a lock, two threads could read the same usage count, both increment by 1, and write back the same value — losing one increment. Over time this causes usage to drift below actual, defeating rate limiting.

### Issue 2: Provider Name Mismatch — `MODEL_TO_BUDGET_PROVIDER` Mapping

**What changed:**

- Added a 12-entry dict mapping model prefixes to `budget.yaml` keys (`"google"` → `"google_gemini"`, `"nvidia"` → `"nvidia_nim"`, `"cloudflare"` → `"cloudflare_workers_ai"`, etc.)
- Rewrote `get_provider_from_model()` to extract the prefix then look it up in the dict, falling back to the raw prefix if no mapping exists

**Why:**
`routing.yaml` lists models like `google/gemini-cli-2.5-pro`. Splitting on `/` gives `"google"`, but `budget.yaml` uses the key `"google_gemini"`. Without the mapping, `get_limit("google")` returns `None`, causing `is_provider_available()` to return `True, "no_daily_limit"` for every provider — effectively disabling all rate limiting.

### Issue 3: Warning Threshold Logging

**What changed:**

- Added `import logging` and `logger = logging.getLogger(__name__)` to `router.py`
- When usage crosses `warn_at_percent` in `is_provider_available()`, logs a `logger.warning()` with provider name, percentage, raw usage/limit, and instruction to call `write_entry(type='alert')`
- Added **"Warning Threshold Alerting"** section to `README.md` with a code snippet showing how agents should respond to the `"warning_threshold"` reason

**Why:**
The spec requires logging a warning to Agent-Converse when the threshold is hit. The plugin cannot directly write to Agent-Converse (requires MCP tools). The compromise: log to the Jade logger (visible in `agent.log`) and document the pattern so the calling agent can detect the reason and write the alert itself.

### Issue 4: Silent Exception in `_log_decision`

**What changed:**

- Replaced `except Exception: pass` with `except Exception as exc: logger.debug("Failed to log routing decision: %s", exc)`

**Why:**
A bare `pass` swallows all errors silently. If the log directory is unwritable or the disk is full, you'd never know. `logger.debug()` keeps the failure observable in debug mode without crashing the routing flow.

### Issue 5: Clean Context API — `types.SimpleNamespace`

**What changed:**

- Added `import types` to `__init__.py`
- Replaced four separate `ctx.router_* = ...` assignments with a single `ctx.oracule_routing = types.SimpleNamespace(...)` containing `get_model`, `set_override`, `clear_override`, and `get_status`
- Updated `README.md` to show the new access pattern: `ctx.oracule_routing.get_model(...)`

**Why:**
Attaching arbitrary attributes directly to `ctx` risks name collisions with existing or future ctx attributes. A nested namespace object isolates the plugin's public API and makes it clear these functions belong to the routing plugin.

### Issue 6: `Path.home()` at Module Load — Env Var Override + Lazy Directory Creation

**What changed:**

- Added `import os` to `router.py`
- Replaced `HOME = Path.home()` with `_ORACULE_HOME = Path(os.environ.get("ORACULE_HOME", str(Path.home() / ".oracule")))`
- All path constants now derive from `_ORACULE_HOME`
- Removed module-level `ORACULE_STATE.mkdir()` / `ORACULE_LOGS.mkdir()` calls
- Added `_ensure_directories()` with a guard flag, called from `Router.__init__`

**Why:**
Calling `Path.home()` at import time hardcodes the path before any env var override can take effect. The `os.environ.get()` pattern allows `ORACULE_HOME` to redirect all paths (useful for testing or multi-instance setups). Deferring directory creation avoids side effects at import time — importing the module no longer mutates the filesystem.

### Issue 7: Import Cleanup in `__init__.py`

**What changed:**

- Moved `import yaml` from inside `_handle_routing_override` to module-level imports
- Removed inline `from pathlib import Path` and hardcoded path construction from the handler
- Added `ROUTING_YAML` to the `from .router import (...)` block
- Used the imported `ROUTING_YAML` constant directly in `_handle_routing_override`

**Why:**
Re-importing inside a function on every slash command invocation is wasteful. Using the shared constant from `router.py` ensures both files reference the exact same path — if it ever changes, it only needs updating in one place.

## Assumptions & Additions Outside Scope

1. **Removed `hooks` from `plugin.yaml`**: The original listed `post_tool_call` and `on_session_end` hooks, but the plugin doesn't register any. Removed them to prevent the plugin loader from expecting hooks that don't exist.

2. **Added `logger` to `router.py`**: The file had no logging setup. Added `import logging` and `logger = logging.getLogger(__name__)` to support the warning and debug log calls (direct dependency of Issues 3 and 4).

3. **Lazy directory creation**: The original code created directories at module import time. Deferred to `_ensure_directories()` called from `Router.__init__` — a direct consequence of fixing Issue 6.

4. **README updates beyond Issue 3**: Added documentation for the `ORACULE_HOME` env var, the thread safety guarantee, and the new `ctx.oracule_routing` access pattern. Natural consequences of the code changes.

No unrelated features, new functions, or behavioral changes were introduced beyond what the 7 issues required.

## How It Works

1. Agent calls `get_model(task_type, requesting_agent)`
2. Router checks for session override → if present, returns it immediately
3. Looks up task type in `routing.yaml` → gets primary and fallback model lists
4. For each model, extracts provider, maps to budget key, checks rate limit status
5. Returns first available model, increments usage, logs decision to JSONL
6. Falls through to fallback list if all primary models are limited
7. If all models are blocked, returns first primary anyway (logged as `rate_limited=True`)

## Rate Limit Behavior

- Usage tracked in `~/.oracule/state/rate-limits.json`
- Resets automatically at midnight UTC
- `warn_at_percent` (default 80%): Logs warning, returns `"warning_threshold"`
- `hard_stop_at_percent` (default 100%): Returns `False`, model excluded from selection
- Providers without `daily_requests` in budget.yaml are always available

## Slash Commands

- `/routing-status`: Table showing provider, usage, limit, % used, and status (OK/WARNING/HARD STOP/BLOCKED)
- `/routing-override [task_type] [model]`: Forces a specific model for a task type. Resets after session. Validates task type exists in routing.yaml.
