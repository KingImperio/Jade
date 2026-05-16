# Session 8: Experience Recall Plugin - Implementation Summary

## Files Created

### 1. `plugins/experience-recall/__init__.py`
Plugin entry point. Registers `post_tool_call` hook for auto-detection of error signals and two slash commands (`/incident`, `/recall-experience`).

### 2. `plugins/experience-recall/recall.py`
Core recall engine:
- `write_incident()`: Writes structured incident to incidents.md with auto-sequencing (INC-YYYY-NNN), updates never-do.md if a rule is derived
- `search_incidents()`: Keyword-based search across incidents, returns top N most relevant matches
- `_get_next_incident_number()`: Reads existing incidents to find highest sequence number, increments by 1
- `_ensure_files()`: Creates experience directory and initializes files if they don't exist

### 3. `plugins/experience-recall/plugin.yaml`
Plugin metadata: name, version, description, author, hooks, and commands.

### 4. `plugins/experience-recall/README.md`
Documentation covering features, incident format, never-do format, slash commands, and usage examples.

## How It Works

1. **Auto-detection**: The `post_tool_call` hook inspects every tool result for error signals (error, failed, failure, exception, traceback, etc.). When detected, logs a note suggesting `/incident` documentation.

2. **Manual incident**: `/incident` accepts key=value arguments (situation, assumption, root_cause, resolution, etc.) and writes a structured incident block. Without arguments, returns a template.

3. **Experience search**: `/recall-experience <query>` splits the query into keywords, scores each incident by keyword overlap, and returns the top 3 most relevant.

4. **Auto-sequencing**: Reads incidents.md for existing INC-YYYY-NNN patterns, finds the maximum, and increments. Starts at INC-2026-001 if no incidents exist.

5. **Never-do rules**: When an incident includes a "never_do" field, the rule is automatically appended to never-do.md with a reference back to the incident ID. Duplicate rules are skipped.

## Files Created by Plugin (at runtime)

- `~/.oracule/agents/jade/experience/incidents.md` — Running incident log (auto-created on first use)
- `~/.oracule/agents/jade/experience/never-do.md` — Distilled prevention rules (auto-created on first use)
