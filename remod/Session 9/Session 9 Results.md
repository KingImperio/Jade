# Session 9: Discord Gateway Configuration - Implementation Summary

## Files Created

### 1. `~/.oracule/setup/discord-config.yaml`
Jade's Discord gateway configuration file with placeholder token. Specifies:
- Bot name: "Jade"
- Token: `[JADE_DISCORD_TOKEN]` — user fills this in
- Guild allowlist: `[YOUR_GUILD_ID]` — CVSS 8.1 scoped to single server
- Channel mapping: bridge (general), alerts (urgent), org-pulse (progress), decisions (permanent), scratch (personal)
- Message formatting: max 400 chars, emoji prefixes (🔴✅⚠️💡), Discord markdown enabled
- Mention safety: @everyone/@here blocked, user mentions allowed
- Slash commands: enabled

### 2. `~/.oracule/setup/discord-setup.md`
Complete step-by-step setup guide for users who have never used Discord. Covers:
1. Creating a Discord account
2. Creating the "Oracule Zero" server
3. Creating 5 starter channels (#bridge, #alerts, #org-pulse, #decisions, #scratch)
4. Discord Developer Portal navigation
5. Creating the "Jade" application
6. Adding a bot
7. Copying the bot token
8. OAuth2 URL generation with required permissions
9. Inviting Jade to the server
10. Configuring the token in discord-config.yaml
11. Starting the gateway and testing

Includes troubleshooting section for:
- Bot showing offline (token/gateway check)
- Bot in wrong server (re-invite)
- Messages not appearing (channel permissions)
- User allowlist blocking (DISCORD_ALLOWED_USERS)

## Discord Adapter Findings

### (a) Config Keys Accepted
- `discord.token` — Bot token (required)
- `discord.allowed_guilds` — Server ID allowlist (CVSS 8.1 fix)
- `discord.allowed_users` — Comma-separated user IDs
- `discord.allowed_roles` — Comma-separated role IDs
- `discord.allow_mentions.everyone` — @everyone/@here (default false)
- `discord.allow_mentions.roles` — @role pings (default false)
- `discord.allow_mentions.users` — @user pings (default true)
- `discord.allow_mentions.replied_user` — reply-ping (default true)
- `discord.slash_commands` — Enable slash commands (default true)

Environment variables: `DISCORD_ALLOWED_USERS`, `DISCORD_ALLOWED_ROLES`, `DISCORD_ALLOWED_CHANNELS`, `DISCORD_IGNORED_CHANNELS`, `DISCORD_ALLOW_BOTS`, `DISCORD_ALLOW_MENTION_*`, `DISCORD_COMMAND_SYNC_POLICY`, `DISCORD_REACTIONS`, `DISCORD_PROXY`

### (b) Bot Token Location
Set via `discord.token` in config.yaml or `DISCORD_TOKEN` env var. The adapter reads `self.config.token` in `discord.py:623`.

### (c) Channel Mapping
The Discord adapter does not have built-in channel-to-purpose mapping — it responds to messages in any channel the bot can see. Channel routing is handled at the application level (Agent-Converse posts to specific channels). The config file above documents the intended channel purposes for Jade's workflow.

### (d) Guild-Scoped Allowlist (CVSS 8.1 Fix)
The adapter enforces user access control via `DISCORD_ALLOWED_USERS` (env var) or `discord.allowed_users` (config.yaml). Without this, any Discord user who can DM the bot or message it in a shared server can interact with Jade. The fix scopes access to specific user IDs or role IDs. The `discord.dm_role_auth_guild` config key restricts role-based auth to a specific guild.
