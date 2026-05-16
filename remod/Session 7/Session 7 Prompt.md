Create a standalone Python MCP server project.
This is NOT inside the hermes-agent repo.
Create it at: ~/oracule-zero/agent-converse-mcp/

This MCP server is the sole writer to the Agent-Converse SQLite
database. All Oracule Zero agents connect to it as MCP clients.

CRITICAL: SQLite must run with WAL mode enabled from first
connection. This is non-negotiable — without WAL mode, concurrent
writes from multiple agents will corrupt the database.

Project structure:
agent-converse-mcp/
├── server.py — main MCP server, tool definitions
├── database.py — all SQLite operations, WAL mode setup
├── models.py — Pydantic models for all entry types
├── requirements.txt
└── README.md

DATABASE SCHEMA — implement exactly:

Table: entries
id TEXT PRIMARY KEY — format: ac*[yyyymmdd]*[author]\_[seq]
author TEXT NOT NULL — which OG wrote this
target TEXT DEFAULT 'all' — recipient: 'all' or agent name
type TEXT NOT NULL — decision/discovery/failure/progress/
alert/handoff/memory/security_incident
project TEXT DEFAULT 'global'
priority TEXT DEFAULT 'normal' — low/normal/high/urgent
ttl_hours INTEGER — null = permanent
tags TEXT — comma-separated
timestamp TEXT NOT NULL — ISO 8601
session_id TEXT
content TEXT NOT NULL — summary + filepath, never raw content
references TEXT — comma-separated entry IDs
source TEXT DEFAULT 'internal' — internal or external
expires_at TEXT — computed from timestamp + ttl_hours

Table: flagged_sites
url TEXT PRIMARY KEY
flagged_by TEXT
timestamp TEXT
reason TEXT
injection_text TEXT
task_context TEXT
confirmed_dangerous INTEGER DEFAULT 0
official_blacklist INTEGER DEFAULT 0

Table: visited_sites
id INTEGER PRIMARY KEY AUTOINCREMENT
url TEXT
timestamp TEXT
agent TEXT
task TEXT
goal_achieved INTEGER
useful INTEGER
promoted_to_trusted INTEGER DEFAULT 0
summary TEXT

Table: trusted_sites
url TEXT PRIMARY KEY
trust_level TEXT DEFAULT 'session' — session/project/always
categories TEXT
added_by TEXT
approved_by TEXT
timestamp TEXT
notes TEXT

MCP TOOLS to implement (8 total):

write_entry(author, type, content, project, target,
ttl_hours, tags, source) → entry_id
Validates type is one of the valid types.
Computes expires_at from ttl_hours.
WAL-safe write.

read_entries(target, project, type, since_hours, limit) → list
Returns entries matching filters.
Excludes expired entries automatically.
Default limit: 20.

search_entries(query, project, tags) → list
Full-text search across content field.
Filter by tags if provided.

get_handoff(target_agent, project) → entry or null
Returns the most recent unread handoff targeting this agent.
Marks it as read after retrieval.

expire_entries() → count
Deletes all entries where expires_at < now.
Called by Aurelius on a cron schedule.

get_org_status() → dict
Returns snapshot of all active progress entries grouped
by author. Shows what each agent is currently doing.

flag_site(url, reason, agent, injection_text, task_context) → ok
Writes to flagged_sites table.
Also writes a security_incident entry to entries table.

get_flagged_sites(confirmed_only) → list
Returns flagged sites. If confirmed_only=True, only returns
confirmed dangerous sites.

Write complete working Python code for every file.
Use the official mcp Python SDK.
No placeholders. No TODO comments.
Show each file completely before writing to disk.
