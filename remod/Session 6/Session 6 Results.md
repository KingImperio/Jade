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

### Thread Safety (Issue 1)
Added `threading.Lock` to `RateLimiter`. All read-modify-write operations on usage counts are serialized to prevent lost increments during concurrent tool calls.

### Provider Name Mapping (Issue 2)
Added `MODEL_TO_BUDGET_PROVIDER` dict mapping model prefixes (e.g., `"google"`) to `budget.yaml` keys (e.g., `"google_gemini"`). Without this, rate limit lookups would fail silently since `routing.yaml` and `budget.yaml` use different naming conventions.

### Warning Threshold Logging (Issue 3)
When a provider crosses `warn_at_percent`, the router logs a warning via `logger.warning()` and returns `"warning_threshold"` as the availability reason. The README documents how agents should respond by calling `write_entry(type="alert")` on Agent-Converse.

### Error Handling (Issue 4)
Replaced bare `except: pass` in `_log_decision()` with `logger.debug()` to make logging failures observable without crashing routing.

### Clean Context API (Issue 5)
Replaced arbitrary `ctx.router_*` attributes with `ctx.oracule_routing = types.SimpleNamespace(...)`. Isolates the plugin's public API and prevents name collisions.

### Lazy Directory Creation & Env Override (Issue 6)
Replaced module-level `Path.home()` with `os.environ.get("ORACULE_HOME", ...)`. Deferred directory creation to `_ensure_directories()` called from `Router.__init__` to avoid import-time side effects.

### Import Cleanup (Issue 7)
Moved all imports to module level in `__init__.py`. Reused `ROUTING_YAML` constant from `router.py` instead of hardcoding the path in the slash command handler.

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
