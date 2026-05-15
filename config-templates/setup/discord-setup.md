# Discord Setup for Oracule Zero

## Channels

| Channel | Purpose |
|---------|---------|
| `#bridge` | Main conversation channel — Jade and S.B. communicate here |
| `#alerts` | System alerts, incident notifications, budget warnings |
| `#agent-converse` | Cross-agent communication log (automated posts) |
| `#incidents` | Incident reports and postmortems |

## Bot Setup

1. Go to https://discord.com/developers/applications
2. Create a new application → Bot
3. Copy the bot token
4. Add bot to your server with these permissions:
   - Send Messages
   - Read Message History
   - Mention Everyone (for alerts)
   - Embed Links
5. Set bot name to "Jade"
6. Configure in `~/.oracule/agents/jade/config.yaml` under the `discord:` section

## Environment Variable

```bash
export DISCORD_BOT_TOKEN="your-bot-token-here"
```

Add this to `~/.oracule/agents/jade/.env` or your shell profile.
