# Session 2: Rebranding Report — Jade-ization Complete

**Date:** 2026-05-15
**Tag:** By DpSkV4 (continuing from Session 1 codebase read)

---

## Overview

Completed the full Jade-ization of the Hermes Agent fork. Theme overhaul (green/cyan/silver/purple), install pipeline redirection to `KingImperio/Jade`, CLI help text renamed, and comprehensive audit closing all critical upstream references.

---

## Completed Work

### 1. Theme Overhaul

| File | Changes |
|------|---------|
| `hermes_cli/skin_engine.py` | Default skin colors switched from gold/amber (`#FFD700`, `#CD7F32`, `#B8860B`) to green/cyan/silver/purple (`#00E676`, `#00BCD4`, `#E0E0E0`, `#7C4DFF`). Description updated. |
| `ui-tui/src/theme.ts` | `DARK_THEME` and `LIGHT_THEME` fully updated: `primary` → `#00E676`, `accent` → `#7C4DFF`, `border` → `#00C853`, `text` → `#E0E0E0`, `muted` → `#9E9E9E`, `label` → `#00BCD4`. Status bar, completions, diffs, shell dollar aligned. |
| `remod/jade_theme_preview.html` | 302-line HTML demo showing the full theme across logo art, CLI banner, status bar, session panel, tool feed, input prompt, response box. |

### 2. Install/Update Pipeline

| File | Before | After |
|------|--------|-------|
| `scripts/install.sh` | `REPO_URL_SSH/HTTPS` → NousResearch, banner "Hermes Agent Installer" / "by Nous Research" | → `KingImperio/Jade`, "Jade Installer" / "by Oracule Zero" |
| `scripts/install.ps1` | Same issues | Same fixes |
| `scripts/install.cmd` | All 4 URLs → NousResearch | → `KingImperio/Jade` |
| `hermes_cli/main.py` | `OFFICIAL_REPO_URLS` → NousResearch, ZIP URL, reinstall URL, fork prompt | → `KingImperio/Jade` |
| `hermes_cli/banner.py` | `_UPSTREAM_REPO_URL`, `_RELEASE_URL_BASE` → NousResearch | → `KingImperio/Jade` |
| `hermes_cli/uninstall.py` | Reinstall URLs → NousResearch | → `KingImperio/Jade` |
| `.github/workflows/docker-publish.yml` | `IMAGE_NAME: nousresearch/hermes-agent`, all 5 `github.repository` checks | → `kingimperio/jade`, `KingImperio/Jade` |

### 3. CLI Help Text

| File | Changes |
|------|---------|
| `hermes_cli/_parser.py` | `prog="hermes"` → `prog="jade"`. Description → `"Jade - Oracule Intelligence"`. All 38 epilogue examples: `hermes` → `jade`. |

### 4. Previous Session 2 Branding (from earlier commits)

| File | Changes |
|------|---------|
| `hermes_cli/banner.py` | Version label `"Jade v{VERSION}"`, attribution `"Oracule Zero"`, docstrings |
| `hermes_cli/default_soul.py` | `"You are Jade, created by Oracule Zero."` |
| `hermes_cli/status.py` | Header `"◆ Jade Status"` |
| `hermes_cli/setup.py` | Wizard headers, prompts, `bot_name="Jade"` |
| `hermes_cli/tools_config.py` | Header `"◆ Jade Tool Configuration"` |
| `hermes_cli/uninstall.py` | Header `"◆ Jade Uninstaller"`, thank-you |
| `hermes_cli/gateway.py` | `SERVICE_DESCRIPTION`, startup banner |
| `hermes_cli/doctor.py` | Header `"◆ Jade Doctor"` |
| `hermes_cli/config.py` | Header `"◆ Jade Configuration"` |
| `hermes_cli/backup.py` | Error/warning messages |
| `hermes_cli/claw.py` | `"Migrate from OpenClaw to Jade"` |
| `hermes_cli/logs.py` | `"Logs created when Jade runs"` |
| `hermes_cli/debug.py` | `"Share with the Jade team"` |
| `hermes_cli/web_server.py` | `"Jade Web UI"` |
| `scripts/build_skills_index.py` | `"Building Jade Skills Index"` |
| `ui-tui/src/theme.ts` | BRAND: `name: 'Jade'`, `icon: '◆'` |
| `ui-tui/src/components/branding.tsx` | Banner text, session panel attribution |
| `ui-tui/src/components/appChrome.tsx` | EMOJI_FRAMES `'⚕'` → `'◆'` |
| `ui-tui/src/components/appLayout.tsx` | Status icon `⚕` → `◆` |
| `web/src/i18n/*.ts` (16 files) | `"Hermes Agent"` → `"Jade"`, `"Nous Research"` → `"Oracule Zero"` |
| `web/src/themes/presets.ts` | `"Hermes Teal"` → `"Jade Dark"` |
| `website/docusaurus.config.ts` | Title, tagline, navbar, footer |
| `skills/**/SKILL.md` (50 files) | Content `"Hermes"` → `"Jade"` |
| `optional-skills/**/SKILL.md` (13 files) | Content `"Hermes"` → `"Jade"` |
| `README.md` | Title, description, badges, install URLs, contributing section |

### 5. jade Command Alias

| File | Change |
|------|--------|
| `pyproject.toml` | Added `jade = "hermes_cli.main:main"` entry point |
| `scripts/install.sh` | Creates `jade` launcher symlink alongside `hermes` |
| `scripts/install.ps1` | Success message for `jade` command |

---

## Critical Audit

Ran comprehensive grep for `NousResearch/hermes-agent` across all `.sh`, `.ps1`, `.py`, `.yml`, `.yaml`, `.nix`, `.cmd` files after fixes.

**Result: Zero remaining matches in functional pipeline files.**

---

## Files Never Modified (Per Constraints)

| File | Reason |
|------|--------|
| `run_agent.py` | Core AIAgent class — forbidden per AGENTS.md |
| `cli.py` | HermesCLI orchestrator — forbidden |
| `gateway/run.py` | Gateway runner — forbidden |
| `hermes_cli/main.py` | Logic — forbidden; only URLs changed (non-logic) |
| All `hermes_*` imports/modules | Would break 400+ import statements |
| `get_hermes_home()` / `display_hermes_home()` | 500+ call sites |
| `HERMES_HOME` / `HERMES_*` env vars | User config compatibility |
| `HermesCLI` class | Object instantiation across codebase |

---

## Remaining Issues (Low Priority)

| File | Issue |
|------|-------|
| `pyproject.toml:6` | `name = "hermes-agent"` — would change for full PyPI rename |
| `uv.lock` | `name = "hermes-agent"` — tied to pyproject.toml |
| `nix/hermes-agent.nix` | `pname = "hermes-agent"`, homepage URL |
| `website/docusaurus.config.ts` | Site URL, edit URL, footer — full docs fork needed |
| `hermes_cli/status.py:373` | `pip install 'hermes-agent[vercel]'` — internal hint |
| `hermes_cli/doctor.py:1105-1106` | Same — internal hint |
