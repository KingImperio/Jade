"""Experience recall plugin for Jade.

Manages Jade's permanent incident documentation and experience recall
system. After task completion, prompts Jade to document errors, wrong
assumptions, novel solutions, and escalations.
"""

from __future__ import annotations

import logging
import re

from .recall import search_incidents, write_incident

logger = logging.getLogger(__name__)


def register(ctx) -> None:
    """Register hooks and slash commands.

    Called once by the plugin loader when the plugin is enabled via
    plugins.enabled in config.yaml.
    """
    # Register post-tool-call hook to detect incidents
    ctx.register_hook("post_tool_call", _post_tool_call_hook)

    # Register slash commands
    ctx.register_command(
        "incident",
        handler=_handle_incident,
        description="Manually trigger incident documentation for the current task.",
    )

    ctx.register_command(
        "recall-experience",
        handler=_handle_recall,
        description="Search past incidents matching a query.",
        args_hint="<query>",
    )

    logger.info("experience-recall plugin registered: 2 slash commands, 1 hook")


def _post_tool_call_hook(
    tool_name: str = "",
    tool_result: str = "",
    **kwargs,
) -> None:
    """Hook: post_tool_call.

    Inspects tool results for error signals. If an error or failure is
    detected, logs it for the agent to consider documenting via /incident.
    """
    if not tool_result:
        return

    result_lower = tool_result.lower()
    error_signals = [
        "error",
        "failed",
        "failure",
        "exception",
        "traceback",
        "cannot",
        "unable to",
        "not found",
        "permission denied",
    ]

    if any(sig in result_lower for sig in error_signals):
        logger.info(
            "experience-recall: potential incident detected in tool '%s' "
            "(result contains error signal) — use /incident to document",
            tool_name,
        )


def _handle_incident(raw_args: str) -> str:
    """Slash command: /incident

    Manually trigger incident documentation. If arguments are provided
    in a structured format, writes the incident directly. Otherwise,
    returns a template for the user to fill in.
    """
    args = raw_args.strip()
    if not args:
        return (
            "Use /incident with details, or fill in this template:\n\n"
            "```\n"
            "/incident situation=<what happened> "
            "assumption=<what was assumed> "
            "root_cause=<actual cause> "
            "resolution=<steps taken> "
            "[escalated_to=<who>] "
            "[time_lost=<duration>] "
            "[never_do=<rule>] "
            "[prevention=<how to catch earlier>]\n"
            "```\n\n"
            "Fields in brackets are optional."
        )

    # Parse key=value arguments
    params = _parse_kv(args)

    situation = params.get("situation", "")
    assumption = params.get("assumption", "")
    root_cause = params.get("root_cause", "")
    resolution = params.get("resolution", "")

    if not situation or not root_cause:
        return "Missing required fields: situation and root_cause are required."

    inc_id = write_incident(
        situation=situation,
        initial_assumption=assumption or "Not documented",
        root_cause=root_cause,
        resolution_steps=resolution or "Not documented",
        escalated_to=params.get("escalated_to", "No"),
        what_made_worse=params.get("what_made_worse", ""),
        time_lost=params.get("time_lost", ""),
        never_do=params.get("never_do", ""),
        prevention=params.get("prevention", ""),
    )

    return f"Incident {inc_id} recorded."


def _handle_recall(raw_args: str) -> str:
    """Slash command: /recall-experience [query]

    Search incidents.md for past experiences matching the query.
    Returns top 3 most relevant incidents.
    """
    query = raw_args.strip()
    if not query:
        return "Usage: /recall-experience <search query>"

    results = search_incidents(query, top_n=3)
    if not results:
        return f"No past incidents found matching '{query}'."

    lines = [f"Found {len(results)} relevant incident(s) for '{query}':\n"]
    for r in results:
        lines.append(f"### {r['id']} | {r['date']} | score: {r['score']}")
        # Show first 500 chars of content
        content = r["content"]
        if len(content) > 500:
            content = content[:500] + "..."
        lines.append(content)
        lines.append("")

    return "\n".join(lines)


def _parse_kv(text: str) -> dict[str, str]:
    """Parse key=value pairs from a string.

    Handles quoted values and ignores whitespace between pairs.
    """
    params = {}
    pattern = r'(\w+)=(?:"([^"]*?)"|(\S+))'
    for match in re.finditer(pattern, text):
        key = match.group(1)
        value = match.group(2) if match.group(2) is not None else match.group(3)
        params[key] = value
    return params
