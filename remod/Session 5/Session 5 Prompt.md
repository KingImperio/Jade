We need to create a Jade identity plugin for hermes-agent.

Before writing any code, do this in order:

STEP 1 — Read AGENTS.md completely.
Extract and show me:
(a) The exact plugin rules (what plugins can and cannot do)
(b) The list of core files we cannot modify
(c) Any guidelines about plugin registration or hooks

STEP 2 — Read two existing plugins.
Navigate to plugins/ and find two plugins that are relatively
simple. Read their complete file structure.
For each plugin show me:
(a) Every file in the plugin directory
(b) The full content of **init**.py
(c) The full content of plugin.py
(d) How the plugin registers itself with the framework
(e) What hooks or events it listens to

STEP 3 — Only after reading, design the plugin.
Show me your proposed design before writing any code:
(a) File structure for plugins/jade-identity/
(b) What **init**.py will contain
(c) What plugin.py will do step by step
(d) Which hooks it will use (based on what you saw in step 2)
(e) How it will load ~/.oracule/agents/jade/config.yaml
Wait for my confirmation before writing code.

STEP 4 — Write the plugin.
After I confirm, write each file completely:

plugins/jade-identity/**init**.py
plugins/jade-identity/plugin.py
plugins/jade-identity/README.md

The plugin must:

- Load ~/.oracule/agents/jade/config.yaml at startup
- Inject Jade's identity into the system prompt without
  replacing the base prompt (append only)
- Register a /org command that reads config.yaml and displays
  the org structure as a clean text tree
- Register a /whoami command that displays Jade's identity
  and current role
- NOT modify any core files
- Follow the exact same registration pattern as the existing
  plugins you read in Step 2

The system prompt injection text to add:
"You are Jade, Executive Orchestrator of Oracule Zero — a
multi-agent autonomous organization. You coordinate department
heads (Vex, Solleos, Meridian, Cassius, Prism, Lumen, Aegis)
and their worker teams to accomplish goals for your founder, S.B.

Your operating rules live in your skill files. Your org
structure is in ~/.oracule/agents/jade/config.yaml.

Core rules: Plan before acting on significant tasks. Post
decisions to Agent-Converse. Route through department heads
— never skip tiers. Nothing irreversible without user approval."

Show complete code for each file. No placeholders.
