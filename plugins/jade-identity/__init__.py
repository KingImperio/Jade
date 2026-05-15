"""Jade identity plugin for Oracule Zero.

Loads Jade's organizational configuration from config.yaml, registers
core skill files into the plugin skill registry, and provides slash
commands for org visualization and status reporting.

Note on system prompt injection:
    The plugin framework does NOT support arbitrary system prompt
    modification. To get Oracule skills into the system prompt's
    <available_skills> block, add the skills core directory to
    skills.external_dirs in ~/.hermes/config.yaml:

        skills:
          external_dirs:
            - ~/.oracule/agents/jade/skills/core

    The plugin will verify this on startup and warn if it's missing.
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────

JADE_CONFIG_PATH = Path.home() / ".oracule" / "agents" / "jade" / "config.yaml"
SKILLS_CORE_DIR = Path.home() / ".oracule" / "agents" / "jade" / "skills" / "core"

# ── Module-level state ─────────────────────────────────────────────────

_jade_config: dict | None = None
_registered_skills: list[str] = []


# ── Config loading ─────────────────────────────────────────────────────

def get_config() -> dict:
    """Return the loaded Jade config dict. Empty if not yet loaded."""
    return _jade_config or {}


def _load_config() -> dict:
    """Load ~/.oracule/agents/jade/config.yaml into module state.

    Returns the parsed config dict (may be empty on failure).
    """
    global _jade_config
    if not JADE_CONFIG_PATH.exists():
        logger.warning(
            "jade-identity: config file not found at %s", JADE_CONFIG_PATH
        )
        _jade_config = {}
        return {}
    try:
        _jade_config = yaml.safe_load(
            JADE_CONFIG_PATH.read_text(encoding="utf-8")
        ) or {}
        logger.info(
            "jade-identity: loaded config from %s", JADE_CONFIG_PATH
        )
        return _jade_config
    except Exception as exc:
        logger.error("jade-identity: failed to parse config: %s", exc)
        _jade_config = {}
        return {}


# ── Skill registration ────────────────────────────────────────────────

def _register_skills(ctx) -> int:
    """Register all skill files from the core skills directory.

    Skills are registered regardless of their always_load value so they
    remain accessible via skill_view('jade-identity:<name>').

    Args:
        ctx: The PluginContext passed during registration.

    Returns:
        Count of successfully registered skills.
    """
    global _registered_skills
    if not SKILLS_CORE_DIR.exists():
        logger.warning(
            "jade-identity: skills core dir not found at %s", SKILLS_CORE_DIR
        )
        return 0

    from agent.skill_utils import parse_frontmatter

    count = 0
    for skill_file in sorted(SKILLS_CORE_DIR.glob("*.md")):
        try:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter, _ = parse_frontmatter(content)

            ctx.register_skill(
                name=skill_file.stem,
                path=skill_file,
                description=frontmatter.get("description", ""),
            )
            _registered_skills.append(skill_file.stem)
            logger.debug(
                "jade-identity: registered skill %s "
                "(always_load=%s, description=%s)",
                skill_file.stem,
                frontmatter.get("always_load", False),
                frontmatter.get("description", "")[:60],
            )
            count += 1
        except Exception as exc:
            logger.warning(
                "jade-identity: failed to register skill %s: %s",
                skill_file,
                exc,
            )
    return count


def _check_external_dirs() -> bool:
    """Check whether skills core dir is in config's external_dirs.

    Logs a warning if it is not found, since skills won't appear in
    the system prompt's <available_skills> block without this config.

    Returns:
        True if the directory is listed, False otherwise.
    """
    try:
        from hermes_cli.config import load_config

        cfg = load_config()
        ext_dirs = cfg.get("skills", {}).get("external_dirs", [])
        resolved_core = str(SKILLS_CORE_DIR.resolve())
        resolved_ext = [str(Path(d).resolve()) for d in ext_dirs]

        if resolved_core in resolved_ext:
            return True

        logger.warning(
            "jade-identity: %s is NOT in skills.external_dirs. "
            "Skills will be registered for programmatic access "
            "(skill_view) but will NOT appear in the system prompt's "
            "<available_skills> index. "
            "Fix: add to ~/.hermes/config.yaml:\n"
            "  skills:\n"
            "    external_dirs:\n"
            "      - %s",
            SKILLS_CORE_DIR,
            SKILLS_CORE_DIR,
        )
        return False
    except Exception:
        logger.debug("jade-identity: could not check external_dirs", exc_info=True)
        return False


# ── Org tree rendering ────────────────────────────────────────────────

def _build_org_tree(org_data: dict, indent: int = 0) -> str:
    """Build a text-tree representation of the org structure.

    Args:
        org_data: The 'organization' section from config.yaml.
        indent:   Base indentation level (for recursion).

    Returns:
        Multi-line string with box-drawing tree.
    """
    lines = []
    prefix = "  " * indent

    org_name = org_data.get("organization", {}).get("name", "Oracule Zero")
    lines.append(f"{prefix}{org_name}")

    # Executive layer
    exec_layer = org_data.get("executive_layer", {})
    if exec_layer:
        lines.append(f"{prefix}  ├── Executive Layer")
        exec_items = list(exec_layer.items())
        for i, (role, person) in enumerate(exec_items):
            connector = "├──" if i < len(exec_items) - 1 else "└──"
            lines.append(f"{prefix}  │  {connector} {role}: {person}")

    # Department heads and their workers
    dept_heads = org_data.get("department_heads", {})
    if dept_heads:
        lines.append(f"{prefix}  └── Department Heads")
        depts = list(dept_heads.items())
        for i, (dept, workers) in enumerate(depts):
            dept_connector = "├──" if i < len(depts) - 1 else "└──"
            lines.append(f"{prefix}  │  {dept_connector} {dept}")
            for j, worker in enumerate(workers):
                worker_connector = "├──" if j < len(workers) - 1 else "└──"
                lines.append(f"{prefix}  │     {worker_connector} {worker}")

    # Worker capabilities
    capabilities = org_data.get("worker_capabilities", {})
    if capabilities:
        lines.append(f"{prefix}  └── Worker Capabilities")
        caps = list(capabilities.items())
        for i, (cap, value) in enumerate(caps):
            connector = "├──" if i < len(caps) - 1 else "└──"
            lines.append(f"{prefix}     {connector} {cap}: {value}")

    return "\n".join(lines)


# ── Slash command handlers ────────────────────────────────────────────

def _handle_org(raw_args: str) -> str:
    """Slash command: /org

    Reads org_structure from config.yaml and renders it as a clean
    box-drawn text tree.
    """
    config = get_config()
    if not config:
        return (
            "No org configuration found.\n"
            f"Ensure {JADE_CONFIG_PATH} exists with an 'organization' section."
        )

    org_structure = config.get("organization", {})
    if not org_structure:
        return "Config exists but contains no 'organization' section."

    lines = []
    lines.append("┌─ Oracule Zero — Org Structure ───────────────┐")
    lines.append("│                                               │")

    tree = _build_org_tree(org_structure, indent=1)
    for line in tree.split("\n"):
        padded = line.ljust(44)[:44]
        lines.append(f"│  {padded}│")

    lines.append("│                                               │")
    lines.append("└───────────────────────────────────────────────┘")
    return "\n".join(lines)


def _handle_whoami(raw_args: str) -> str:
    """Slash command: /whoami

    Displays Jade's identity and current role from config.yaml.
    """
    config = get_config()
    if not config:
        return "No identity configuration found."

    identity = config.get("identity", {})
    if not identity:
        return "Config exists but contains no 'identity' section."

    lines = []
    lines.append("┌─ Jade Identity ──────────────────────────────┐")
    lines.append("│                                               │")
    lines.append(
        f"│  Name:         {identity.get('name', 'Jade'):<35}│"
    )
    lines.append(
        f"│  Role:         {identity.get('role', 'Executive Orchestrator'):<35}│"
    )
    lines.append(
        f"│  Organization: {identity.get('organization', 'Oracule Zero'):<35}│"
    )
    tier = identity.get("tier", "Tier 1")
    lines.append(f"│  Tier:         {tier:<35}│")
    lines.append("│                                               │")

    peers = identity.get("peers", [])
    if peers:
        peer_str = ", ".join(peers)
        lines.append(
            f"│  Peers:        {peer_str:<35}│"
        )

    reports_to = identity.get("reports_to", "S.B.")
    lines.append(
        f"│  Reports to:   {reports_to:<35}│"
    )
    lines.append("│                                               │")
    lines.append("└───────────────────────────────────────────────┘")
    return "\n".join(lines)


def _handle_oracule_status(raw_args: str) -> str:
    """Slash command: /oracule-status

    Shows which skills are loaded, config path, and org summary.
    """
    config = get_config()

    org = config.get("organization", {})
    dept_heads = org.get("department_heads", {})
    worker_count = sum(len(w) for w in dept_heads.values())

    skills_dir_exists = SKILLS_CORE_DIR.exists()
    skill_file_count = (
        len(list(SKILLS_CORE_DIR.glob("*.md"))) if skills_dir_exists else 0
    )

    lines = []
    lines.append("┌─ Oracule Status ─────────────────────────────┐")
    lines.append("│                                               │")
    lines.append(
        f"│  Config path:     {str(JADE_CONFIG_PATH):<38}│"
    )
    lines.append(
        f"│  Config loaded:   {'Yes' if config else 'No':<38}│"
    )
    lines.append(
        f"│  Org name:        {org.get('name', 'N/A'):<38}│"
    )
    lines.append(
        f"│  Departments:     {len(dept_heads):<38}│"
    )
    lines.append(
        f"│  Workers total:   {worker_count:<38}│"
    )
    lines.append(
        f"│  Skills dir:      {str(SKILLS_CORE_DIR):<38}│"
    )
    lines.append(
        f"│  Skills dir exists: {'Yes' if skills_dir_exists else 'No':<31}│"
    )
    lines.append(
        f"│  Skill files found: {skill_file_count:<31}│"
    )
    lines.append(
        f"│  Registered via plugin: {len(_registered_skills):<19}│"
    )
    if _registered_skills:
        for skill in _registered_skills:
            lines.append(
                f"│    • {skill:<37}│"
            )
    lines.append("│                                               │")
    lines.append("└───────────────────────────────────────────────┘")
    return "\n".join(lines)


# ── Hook handler ──────────────────────────────────────────────────────

def _on_session_start(
    session_id: str = "",
    model: str = "",
    platform: str = "",
    **kwargs,
) -> None:
    """Hook: on_session_start.

    Fired once when a brand-new session is created. Reloads config,
    verifies external_dirs, and logs a status line.
    """
    # Reload config in case it changed between sessions
    _load_config()

    # Warn if external_dirs is not configured for system-prompt indexing
    _check_external_dirs()

    # Human-readable status to stderr/logs
    logger.info(
        "[jade-identity] Session %s started — config=%s, skills_dir=%s, "
        "registered_skills=%d",
        session_id or "unknown",
        "loaded" if _jade_config else "missing",
        "present" if SKILLS_CORE_DIR.exists() else "missing",
        len(_registered_skills),
    )


# ── Plugin entry point ────────────────────────────────────────────────

def register(ctx) -> None:
    """Register hooks, slash commands, and skills.

    Called once by the plugin loader when the plugin is enabled via
    plugins.enabled in config.yaml.
    """
    # 1. Load config at startup
    _load_config()

    # 2. Register all skill files from the core directory
    skill_count = _register_skills(ctx)

    # 3. Check whether external_dirs is configured properly
    _check_external_dirs()

    # 4. Register lifecycle hook
    ctx.register_hook("on_session_start", _on_session_start)

    # 5. Register slash commands
    ctx.register_command(
        "org",
        handler=_handle_org,
        description="Display Oracule Zero org structure as a tree.",
    )
    ctx.register_command(
        "whoami",
        handler=_handle_whoami,
        description="Display Jade's identity and current role.",
    )
    ctx.register_command(
        "oracule-status",
        handler=_handle_oracule_status,
        description="Show Oracule Zero configuration and skill status.",
    )

    logger.info(
        "jade-identity plugin registered: %d skills, 3 slash commands, 1 hook",
        skill_count,
    )