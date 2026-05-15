Create the Oracule ADZ Routing plugin.
Location: plugins/oracule-adz-routing/

Before writing code, read two existing plugins again if the
model context does not already have them. Confirm you know
the correct plugin registration pattern.

This plugin provides intelligent model routing for all of
Oracule Zero's agents. It reads ~/.oracule/global/routing.yaml
(already created in Session 3) and tracks rate limit usage.

Design requirements:

1. Core function: get_model(task_type, requesting_agent)
   - Reads routing.yaml for the task_type's model list
   - Checks current rate limit usage for each model
   - Returns the best available model that is not rate-limited
   - Falls through to fallback list if primary models are limited
   - Logs the selection to ~/.oracule/logs/routing-decisions.jsonl

2. Rate limit tracking:
   - Reads ~/.oracule/global/budget.yaml for limits
   - Tracks usage in ~/.oracule/state/rate-limits.json
   - Resets counts at midnight UTC automatically
   - When a provider hits warn_at_percent, logs a warning
     to Agent-Converse (type=alert)
   - When a provider hits hard_stop_at_percent, removes it
     from available models for the rest of the day

3. Commands to register:
   /routing-status — shows current usage vs limits for all
   providers in a clean table format
   /routing-override [task_type] [model] — temporarily
   forces a specific model for a task type
   (resets after current session)

4. Other plugin calling this:
   Other plugins and agents call it like:
   from plugins.oracule_adz_routing import get_model
   model = get_model("deep_coding", "xovadev")

Do not write placeholder functions. Write complete working code.
The plugin must follow the exact same structure as existing plugins.
Show full code for every file before writing to disk.

Files needed:
plugins/oracule-adz-routing/**init**.py
plugins/oracule-adz-routing/plugin.py
plugins/oracule-adz-routing/router.py
plugins/oracule-adz-routing/README.md
