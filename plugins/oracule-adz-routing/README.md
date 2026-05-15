# Oracule ADZ Routing Plugin

This plugin provides intelligent model routing for all Oracule Zero agents. It reads `~/.oracule/global/routing.yaml` and tracks rate limit usage to select the best available model for a given task type.

## Features

- **Intelligent Model Selection**: Reads routing configuration and selects the best available model based on current rate limits.
- **Rate Limit Tracking**: Tracks API usage per provider and resets counts at midnight UTC.
- **Automatic Fallbacks**: Falls back to secondary models when primary models are rate-limited.
- **Usage Logging**: Logs all routing decisions to `~/.oracule/logs/routing-decisions.jsonl`.
- **Slash Commands**:
  - `/routing-status`: Shows current usage vs limits for all providers.
  - `/routing-override [task_type] [model]`: Temporarily forces a specific model for a task type (resets after session).

## How It Works

1. On startup, the plugin loads the routing configuration from `~/.oracule/global/routing.yaml`.
2. It also loads the budget configuration from `~/.oracule/global/budget.yaml` to know the rate limits.
3. Usage is tracked in `~/.oracule/state/rate-limits.json` and reset daily at midnight UTC.
4. When `get_model(task_type, agent)` is called:
   - Checks for any session-specific overrides set via `/routing-override`.
   - Looks up the task type in the routing configuration to get primary and fallback model lists.
   - Checks each model's provider against current usage and limits.
   - Returns the first available model, logging the decision.
   - If no models are available, returns the first primary model anyway (but logs as rate-limited).
5. Usage is incremented for the selected provider.

## Usage by Other Plugins and Agents

Other plugins and agents can use the router functions directly:

```python
from plugins.oracule_adz_routing import get_model

model = get_model("deep_coding", "xovadev")
```

Or access via the plugin context namespace:

```python
# In a plugin's register function
model = ctx.oracule_routing.get_model("deep_coding", "xovadev")
```

## Warning Threshold Alerting

When a provider reaches its `warn_at_percent` threshold (default 80%), the router logs a warning to the Hermes logger and returns `"warning_threshold"` as the availability reason. The calling agent should detect this reason and write an alert to Agent-Converse:

```python
available, reason = rate_limiter.is_provider_available(provider)
if reason == "warning_threshold":
    write_entry(
        type="alert",
        content=f"Provider {provider} approaching daily limit",
        author="jade",
    )
```

This ensures the warning is visible to all agents via the shared memory layer.

## Configuration

The plugin expects the following files to exist (created in earlier sessions):

- `~/.oracule/global/routing.yaml`: Defines task types and their model preferences.
- `~/.oracule/global/budget.yaml`: Defines API rate limits and warning thresholds.

These files should already exist from Session 3 setup.

## Environment Variables

- `ORACULE_HOME`: Override the default `~/.oracule` path. Useful for testing or multi-instance setups.

## Notes

- The plugin does not modify any core Hermes files.
- All state is stored under `~/.oracule/` (or `$ORACULE_HOME`).
- Overrides set via `/routing-override` are session-only and reset when the agent restarts.
- Thread-safe: concurrent model selection calls are protected by a lock.
