Create the experience recall plugin for Jade.
Location: plugins/experience-recall/

This plugin manages Jade's permanent incident documentation
and experience recall system.

Read the existing plugin structure from plugins/ first.
Confirm the registration pattern before writing.

WHAT THE PLUGIN DOES:

1. After task completion hook:
   After every completed task, check if Jade encountered any of:
   - Errors or failures
   - Wrong initial assumptions
   - Novel solutions worth remembering
   - Situations that required escalation
     If any of the above occurred, prompt Jade to document them.

2. Writes incidents to two files:
   ~/.oracule/agents/jade/experience/incidents.md (running log)
   ~/.oracule/agents/jade/experience/never-do.md (distilled rules)

3. Incident format in incidents.md:

   ## INC-[YEAR]-[SEQ] | [DATE] | Jade

   **Situation:** [what was happening]
   **Initial assumption:** [what was assumed — mark WRONG if incorrect]
   **What made it worse:** [if applicable, else omit]
   **Root cause:** [actual cause]
   **Resolution steps:** [numbered list]
   **Escalated to:** [who, or "No"]
   **Time lost to wrong path:** [if applicable]
   **Never do:** [rule derived from this]
   **Prevention:** [how to catch this earlier]

4. Never-do format in never-do.md:

   # Jade — Never Do List
   - [Rule] (ref: INC-[YEAR]-[SEQ])

5. Commands to register:
   /incident — manually trigger incident documentation for
   the current or last completed task
   /recall-experience [query] — search incidents.md for past
   experiences matching the query
   Returns top 3 most relevant incidents

6. Auto-sequence numbering:
   Read existing incidents.md to find the highest INC number,
   increment by 1 for new entries.
   If file does not exist, start at INC-2026-001.

Plugin must not modify core files.
Show complete code for every file before writing.
