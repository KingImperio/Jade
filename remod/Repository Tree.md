# Jade Repository Tree

```
Jade/
│   run_agent.py                    AIAgent class and core conversation loop (~16k LOC). The heart of the agent.
│   cli.py                          JadeCLI class and interactive terminal REPL (~13.7k LOC). Rich/prompt_toolkit UI.
│   model_tools.py                  Tool orchestration layer. Exposes get_tool_definitions() and handle_function_call().
│   toolsets.py                     Defines all toolsets and _HERMES_CORE_TOOLS list. Default bundle for all platforms.
│   hermes_state.py                 SessionDB — SQLite store with FTS5 full-text search for sessions and messages.
│   hermes_constants.py             Profile-aware get_hermes_home() and display_hermes_home(). Path resolution.
│   hermes_logging.py               Centralized logging: agent.log, errors.log, gateway.log with rotation.
│   batch_runner.py                 Parallel batch processing with checkpointing and fault tolerance.
│   trajectory_compressor.py        Context compression for long conversations to stay within token limits.
│   hermes_bootstrap.py             Windows UTF-8 stdio bootstrap. No-op on POSIX.
│   utils.py                        General utility functions for paths, strings, and common operations.
│   hermes_time.py                  Timezone-aware timestamps and duration formatting.
│   toolset_distributions.py        Toolset distribution sampling for batch runs and RL training.
│   mcp_serve.py                    MCP server entry point. Exposes Jade tools to external clients.
│   rl_cli.py                       CLI for reinforcement learning training environments.
│   mini_swe_runner.py              Mini SWE agent runner for SWE-bench evaluation.
│   hermes                          Main CLI entry point script.
│   setup-hermes.sh                 POSIX installation script for standard Jade.
│   setup-oracule.sh                Installation script for Oracule Zero variant with Jade identity.
│   Dockerfile                      Multi-stage Docker build for production deployment.
│   docker-compose.yml              Orchestrates Jade with Browserless and Redis.
│   pyproject.toml                  Python package definition, dependencies, and entry points.
│   AGENTS.md                       Development guide for AI assistants. Architecture, standards, and policies.
│   README.md                       Main project readme with overview and quick start.
│   CONTRIBUTING.md                 Contribution guidelines and PR process.
│   SECURITY.md                     Security policy and vulnerability reporting.
│
├── agent/                          Agent internals (62 entries). The brain of the agent.
│   ├── prompt_builder.py           System prompt construction with tool schemas, skills, and memory.
│   ├── context_compressor.py       Summarizes conversation history to stay within token limits.
│   ├── memory_manager.py           Memory provider orchestration. Routes to honcho, mem0, supermemory.
│   ├── anthropic_adapter.py        Anthropic Claude API adapter with tool calling and thinking.
│   ├── auxiliary_client.py         Auxiliary LLM for side tasks (curator, vision, embedding, titles).
│   ├── context_engine.py           Dynamic context assembly. Manages @file, @url, @folder references.
│   ├── credential_pool.py          Multi-credential management with fallback routing.
│   ├── curator.py                  Background skill maintenance. Auto-archives stale agent-created skills.
│   ├── display.py                  KawaiiSpinner animated faces, tool output formatting, activity feed.
│   ├── prompt_caching.py           Prompt caching optimization for reduced API costs.
│   ├── redact.py                   Secret redaction. Strips API keys and credentials from output.
│   ├── tool_guardrails.py          Tool call safety. Validates arguments, prevents dangerous operations.
│   ├── trajectory.py               Conversation trajectory management. Full message history tracking.
│   ├── web_search_provider.py      Web search orchestration. Routes to Brave, Tavily, Exa, etc.
│   ├── image_gen_provider.py       Image generation provider orchestration.
│   ├── video_gen_provider.py       Video generation provider orchestration.
│   ├── memory_provider.py          MemoryProvider ABC. Interface all memory plugins implement.
│   ├── skill_commands.py           Skill slash command handlers (/skills list, install, view).
│   ├── lsp/                        Language Server Protocol integration (client, manager, servers).
│   └── transports/                 API transport layer (Anthropic, Bedrock, chat completions, Codex).
│
├── tools/                          Tool implementations (81 entries). The agent's hands.
│   ├── registry.py                 Tool registry. Zero deps. Schema collection, dispatch, availability.
│   ├── file_tools.py               read_file, write_file, patch, search_files. Primary file manipulation.
│   ├── terminal_tool.py            Shell execution with PTY. Runs commands in configurable environments.
│   ├── code_execution_tool.py      Code execution in isolated environments (Python, etc.).
│   ├── delegate_tool.py            Task delegation to subagents. Spawns isolated child agents.
│   ├── mcp_tool.py                 MCP integration. Connects to external MCP servers.
│   ├── browser_tool.py             Browser automation (navigate, click, type, scroll).
│   ├── computer_use_tool.py        CUA desktop automation. Mouse and keyboard control for GUIs.
│   ├── kanban_tools.py             Kanban work queue tools. Only exposed in worker context.
│   ├── web_tools.py                Web search and extraction tools.
│   ├── vision_tools.py             Vision/image analysis. Sends images to vision-capable models.
│   ├── image_generation_tool.py    Image generation via DALL-E, xAI, etc.
│   ├── video_generation_tool.py    Video generation tool.
│   ├── memory_tool.py              Agent memory operations.
│   ├── environments/               Terminal backends: local, Docker, SSH, Modal, Daytona, Singularity.
│   ├── browser_providers/          Browser backends: browser_use, browserbase, firecrawl.
│   └── computer_use/               CUA backend implementations with schema and wrapper.
│
├── gateway/                        Messaging gateway (23 entries). Persistent service on messaging platforms.
│   ├── run.py                      Gateway runtime. Event loop, message dispatch, session management.
│   ├── session.py                  Session lifecycle: create, resume, split, reset.
│   ├── config.py                   Configuration loading. YAML to env var bridging.
│   ├── delivery.py                 Message delivery abstraction across platforms.
│   ├── stream_consumer.py          Real-time token streaming from LLM to platform.
│   └── platforms/                  Platform adapters (34 entries).
│       ├── base.py                 Base platform ABC. Message queuing, session management, approvals.
│       ├── telegram.py             Telegram Bot with inline buttons, reactions, voice, photos.
│       ├── discord.py              Discord Bot with slash commands, components, voice, attachments.
│       ├── slack.py                Slack with slash commands and approval buttons.
│       ├── whatsapp.py             WhatsApp Cloud API adapter.
│       ├── signal.py               Signal messenger adapter.
│       ├── matrix.py               Matrix protocol with E2EE support.
│       ├── webhook.py              Generic webhook for custom integrations.
│       └── api_server.py           REST API server for programmatic access.
│
├── hermes_cli/                     CLI subcommands (79 entries).
│   ├── main.py                     Main entry point. Argparse, profiles, command routing, plugin discovery.
│   ├── commands.py                 Central slash command registry. Drives CLI, gateway, Telegram, Slack.
│   ├── config.py                   Configuration loading. DEFAULT_CONFIG, env mapping, YAML merge.
│   ├── setup.py                    Interactive setup wizard for API keys and provider selection.
│   ├── plugins.py                  Plugin manager. Discovery from ~/.hermes/plugins/, repo, pip.
│   ├── skin_engine.py              Skin/theme engine. Data-driven CLI theming via YAML.
│   ├── curses_ui.py                Curses-based interactive UI for menus.
│   ├── profiles.py                 Multi-profile management. Create, list, switch, delete.
│   ├── cron.py                     Cron CLI: list, add, edit, pause, resume, run, remove.
│   ├── curator.py                  Curator CLI: status, run, pin, archive, restore, prune.
│   ├── kanban.py                   Kanban CLI: init, create, list, assign, complete, dispatch.
│   ├── gateway.py                  Gateway management: start, stop, status, restart.
│   ├── web_server.py               Web dashboard server with PTY bridge websocket.
│   └── pty_bridge.py               PTY bridge. Spawns hermes --tui as PTY child over WebSocket.
│
├── plugins/                        Plugin system (18 entries).
│   ├── jade-identity/              Jade identity plugin. Org config, core skills, /org, /whoami.
│   ├── oracule-adz-routing/        ADZ routing plugin. Model selection with rate limit tracking.
│   ├── teams_pipeline/             Teams meeting pipeline (9 files). Pipeline, meetings, CLI.
│   ├── memory/                     Memory providers: honcho, mem0, supermemory, byterover, hindsight, holographic, openviking, retaindb.
│   ├── model-providers/            30+ inference backends: anthropic, openai, gemini, deepseek, nous, nvidia, bedrock, etc.
│   ├── web/                        Search providers: brave_free, ddgs, exa, firecrawl, parallel, searxng, tavily.
│   ├── kanban/                     Kanban dashboard web UI and systemd service file.
│   ├── observability/              Langfuse integration for traces and metrics.
│   └── platforms/                  Additional platforms: google_chat, irc, line, teams.
│
├── skills/                         Built-in skills (25 categories). Loaded on demand or always.
│   ├── github/                     GitHub: auth, code review, issues, PR workflow, repo management.
│   ├── mcp/                        MCP: native server configuration and usage.
│   ├── software-development/       Dev: debugging, TDD, code review, planning, subagent-driven-dev.
│   ├── creative/                   Creative (20 entries): ASCII art, manim, p5js, pixel art, excalidraw.
│   ├── devops/                     DevOps: kanban-orchestrator, kanban-worker, webhook-subscriptions.
│   ├── productivity/               Productivity: Airtable, Google Workspace, Linear, Notion, OCR.
│   └── research/                   Research: arxiv, blogwatcher, LLM wiki, Polymarket, paper writing.
│
├── optional-skills/                Niche skills NOT active by default (18 categories).
│   ├── blockchain/                 Blockchain: EVM and Solana development.
│   ├── finance/                    Finance: 3-statement model, DCF, LBO, comps, Excel/PPTX authoring.
│   ├── security/                   Security: 1Password, OSS forensics, Sherlock OSINT.
│   └── mlops/                      MLOps: Accelerate, Chroma, FAISS, PEFT, PyTorch FSDP, TRL, Unsloth.
│
├── tests/                          Pytest test suite (~17k tests, ~900 files).
│   ├── conftest.py                 Pytest config with autouse fixtures. HERMES_HOME isolation, TZ=UTC.
│   ├── agent/                      Agent unit tests (88 files). Adapters, compression, memory, curator.
│   ├── gateway/                    Gateway tests (247 files). All platform adapters, sessions, delivery.
│   ├── hermes_cli/                 CLI tests (207 files). Setup, profiles, config, models, kanban.
│   ├── tools/                      Tool tests (214 files). All tools, environments, MCP, browser.
│   ├── cron/                       Cron tests (14 files). Scheduler, jobs, script injection.
│   ├── e2e/                        End-to-end tests (5 files). Matrix, Discord, platform commands.
│   └── stress/                     Stress/load tests. Concurrency, fuzzing, subprocess E2E.
│
├── cron/                           Scheduled jobs system.
│   ├── jobs.py                     Job store (SQLite). Cron expressions, duration phrases, ISO timestamps.
│   └── scheduler.py                Scheduler tick loop. Catchup windows, grace periods, 3-min hard interrupt.
│
├── environments/                   RL training environments and benchmarks.
│   ├── hermes_swe_env/             SWE benchmark environment for SWE-bench tasks.
│   ├── benchmarks/                 Benchmark configs: tblite, terminalbench_2, yc_bench.
│   └── tool_call_parsers/          Model-specific parsers: deepseek, qwen, llama, mistral, kimi, glm.
│
├── ui-tui/                         Ink (React) terminal UI. TypeScript/React for hermes --tui.
│   ├── src/
│   │   ├── entry.tsx               Ink app entry point.
│   │   ├── app.tsx                 Main app. Transcript, composer, sidebar, status panels.
│   │   ├── gatewayClient.ts        JSON-RPC client. Communicates with Python TUI gateway over stdio.
│   │   ├── components/             UI components (22 files). Messages, tool activity, prompts, picker.
│   │   ├── hooks/                  React hooks (5 files).
│   │   └── lib/                    Utilities: clipboard, editor, emoji, messages, RPC, text.
│   └── packages/hermes-ink/        Forked Ink terminal rendering engine.
│
├── tui_gateway/                    Python JSON-RPC backend for TUI.
│   ├── server.py                   JSON-RPC server. Handles Ink requests, manages sessions and tools.
│   ├── entry.py                    Entry point. Starts the TUI gateway process.
│   └── slash_worker.py             Slash command worker. Runs commands in isolated subprocesses.
│
├── web/                            React dashboard web app (Vite + TypeScript).
│   ├── src/
│   │   ├── App.tsx                 Main app with sidebar, chat pane, status panels.
│   │   ├── components/             React components (19 files). ChatSidebar, ModelPickerDialog, ToolCall.
│   │   ├── pages/                  Page components (12 files). ChatPage, SettingsPage, SessionsPage.
│   │   ├── i18n/                   Internationalization for 16+ languages.
│   │   └── plugins/                Web plugin system for dashboard extensions.
│
├── website/                        Docusaurus documentation site with i18n.
│   └── docs/
│       ├── user-guide/             User docs: CLI, config, profiles, TUI, security, features, messaging.
│       ├── developer-guide/        Dev docs: architecture, adding tools/providers/platforms, plugins.
│       └── reference/              Reference: CLI commands, env vars, model catalog, tools, toolsets.
│
├── acp_adapter/                    ACP server for VS Code / Zed / JetBrains IDE integration.
│   └── server.py                   ACP protocol server. Implements Agent Communication Protocol.
│
├── scripts/                        Build, test, release, and utility scripts (21 entries).
│   ├── run_tests.sh                Test runner with CI-parity. Unsets credentials, TZ=UTC, 4 xdist workers.
│   ├── install.sh                  POSIX installation script.
│   ├── install.ps1                 Windows installation script (PowerShell).
│   ├── release.py                  Release automation.
│   ├── build_model_catalog.py      Model catalog builder.
│   └── build_skills_index.py       Skills index builder.
│
├── remod/                          Re-modelling session artifacts (6 sessions).
│   ├── Session 1/                  Initial remodelling notes.
│   ├── Session 2/                  Session 2 artifacts.
│   ├── Session 3/                  Session 3 artifacts.
│   ├── Session 4/                  Core skill files: oracule-rules, agent-converse-protocol, slash-commands, injection-guard, time-consciousness.
│   ├── Session 5/                  Jade identity plugin design and implementation.
│   ├── Session 6/                  Oracule ADZ Routing plugin design and implementation.
│   ├── kanban_boards/              Kanban board markdown files for project tracking.
│   └── jade_theme_preview.html     Jade theme preview HTML visual mockup.
│
├── providers/                      Legacy provider base class. Superseded by plugins/model-providers/.
├── locales/                        i18n translation YAML files for 16 languages.
├── config-templates/               Configuration templates for agents, global settings, setup guides.
├── .github/                        GitHub workflows, issue templates, CI configuration.
├── nix/                            Nix package definitions (hermes-agent, TUI, web, devShell).
├── packaging/                      Homebrew packaging formula.
├── docker/                         Docker entrypoint script and SOUL.md.
├── assets/                         Static assets (banner.png).
├── acp_registry/                   ACP registry metadata (agent.json, icon.svg).
├── plans/                          Planning documents.
└── datagen-config-examples/        Example configurations for data generation.
```
