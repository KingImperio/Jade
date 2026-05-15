"""Oracule ADZ Routing plugin for intelligent model routing.

This plugin reads ~/.oracule/global/routing.yaml and tracks rate limit usage
to provide intelligent model selection for all Oracule Zero agents.
"""

from __future__ import annotations

import logging
import types

import yaml

from .router import (
    ROUTING_YAML,
    clear_override,
    get_model,
    get_routing_status,
    set_override,
)

logger = logging.getLogger(__name__)


def register(ctx) -> None:
    """Register hooks, slash commands, and make router functions available.

    Called once by the plugin loader when the plugin is enabled via
    plugins.enabled in config.yaml.
    """
    # Issue 5: Use types.SimpleNamespace instead of arbitrary ctx attributes
    ctx.oracule_routing = types.SimpleNamespace(
        get_model=get_model,
        set_override=set_override,
        clear_override=clear_override,
        get_status=get_routing_status,
    )

    # Register slash commands
    ctx.register_command(
        "routing-status",
        handler=_handle_routing_status,
        description="Show current model routing status and rate limits.",
    )

    ctx.register_command(
        "routing-override",
        handler=_handle_routing_override,
        description="Temporarily override model for a task type.",
        args_hint="[task_type] [model]",
    )

    logger.info("oracule-adz-routing plugin registered: 2 slash commands")


def _handle_routing_status(raw_args: str) -> str:
    """Slash command: /routing-status

    Shows current usage vs limits for all providers in a clean table format.
    """
    try:
        status = get_routing_status()

        if not status:
            return "No routing status available."

        lines = []
        lines.append("Oracule ADZ Routing Status")
        lines.append("=" * 50)
        lines.append(f"{'Provider':<20} {'Usage':<10} {'Limit':<10} {'% Used':<10} {'Status':<15}")
        lines.append("-" * 50)

        for provider, data in sorted(status.items()):
            usage = data["usage"]
            limit = data["limit"]
            usage_percent = data["usage_percent"]
            available = data["available"]

            # Format limit
            limit_str = str(limit) if limit is not None else "N/A"

            # Determine status
            if not available:
                status_str = "BLOCKED"
            elif usage_percent >= data["hard_stop_percent"]:
                status_str = "HARD STOP"
            elif usage_percent >= data["warn_percent"]:
                status_str = "WARNING"
            else:
                status_str = "OK"

            lines.append(f"{provider:<20} {usage:<10} {limit_str:<10} {usage_percent:<10.1f} {status_str:<15}")

        return "\n".join(lines)
    except Exception as e:
        logger.error("Error in routing-status: %s", e)
        return f"Error retrieving routing status: {e}"


def _handle_routing_override(raw_args: str) -> str:
    """Slash command: /routing-override [task_type] [model]

    Temporarily forces a specific model for a task type (resets after session).
    """
    try:
        args = raw_args.strip().split()
        if len(args) != 2:
            return "Usage: /routing-override [task_type] [model]"

        task_type, model = args

        # Issue 7: Use shared ROUTING_YAML constant instead of hardcoding
        if ROUTING_YAML.exists():
            routing_config = yaml.safe_load(ROUTING_YAML.read_text(encoding="utf-8")) or {}
            if task_type not in routing_config.get("task_types", {}):
                return f"Unknown task type: {task_type}. Available: {list(routing_config.get('task_types', {}).keys())}"

        set_override(task_type, model)

        return f"Override set: {task_type} -> {model} (will reset after session)"
    except Exception as e:
        logger.error("Error in routing-override: %s", e)
        return f"Error setting override: {e}"
