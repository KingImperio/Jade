"""
Router for Oracule ADZ Routing plugin.

Handles model selection based on task type and rate limits.
"""

import json
import logging
import os
import threading
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Paths — Issue 6: allow ORACULE_HOME override via env var
_ORACULE_HOME = Path(os.environ.get("ORACULE_HOME", str(Path.home() / ".oracule")))
ORACULE_GLOBAL = _ORACULE_HOME / "global"
ORACULE_STATE = _ORACULE_HOME / "state"
ORACULE_LOGS = _ORACULE_HOME / "logs"

ROUTING_YAML = ORACULE_GLOBAL / "routing.yaml"
BUDGET_YAML = ORACULE_GLOBAL / "budget.yaml"
RATE_LIMITS_FILE = ORACULE_STATE / "rate-limits.json"
ROUTING_DECISIONS_LOG = ORACULE_LOGS / "routing-decisions.jsonl"

# Ensure directories exist — deferred until first use to avoid side effects at import
_directories_initialized = False


def _ensure_directories() -> None:
    """Create state and log directories if they don't exist."""
    global _directories_initialized
    if not _directories_initialized:
        ORACULE_STATE.mkdir(parents=True, exist_ok=True)
        ORACULE_LOGS.mkdir(parents=True, exist_ok=True)
        _directories_initialized = True


# Issue 2: Provider name mapping — model prefix → budget.yaml key
MODEL_TO_BUDGET_PROVIDER = {
    "google": "google_gemini",
    "xai": "xai",
    "groq": "groq",
    "mistral": "mistral",
    "nvidia": "nvidia_nim",
    "deepseek": "deepseek",
    "cerebras": "cerebras",
    "cloudflare": "cloudflare_workers_ai",
    "poolside": "poolside",
    "inclusion": "inclusion",
    "minimax": "minimax",
    "stepfun": "stepfun",
}


def load_yaml(path: Path) -> dict:
    """Load YAML file, return empty dict if not found or error."""
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def load_json(path: Path) -> dict:
    """Load JSON file, return empty dict if not found or error."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_json(path: Path, data: dict) -> None:
    """Save data to JSON file."""
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_provider_from_model(model: str) -> str:
    """Extract provider from model string and map to budget.yaml key."""
    prefix = model.split("/")[0] if "/" in model else "unknown"
    return MODEL_TO_BUDGET_PROVIDER.get(prefix, prefix)


class RateLimiter:
    """Tracks rate limits per provider and resets at midnight UTC."""

    def __init__(self):
        self._lock = threading.Lock()  # Issue 1: thread safety
        self.budget_config = load_yaml(BUDGET_YAML)
        self.usage = self._load_usage()
        self.last_reset = self._load_last_reset()
        self._check_reset()

    def _load_usage(self) -> dict:
        """Load usage from file."""
        return load_json(RATE_LIMITS_FILE)

    def _load_last_reset(self) -> str:
        """Load last reset date from usage file or default to today."""
        usage = self._load_usage()
        return usage.get("_last_reset", datetime.now(timezone.utc).date().isoformat())

    def _check_reset(self) -> None:
        """Reset usage if the day has changed. Must be called under lock."""
        today = datetime.now(timezone.utc).date().isoformat()
        if self.last_reset != today:
            self.usage = {}
            self.last_reset = today
            self._save_usage()

    def _save_usage(self) -> None:
        """Save usage to file with last reset date. Must be called under lock."""
        self.usage["_last_reset"] = self.last_reset
        save_json(RATE_LIMITS_FILE, self.usage)

    def get_usage(self, provider: str) -> int:
        """Get current usage for provider."""
        with self._lock:
            self._check_reset()
            return self.usage.get(provider, 0)

    def increment_usage(self, provider: str, amount: int = 1) -> None:
        """Increment usage for provider. Thread-safe."""
        with self._lock:
            self._check_reset()
            self.usage[provider] = self.usage.get(provider, 0) + amount
            self._save_usage()

    def get_limit(self, provider: str) -> Optional[int]:
        """Get daily request limit for provider from budget config."""
        provider_config = self.budget_config.get("api_budgets", {}).get(provider, {})
        return provider_config.get("daily_requests")

    def get_warn_percent(self, provider: str) -> int:
        """Get warn percentage for provider."""
        provider_config = self.budget_config.get("api_budgets", {}).get(provider, {})
        return provider_config.get("warn_at_percent", 80)

    def get_hard_stop_percent(self, provider: str) -> int:
        """Get hard stop percentage for provider."""
        provider_config = self.budget_config.get("api_budgets", {}).get(provider, {})
        return provider_config.get("hard_stop_at_percent", 100)

    def is_provider_available(self, provider: str) -> Tuple[bool, str]:
        """
        Check if provider is available based on usage and limits.
        Returns (available, reason).
        """
        with self._lock:
            self._check_reset()
            limit = self.get_limit(provider)
            if limit is None:
                return True, "no_daily_limit"

            usage = self.usage.get(provider, 0)
            if usage >= limit:
                return False, "hard_limit_exceeded"

            warn_percent = self.get_warn_percent(provider)
            hard_stop_percent = self.get_hard_stop_percent(provider)

            if usage >= limit * (hard_stop_percent / 100):
                return False, "hard_stop_threshold"

            if usage >= limit * (warn_percent / 100):
                # Issue 3: Log warning to Hermes logger when threshold hit
                logger.warning(
                    "ADZ Routing: provider '%s' at %.0f%% of daily limit "
                    "(%d/%d). Agent should call write_entry(type='alert') "
                    "to notify via Agent-Converse.",
                    provider,
                    (usage / limit * 100),
                    usage,
                    limit,
                )
                return True, "warning_threshold"

            return True, "within_limits"


class Router:
    """Main router for model selection."""

    def __init__(self):
        _ensure_directories()
        self.routing_config = load_yaml(ROUTING_YAML)
        self.rate_limiter = RateLimiter()
        self.overrides: Dict[str, str] = {}  # task_type -> model

    def get_model(self, task_type: str, requesting_agent: str = "unknown") -> str:
        """
        Get the best available model for a task type.
        Falls back through primary and fallback lists.
        Logs the decision.
        """
        # Check for override
        if task_type in self.overrides:
            model = self.overrides[task_type]
            self._log_decision(task_type, model, requesting_agent, override=True)
            return model

        task_config = self.routing_config.get("task_types", {}).get(task_type, {})
        if not task_config:
            model = "nvidia/nemotron-3-super"
            self._log_decision(task_type, model, requesting_agent, fallback=True)
            return model

        primary_models = task_config.get("primary", [])
        fallback_models = task_config.get("fallback", [])

        # Try primary models
        for model in primary_models:
            provider = get_provider_from_model(model)
            available, reason = self.rate_limiter.is_provider_available(provider)
            if available:
                self._log_decision(task_type, model, requesting_agent)
                self.rate_limiter.increment_usage(provider)
                return model

        # Try fallback models
        for model in fallback_models:
            provider = get_provider_from_model(model)
            available, reason = self.rate_limiter.is_provider_available(provider)
            if available:
                self._log_decision(task_type, model, requesting_agent, fallback=True)
                self.rate_limiter.increment_usage(provider)
                return model

        # If all models are rate-limited, return the first primary model anyway (but log)
        if primary_models:
            model = primary_models[0]
            self._log_decision(task_type, model, requesting_agent, rate_limited=True)
            return model

        # Ultimate fallback
        model = "nvidia/nemotron-3-super"
        self._log_decision(task_type, model, requesting_agent, ultimate_fallback=True)
        return model

    def _log_decision(
        self,
        task_type: str,
        model: str,
        requesting_agent: str,
        override: bool = False,
        fallback: bool = False,
        rate_limited: bool = False,
        ultimate_fallback: bool = False,
    ) -> None:
        """Log routing decision to JSONL file."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": task_type,
            "model": model,
            "requesting_agent": requesting_agent,
            "provider": get_provider_from_model(model),
            "override": override,
            "fallback": fallback,
            "rate_limited": rate_limited,
            "ultimate_fallback": ultimate_fallback,
        }
        try:
            with ROUTING_DECISIONS_LOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as exc:
            # Issue 4: Replace bare except pass with logger.debug
            logger.debug("Failed to log routing decision: %s", exc)

    def set_override(self, task_type: str, model: str) -> None:
        """Set a temporary override for a task type (session-only)."""
        self.overrides[task_type] = model

    def clear_override(self, task_type: str) -> None:
        """Clear override for a task type."""
        if task_type in self.overrides:
            del self.overrides[task_type]

    def get_status(self) -> Dict[str, dict]:
        """Get current usage and limits for all providers."""
        status = {}
        for provider in self.budget_config.get("api_budgets", {}).keys():
            limit = self.rate_limiter.get_limit(provider)
            usage = self.rate_limiter.get_usage(provider)
            warn_percent = self.rate_limiter.get_warn_percent(provider)
            hard_stop_percent = self.rate_limiter.get_hard_stop_percent(provider)

            status[provider] = {
                "limit": limit,
                "usage": usage,
                "usage_percent": (usage / limit * 100) if limit else 0,
                "warn_percent": warn_percent,
                "hard_stop_percent": hard_stop_percent,
                "available": self.rate_limiter.is_provider_available(provider)[0],
            }
        return status


# Global router instance
_router = Router()


def get_model(task_type: str, requesting_agent: str = "unknown") -> str:
    """Public function to get model for a task type."""
    return _router.get_model(task_type, requesting_agent)


def set_override(task_type: str, model: str) -> None:
    """Set a temporary override for a task type."""
    _router.set_override(task_type, model)


def clear_override(task_type: str) -> None:
    """Clear override for a task type."""
    _router.clear_override(task_type)


def get_routing_status() -> Dict[str, dict]:
    """Get current routing status."""
    return _router.get_status()
