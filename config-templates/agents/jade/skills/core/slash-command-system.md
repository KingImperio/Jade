---

name: Oracule Zero Slash Command System
description: How to parse and handle slash commands and at-mention
routing. Activates when user input begins with / or @ or contains
these patterns anywhere in a message.
always_load: true

---

# Oracule Zero Slash Command System

## Design Philosophy

Slash commands are non-blocking by default. They do not interrupt
the main task stream unless explicitly designed to do so.
Results from non-blocking commands appear in the TUI sidebar
status pane — not injected into the main conversation.
Blocking commands (marked below) pause the current task.

The system has two input layers:
/ commands: route through Jade unless @agent is specified first
@ mentions: bypass Jade, go directly to the named agent

## / Commands — Full Specification

/btw [query]
Type: non-blocking, spawns micro-agent
What happens: A short-lived subagent spins up, reads the
relevant file/config/state needed to answer the query,
replies, then terminates. The main task continues uninterrupted.
Result location: TUI sidebar notification pane, not main chat
Examples:
/btw check the base_url in config.json for xovadev
/btw how much of the Groq daily budget have we used
/btw what did we last decide about the auth module
Micro-agent behavior: 1. Parse the query to identify what needs reading 2. Read only the minimal relevant source 3. Format a one-to-three sentence answer 4. Post to sidebar 5. Terminate — do not persist

/diverge [topic]
Type: non-blocking, preserves current state
What happens: Jade checkpoints the current task state,
then branches attention to the new topic. The original
task is paused (not cancelled) and queued for resumption.
Use when: Fola wants to explore a new direction without
losing the current thread.
Jade response: "Checkpointed [current task]. Diverging to
[topic]. Use /resume to return."

/consider [note]
Type: non-blocking, background injection
What happens: The note is written to the current session's
Ghost file as a planning annotation. Jade factors it into
the current task's next decision point without interrupting.
Does not produce immediate output — acknowledged with ✓ only.
Example: /consider we should use Paystack instead of Stripe
for Nigerian users specifically

/pause
Type: BLOCKING
State machine behavior:
If agent is mid-file-write: finish the current file completely,
then pause. Never leave a file half-written.
If agent is mid-inference: complete the current token stream,
then pause.
If agent is mid-tool-call: complete the tool call,
then pause.
After pausing: git checkpoint via Mage, write progress entry
to Agent-Converse, confirm to Fola on Discord.
System stays paused until /approve or explicit resume command.

/why
Type: non-blocking
What happens: Jade explains the reasoning behind the last
action taken. Reads from the Ghost file for the current
session to reconstruct the decision chain.
Output: posted to main conversation (this command IS
a conversation — it expects Fola to read it)

/audit [scope]
Type: non-blocking
Scope options:
/audit — current task only
/audit [project name] — full project history
/audit decisions — only decision entries
/audit failures — only failure entries
/audit security — only security_incident entries
What happens: Calls read_entries() and search_entries()
on Agent-Converse for the specified scope, summarizes
key entries in reverse chronological order.
Output: posted to main conversation

/status
Type: non-blocking
What happens: Two things in parallel: 1. Aurelius reports Oracle VM metrics (RAM, CPU, disk,
network, container health) 2. Jade calls get_org_status() on Agent-Converse to show
what every active agent is currently doing
Output: formatted table in main conversation

/recall [query]
Type: non-blocking
What happens: Searches both Agent-Converse (search_entries)
and Jade's personal memory files for content matching
the query. Returns top 5 most relevant results with
their source (Agent-Converse vs personal memory) and
timestamps.
Example: /recall what did we decide about the database choice

/commit
Type: non-blocking
What happens: Calls Mage to create a git checkpoint commit
of the current working state. Commit message auto-generated
from the current task description in the Ghost file.
Reports the commit hash to sidebar.
Use before any risky operation.

/preview
Type: non-blocking
What happens: Calls Solleos Space to spin up a prototype
preview URL for the current frontend project.
Aurelius handles the temp container deployment.
URL posted to Discord #previews and sidebar.
Requires: an active frontend project context

/approve
Type: BLOCKING (releases a blocked operation)
What happens: Releases the pending operation that was
waiting for Fola approval. Jade logs the approval to
Agent-Converse and proceeds with the approved action.
Only valid when there is an active approval request.

/deny
Type: BLOCKING (cancels a blocked operation)
What happens: Cancels the pending operation. Jade writes
a decision entry to Agent-Converse noting the denial,
then asks Fola what alternative to pursue if relevant.

/remind [content]
Type: non-blocking
What happens: Writes a memory entry to Agent-Converse
with priority=high. Jade will surface this note at the
start of the next relevant session automatically.
Also writes to Ghost file for current session awareness.
Example: /remind we should not forget adding skills
for each agent. The skill architecture itself
is another thing.

/skip
Type: BLOCKING
What happens: Cleanly abandons the current subtask.
Does not kill processes mid-operation — waits for the
current atomic unit to complete.
Moves to the next queued task.
Writes a failure entry to Agent-Converse noting
what was skipped and why (asks Jade to log reason).

/handoff [agent] [task description]
Type: non-blocking
What happens: Jade writes a handoff entry to Agent-Converse
targeting the specified agent. The task description becomes
the handoff content. The target agent will read this on
their next spawn via get_handoff().
Example: /handoff solleos redesign the dashboard header
to be more minimal, reference the current design
in /projects/atlas-ui/src/components/Header.tsx

## @ Mentions — Routing Specification

Format: @[agent-name] [message]
Valid targets: jade atlas vex solleos meridian cassius prism
lumen aegis xovadev mage aurelius diviner
tianyan leizhi

Behavior:
Message goes directly to the named agent's input stream.
Jade is CC'd passively via an Agent-Converse progress entry.
Jade does NOT intercept or modify the message.
The named agent responds directly to Fola

Use @ when:
You know exactly which agent you need.
You want to bypass Jade's routing for speed.
You want a direct answer from a specific specialist.

Examples:
@xovadev are there any TODO comments in the auth module
@aurelius how much RAM is the Oracle VM using right now
@solleos make the dashboard header more minimal
@mage what changed in the last three commits
@meridian find me the top five fintech APIs operating in Nigeria
@leizhi trigger the weekly analytics report workflow
@atlas review the last five skill promotion candidates

## Extensibility

New slash commands can be added by writing a plugin that
registers command handlers using the Jade plugin hook system.
Each new command must be documented in this skill file.
Custom commands created by Fola or derived from usage patterns
should be added here by Jade after Atlas validates them.