"""Experience recall engine for Jade.

Manages permanent incident documentation and experience recall.
Writes to ~/.oracule/agents/jade/experience/incidents.md and never-do.md.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Paths ──────────────────────────────────────────────────────────────

EXPERIENCE_DIR = Path.home() / ".oracule" / "agents" / "jade" / "experience"
INCIDENTS_FILE = EXPERIENCE_DIR / "incidents.md"
NEVER_DO_FILE = EXPERIENCE_DIR / "never-do.md"


def _ensure_files() -> None:
    """Create the experience directory and files if they don't exist."""
    EXPERIENCE_DIR.mkdir(parents=True, exist_ok=True)
    if not INCIDENTS_FILE.exists():
        INCIDENTS_FILE.write_text(
            "# Jade — Incident Log\n\n", encoding="utf-8"
        )
    if not NEVER_DO_FILE.exists():
        NEVER_DO_FILE.write_text(
            "# Jade — Never Do List\n\n", encoding="utf-8"
        )


def _get_next_incident_number() -> str:
    """Read incidents.md and return the next INC-YYYY-NNN sequence."""
    _ensure_files()
    content = INCIDENTS_FILE.read_text(encoding="utf-8")
    pattern = re.compile(r"INC-(\d{4})-(\d+)")
    matches = pattern.findall(content)
    if not matches:
        return "INC-2026-001"

    # Find the highest sequence number
    year, seq = max(matches, key=lambda m: (int(m[0]), int(m[1])))
    next_seq = int(seq) + 1
    return f"INC-{year}-{next_seq:03d}"


def write_incident(
    situation: str,
    initial_assumption: str,
    root_cause: str,
    resolution_steps: str,
    escalated_to: str = "No",
    what_made_worse: str = "",
    time_lost: str = "",
    never_do: str = "",
    prevention: str = "",
) -> str:
    """Write a new incident to incidents.md and update never-do.md.

    Args:
        situation: What was happening when the incident occurred.
        initial_assumption: What was assumed (mark WRONG if incorrect).
        root_cause: The actual cause of the issue.
        resolution_steps: Numbered list of steps taken to resolve.
        escalated_to: Who it was escalated to, or "No".
        what_made_worse: Additional factors that worsened the situation.
        time_lost: Time lost due to wrong path.
        never_do: Rule derived from this incident.
        prevention: How to catch this earlier next time.

    Returns:
        The incident ID (e.g. INC-2026-001).
    """
    _ensure_files()
    inc_id = _get_next_incident_number()
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Build incident block
    lines = [
        f"## {inc_id} | {date_str} | Jade",
        "",
        f"**Situation:** {situation}",
        f"**Initial assumption:** {initial_assumption}",
    ]
    if what_made_worse:
        lines.append(f"**What made it worse:** {what_made_worse}")
    lines += [
        f"**Root cause:** {root_cause}",
        f"**Resolution steps:** {resolution_steps}",
        f"**Escalated to:** {escalated_to}",
    ]
    if time_lost:
        lines.append(f"**Time lost to wrong path:** {time_lost}")
    if never_do:
        lines.append(f"**Never do:** {never_do}")
    if prevention:
        lines.append(f"**Prevention:** {prevention}")
    lines.append("")
    lines.append("---")
    lines.append("")

    block = "\n".join(lines)

    # Append to incidents.md
    existing = INCIDENTS_FILE.read_text(encoding="utf-8")
    INCIDENTS_FILE.write_text(existing + block, encoding="utf-8")

    # Update never-do.md if a rule was derived
    if never_do:
        _add_never_do_rule(never_do, inc_id)

    logger.info("experience-recall: wrote incident %s", inc_id)
    return inc_id


def _add_never_do_rule(rule: str, inc_id: str) -> None:
    """Append a rule to never-do.md with a reference to the incident."""
    _ensure_files()
    existing = NEVER_DO_FILE.read_text(encoding="utf-8")
    # Avoid duplicates
    if inc_id in existing and rule in existing:
        return
    new_line = f"- {rule} (ref: {inc_id})"
    NEVER_DO_FILE.write_text(existing + new_line + "\n", encoding="utf-8")


def search_incidents(query: str, top_n: int = 3) -> list[dict]:
    """Search incidents.md for past experiences matching the query.

    Simple keyword-based search: splits the query into words, scores
    each incident by how many query words appear in its text, and
    returns the top N results.

    Args:
        query: Search query (free text).
        top_n: Maximum number of results to return.

    Returns:
        List of dicts with keys: id, date, score, content.
    """
    _ensure_files()
    content = INCIDENTS_FILE.read_text(encoding="utf-8")
    query_words = set(query.lower().split())

    # Split into incident blocks
    blocks = re.split(r"\n---\n", content)
    results = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Extract ID from header line
        header_match = re.match(r"## (INC-\d{4}-\d{3}) \| (\d{4}-\d{2}-\d{2})", block)
        if not header_match:
            continue

        inc_id = header_match.group(1)
        inc_date = header_match.group(2)

        # Score by keyword overlap
        block_lower = block.lower()
        score = sum(1 for w in query_words if w in block_lower)
        if score > 0:
            results.append({
                "id": inc_id,
                "date": inc_date,
                "score": score,
                "content": block,
            })

    # Sort by score descending, then by date descending
    results.sort(key=lambda r: (-r["score"], r["date"]), reverse=False)
    # Re-sort: score desc, date desc
    results.sort(key=lambda r: (-r["score"], r["date"]), reverse=False)
    # Actually sort properly: score desc, then date desc
    results.sort(key=lambda r: (-r["score"], [-ord(c) for c in r["date"]]))

    return results[:top_n]
