Configure Jade's Discord gateway.
Hermes has Discord support built in. We are configuring it,
not rebuilding it.

STEP 1 — Read the existing Discord adapter.
Find and read the Discord gateway plugin or adapter in the repo.
Navigate to plugins/platforms/ or gateway/ or wherever Discord
configuration lives based on what you found in Session 1.
Show me:
(a) Every config key the Discord adapter accepts
(b) Where the bot token is set
(c) How channels are mapped to message types
(d) The guild-scoped allowlist security feature and how to configure it

STEP 2 — Create the config file.
Based on what you read, create the appropriate config file
for Jade's Discord setup.

The config must specify:

- Bot name: "Jade"
- Token: "[JADE_DISCORD_TOKEN]" — placeholder, user fills this in
- Guild allowlist: scoped to user's guild only (CVSS 8.1 fix)
- Channel mapping:
  bridge → general conversation (default)
  alerts → urgent items only (VM health, approvals needed)
  org-pulse → Agent-Converse progress entries auto-posted here
  decisions → permanent decisions mirrored from Agent-Converse
  scratch → no auto-posting, user personal channel
- Message formatting:
  Max length: 400 characters
  Alert prefix: 🔴
  Completion prefix: ✅  
   Approval needed prefix: ⚠️
  Discovery prefix: 💡
  Use Discord markdown for code blocks

STEP 3 — Create a setup guide.
File: ~/.oracule/setup/discord-setup.md

Write this guide in plain, step-by-step language.
Assume the user has never used Discord before.
Cover:

1. Creating a Discord account (discord.com/register)
2. Creating a new Discord server named "Oracule Zero"
3. Creating these 5 starter channels (in order):
   #bridge, #alerts, #org-pulse, #decisions, #scratch
4. Going to discord.com/developers/applications
5. Creating a new application named "Jade"
6. Going to Bot tab, clicking "Add Bot"
7. Copying the bot token
8. Going to OAuth2 tab, selecting bot scope,
   selecting: Send Messages, Read Message History,
   Embed Links, Mention Everyone, Use Slash Commands
9. Copying the OAuth2 URL and opening it to invite Jade
   to the server
10. Running: hermes gateway discord (or the correct command
    based on what you found in Step 1)
11. Testing by typing "hello" in #bridge

Include troubleshooting section:

- Bot shows offline → check token is correctly set
- Bot in wrong server → re-invite with correct OAuth URL
- Messages not appearing → check channel permissions

Write the guide completely. No skipped steps.
