# Jade (Oracule Zero) Repository Structure Map

> Generated: 2026-05-15
> Base: Fork of NousResearch Hermes Agent, customized for Oracule Zero multi-agent organization.

---

## Root Level

### Core Entry Points

| Path | Importance | Description |
|------|------------|-------------|
| `run_agent.py` | **Critical** | The AIAgent class and core conversation loop (~16k LOC). Drives the main AI agent with tool calling, conversation management, error recovery, and multi-provider support. The heart of the system. |
| `cli.py` | **Critical** | HermesCLI class providing the interactive terminal REPL (~13.7k LOC). Handles Rich/prompt_toolkit UI, animated spinners, skin engine, slash command dispatch, toolset selection, and session management. |
| `model_tools.py` | **Critical** | Thin orchestration layer over the tool registry. Exposes `get_tool_definitions()` and `handle_function_call()` — the public API consumed by run_agent, cli, batch_runner, and RL environments. |
| `toolsets.py` | **Critical** | Defines all toolsets and the `_HERMES_CORE_TOOLS` list. Maps tools to named toolsets, supports composition, and is the default bundle every platform inherits from. |
| `hermes_state.py` | **Critical** | SessionDB — SQLite store with FTS5 full-text search. Stores session metadata, full message history, and model config for both CLI and gateway sessions. Uses WAL mode with NFS fallback. |
| `hermes_constants.py` | **Critical** | Profile-aware `get_hermes_home()` and `display_hermes_home()` functions. Single source of truth for all HERMES_HOME paths. Import-safe with zero dependencies. |
| `hermes_logging.py` | **High** | Centralized logging setup producing agent.log (INFO+), errors.log (WARNING+), and gateway.log. Profile-aware with rotating file handlers, secret redaction, and session context tagging. |
| `batch_runner.py` | **High** | Parallel batch processing for running the agent across multiple prompts from datasets. Includes checkpointing, fault tolerance, trajectory saving, and tool usage statistics. |
| `trajectory_compressor.py` | **High** | Context compression for long conversations. Reduces token usage while preserving critical context, enabling extended sessions without hitting model limits. |
| `hermes_bootstrap.py` | **Medium** | Windows UTF-8 stdio bootstrap. First import in all entry points. No-op on POSIX systems. Ensures consistent encoding across platforms. |
| `utils.py` | **Medium** | General utility functions used across the codebase. Shared helpers for path manipulation, string formatting, and common operations. |
| `hermes_time.py` | **Medium** | Time utilities for the agent. Provides timezone-aware timestamps and duration formatting. |
| `toolset_distributions.py` | **Medium** | Toolset distribution sampling for batch runs and RL training. Enables probabilistic toolset selection for training diversity. |
| `mcp_serve.py` | **Medium** | MCP (Model Context Protocol) server entry point. Exposes Hermes tools to external MCP-compatible clients. |
| `rl_cli.py` | **Medium** | CLI for reinforcement learning training environments. Wraps the agent loop for RL fine-tuning workflows. |
| `mini_swe_runner.py` | **Medium** | Mini SWE (Software Engineering) agent runner for benchmark evaluation. Runs the agent against SWE-bench style tasks. |

### Configuration & Metadata

| Path | Importance | Description |
|------|------------|-------------|
| `pyproject.toml` | **High** | Python package definition, dependencies, build config, and entry points. The canonical source for package metadata. |
| `.env.example` | **Medium** | Template for environment variables (API keys, provider URLs). Documents all required and optional env vars. |
| `cli-config.yaml.example` | **Medium** | Example CLI configuration template. Shows all available config.yaml settings with defaults. |
| `flake.nix` / `flake.lock` | **Medium** | Nix flake for reproducible builds. Defines the development shell and package derivation. |
| `package.json` | **Medium** | Root npm package config for monorepo tooling and frontend build coordination. |
| `uv.lock` / `package-lock.json` | **Low** | Lock files for uv (Python) and npm (Node.js) package managers. Pin exact dependency versions. |
| `constraints-termux.txt` | **Low** | Termux (Android) dependency constraints. Limits packages to those available on mobile. |
| `.envrc` | **Low** | direnv configuration. Auto-activates the virtual environment when entering the directory. |
| `MANIFEST.in` / `LICENSE` | **Low** | Python source distribution manifest and license file. |

### Documentation

| Path | Importance | Description |
|------|------------|-------------|
| `AGENTS.md` | **Critical** | Development guide for AI coding assistants. Contains full architecture docs, file dependency chains, coding standards, plugin rules, testing policies, and known pitfalls. The canonical reference for contributors. |
| `README.md` | **High** | Main project readme. Overview, quick start, features, and links to documentation. |
| `CONTRIBUTING.md` | **Medium** | Contribution guidelines. PR process, coding standards, and review expectations. |
| `SECURITY.md` | **Medium** | Security policy. Vulnerability reporting process and responsible disclosure guidelines. |
| `README.zh-CN.md` | **Low** | Chinese translation of the main readme. |
| `hermes-already-has-routines.md` | **Low** | Internal note documenting existing routines and capabilities. |
| `RELEASE_v0.*.md` (12 files) | **Low** | Historical release notes from v0.2.0 through v0.13.0. Track feature additions and breaking changes per version. |

### Build & Deployment

| Path | Importance | Description |
|------|------------|-------------|
| `hermes` | **High** | Main CLI entry point script. The executable invoked as `hermes <command>`. |
| `Dockerfile` | **Medium** | Docker image definition. Multi-stage build for production deployment. |
| `docker-compose.yml` | **Medium** | Docker Compose configuration. Orchestrates Hermes with supporting services (Browserless, Redis). |
| `setup-hermes.sh` | **Medium** | POSIX installation script for the standard Hermes Agent variant. |
| `setup-oracule.sh` | **Medium** | Installation script for the Oracule Zero variant. Configures Jade identity and Oracule-specific plugins. |

---

## Root Directories

| Path | Importance | Description |
|------|------------|-------------|
| `agent/` | **Critical** | Agent internals (62 entries). Provider adapters, memory management, context compression, prompt building, credential pooling, curator, LSP integration, and transport layers. The brain of the agent. |
| `tools/` | **Critical** | Tool implementations (81 entries). Auto-discovered via registry.py. Includes file ops, terminal execution, browser automation, web search, delegation, MCP, and environment backends. The agent's hands. |
| `gateway/` | **Critical** | Messaging gateway (23 entries). Platform adapters for Telegram, Discord, Slack, WhatsApp, Signal, Matrix, and 20+ more platforms. Runs the agent as a persistent service on messaging platforms. |
| `hermes_cli/` | **Critical** | CLI subcommands (79 entries). Setup wizard, plugin loader, skin engine, kanban CLI, cron management, profile switching, gateway management, and the web dashboard server. |
| `plugins/` | **Critical** | Plugin system (18 entries). Memory providers, model providers, kanban dispatcher, observability, web search, image/video gen, and custom plugins (jade-identity, oracule-adz-routing, teams_pipeline). |
| `tests/` | **Critical** | Pytest test suite (~17k tests, ~900 files). Mirrors source structure with unit, integration, E2E, and stress tests. Run via `scripts/run_tests.sh` for CI-parity. |
| `skills/` | **High** | Built-in skills (25 category directories). Organized by domain: github, mcp, devops, creative, research, productivity, software-development, etc. Loaded on demand or always via `always_load: true`. |
| `optional-skills/` | **High** | Heavier/niche skills NOT active by default (18 categories). Includes blockchain, health, migration, security, web-development. Installed explicitly via `hermes skills install`. |
| `scripts/` | **High** | Build, test, release, and utility scripts (21 entries). Includes the CI-parity test runner, installers, release automation, and model/skills index builders. |
| `cron/` | **High** | Scheduled jobs system. SQLite-backed job store with scheduler tick loop. Supports cron expressions, duration phrases, and ISO timestamps. 3-minute hard interrupt on cron sessions. |
| `environments/` | **High** | RL training environments and benchmark configurations. Includes SWE-bench environment, terminal test environment, web research environment, and model-specific tool call parsers. |
| `ui-tui/` | **Critical** | Ink (React) terminal UI source. TypeScript/React app activated via `hermes --tui`. Full replacement for the classic CLI with streaming transcript, tool activity, approvals, and session picker. |
| `tui_gateway/` | **High** | Python JSON-RPC backend for the TUI. Handles sessions, tools, model calls, and slash command execution. Communicates with Ink via newline-delimited JSON over stdio. |
| `web/` | **High** | React dashboard web app (Vite + TypeScript). Embeds `hermes --tui` via PTY bridge websocket. Provides sidebar widgets, model picker, and status panels around the embedded terminal. |
| `website/` | **Medium** | Docusaurus documentation site with i18n support. User guides, developer guides, and feature docs. |
| `acp_adapter/` | **Medium** | ACP (Agent Communication Protocol) server for VS Code / Zed / JetBrains IDE integration. Exposes the agent as an IDE coding assistant. |
| `locales/` | **Medium** | i18n translation YAML files for 16 languages (en, zh, ja, ko, de, fr, es, ru, etc.). |
| `providers/` | **Medium** | Legacy provider base class. Mostly superseded by `plugins/model-providers/`. Kept for backward compatibility. |
| `remod/` | **Medium** | Re-modelling session artifacts. Contains kanban boards, session reports, design decisions, and theme previews from 6 remodelling sessions. |
| `acp_registry/` | **Low** | ACP registry metadata (agent.json, icon.svg). |
| `config-templates/` | **Low** | Configuration templates for agents, global settings, and setup guides. |
| `nix/` | **Low** | Nix package definitions (hermes-agent, TUI, web, devShell, overlays). |
| `packaging/` | **Low** | Homebrew packaging formula. |
| `docker/` | **Low** | Docker entrypoint script and SOUL.md. |
| `assets/` | **Low** | Static assets (banner.png). |
| `plans/` | **Low** | Planning documents. |
| `datagen-config-examples/` | **Low** | Example configurations for data generation. |
| `tinker-atropos/` | **Low** | Empty directory (Atropos RL environment tinkering). |
| `hermes_agent.egg-info/` | **Low** | Python egg metadata (auto-generated by build). |
| `.venv/` | **Low** | Python virtual environment (auto-generated). |
| `.kilo/` | **Low** | Kilo AI assistant configuration. |
| `.plans/` | **Low** | Internal planning directory. |
| `.github/` | **Medium** | GitHub workflows, issue templates, and CI configuration. |

---

## agent/ — Agent Internals

### Core Agent Files

| Path | Importance | Description |
|------|------------|-------------|
| `agent/prompt_builder.py` | **Critical** | System prompt construction with tool schemas, skills, memory injection, and context references. Builds the complete prompt sent to the LLM. |
| `agent/context_compressor.py` | **Critical** | Context compression engine. Summarizes conversation history to stay within token limits while preserving critical information. |
| `agent/memory_manager.py` | **Critical** | Memory provider orchestration. Routes to honcho, mem0, supermemory, and other memory backends. Manages the memory lifecycle. |
| `agent/anthropic_adapter.py` | **Critical** | Anthropic Claude API adapter with tool calling, streaming, and thinking support. Handles Claude-specific schema and response parsing. |
| `agent/auxiliary_client.py` | **High** | Auxiliary LLM client for side tasks (curator, vision, embedding, title generation). Reads the `auxiliary` config section for per-task model routing. |
| `agent/context_engine.py` | **High** | Context engine for dynamic context assembly. Manages @file, @url, and @folder references injected into conversations. |
| `agent/credential_pool.py` | **High** | Multi-credential management with fallback routing. Manages API keys across providers and handles credential rotation. |
| `agent/curator.py` | **High** | Background skill maintenance system. Reviews agent-created skills, auto-archives stale ones, and manages skill lifecycle. |
| `agent/display.py` | **High** | KawaiiSpinner animated faces, tool output formatting, and activity feed. Controls the visual presentation during agent turns. |
| `agent/prompt_caching.py` | **High** | Prompt caching optimization for reduced API costs. Tracks cache breakpoints and ensures caching remains valid throughout conversations. |
| `agent/redact.py` | **High** | Secret redaction for logs and outputs. Strips API keys, tokens, and credentials from any text before display or storage. |
| `agent/tool_guardrails.py` | **High** | Tool call safety guardrails. Validates tool arguments, enforces path restrictions, and prevents dangerous operations. |
| `agent/trajectory.py` | **High** | Conversation trajectory management. Tracks the full message history, tool calls, and results for context window management. |
| `agent/web_search_provider.py` | **High** | Web search provider orchestration. Routes search queries to configured providers (Brave, Tavily, Exa, etc.). |
| `agent/image_gen_provider.py` | **High** | Image generation provider orchestration. Routes image generation requests to DALL-E, xAI, or other providers. |
| `agent/video_gen_provider.py` | **High** | Video generation provider orchestration. Routes video generation requests to configured providers. |
| `agent/memory_provider.py` | **High** | MemoryProvider ABC definition. The interface all memory plugins must implement. |
| `agent/skill_commands.py` | **High** | Skill slash command handlers. Implements `/skills` commands for listing, installing, and managing skills. |
| `agent/account_usage.py` | **Medium** | API account usage tracking and cost estimation. Monitors token consumption across providers. |
| `agent/bedrock_adapter.py` | **High** | AWS Bedrock provider adapter. Handles Bedrock-specific API calls and response parsing. |
| `agent/codex_responses_adapter.py` | **High** | OpenAI Codex responses API adapter. Handles the Codex-specific response format and tool calling. |
| `agent/gemini_native_adapter.py` | **High** | Google Gemini native API adapter. Handles Gemini's unique schema and response format. |
| `agent/gemini_cloudcode_adapter.py` | **High** | Gemini Cloud Code (IDE integration) adapter. |
| `agent/curator_backup.py` | **Medium** | Curator backup system. Creates pre-run tar.gz snapshots of skills before curator modifications. |
| `agent/error_classifier.py` | **Medium** | LLM error classification for retry logic. Categorizes API errors to determine retry strategy. |
| `agent/file_safety.py` | **Medium** | File operation safety guards. Prevents path traversal, symlink attacks, and writes outside allowed directories. |
| `agent/i18n.py` | **Medium** | Internationalization support. Loads translations and handles locale-specific formatting. |
| `agent/image_gen_registry.py` | **Medium** | Image generation provider registry. Manages available image generation backends. |
| `agent/image_routing.py` | **Medium** | Image generation model routing. Selects the appropriate model for image generation tasks. |
| `agent/video_gen_registry.py` | **Medium** | Video generation provider registry. |
| `agent/insights.py` | **Medium** | Agent insights and analytics. Generates usage statistics and performance metrics. |
| `agent/lmstudio_reasoning.py` | **Medium** | LM Studio reasoning integration. |
| `agent/model_metadata.py` | **Medium** | Model metadata (context lengths, capabilities, pricing). |
| `agent/models_dev.py` | **Medium** | Development model catalog. |
| `agent/nous_rate_guard.py` | **Medium** | Nous Research rate limiting guard. |
| `agent/onboarding.py` | **Medium** | Agent onboarding flow for new sessions. |
| `agent/plugin_llm.py` | **Medium** | Plugin-based LLM integration. |
| `agent/portal_tags.py` | **Low** | Portal tagging system. |
| `agent/rate_limit_tracker.py` | **Medium** | API rate limit monitoring. |
| `agent/retry_utils.py` | **Medium** | Retry logic with exponential backoff. |
| `agent/shell_hooks.py` | **Medium** | Shell command hooks and consent management. |
| `agent/skill_preprocessing.py` | **Medium** | Skill content preprocessing before injection. |
| `agent/skill_utils.py` | **Medium** | Skill utility functions (frontmatter parsing, validation). |
| `agent/subdirectory_hints.py` | **Medium** | Subdirectory context hints for workspace awareness. |
| `agent/think_scrubber.py` | **Medium** | Scrubs reasoning/thinking content from outputs. |
| `agent/title_generator.py` | **Medium** | Auto-generates session titles from conversation content. |
| `agent/tool_result_classification.py` | **Medium** | Tool result classification for context management. |
| `agent/usage_pricing.py` | **Medium** | API usage pricing calculations. |
| `agent/web_search_registry.py` | **Medium** | Web search provider registry. |
| `agent/google_code_assist.py` | **Medium** | Google Code Assist integration. |
| `agent/google_oauth.py` | **Medium** | Google OAuth flow for Gemini authentication. |
| `agent/gemini_schema.py` | **Medium** | Gemini-specific schema handling. |
| `agent/moonshot_schema.py` | **Medium** | Moonshot (Kimi) schema handling. |
| `agent/manual_compression_feedback.py` | **Medium** | User feedback loop for manual compression. |
| `agent/context_references.py` | **Medium** | Context reference tracking (@file, @url mentions). |
| `agent/credential_sources.py` | **Medium** | Credential source enumeration. |
| `agent/markdown_tables.py` | **Low** | Markdown table formatting utilities. |
| `agent/__init__.py` | **Low** | Package init. |

### agent/lsp/ — Language Server Protocol

| Path | Importance | Description |
|------|------------|-------------|
| `agent/lsp/client.py` | **High** | LSP client implementation. Connects to language servers for code intelligence. |
| `agent/lsp/manager.py` | **High** | LSP server lifecycle manager. Starts, stops, and monitors LSP servers. |
| `agent/lsp/cli.py` | **Medium** | LSP CLI interface for configuration. |
| `agent/lsp/eventlog.py` | **Medium** | LSP event logging. |
| `agent/lsp/install.py` | **Medium** | LSP server installation. |
| `agent/lsp/protocol.py` | **Medium** | LSP protocol definitions. |
| `agent/lsp/reporter.py` | **Medium** | LSP diagnostics reporter. |
| `agent/lsp/servers.py` | **Medium** | LSP server configurations. |
| `agent/lsp/workspace.py` | **Medium** | LSP workspace management. |
| `agent/lsp/__init__.py` | **Low** | Package init. |

### agent/transports/ — API Transport Layer

| Path | Importance | Description |
|------|------------|-------------|
| `agent/transports/base.py` | **High** | Base transport ABC. Defines the interface all API transports must implement. |
| `agent/transports/anthropic.py` | **High** | Anthropic Messages API transport. |
| `agent/transports/bedrock.py` | **High** | AWS Bedrock transport. |
| `agent/transports/chat_completions.py` | **High** | OpenAI-compatible chat completions transport. Used by most providers. |
| `agent/transports/codex.py` | **High** | OpenAI Codex transport. |
| `agent/transports/codex_app_server.py` | **Medium** | Codex app server session management. |
| `agent/transports/codex_app_server_session.py` | **Medium** | Codex app server session handling. |
| `agent/transports/codex_event_projector.py` | **Medium** | Codex event projection. |
| `agent/transports/hermes_tools_mcp_server.py` | **Medium** | Hermes tools exposed as MCP server. |
| `agent/transports/types.py` | **Medium** | Transport type definitions. |
| `agent/transports/__init__.py` | **Low** | Package init. |

---

## tools/ — Tool Implementations

### Core Tools

| Path | Importance | Description |
|------|------------|-------------|
| `tools/registry.py` | **Critical** | Tool registry. Zero dependencies. Handles schema collection, dispatch, availability checking, and error wrapping. Imported by all tool files. |
| `tools/file_tools.py` | **Critical** | File tools: read_file, write_file, patch, search_files. The agent's primary file manipulation interface. |
| `tools/terminal_tool.py` | **Critical** | Terminal/shell execution tool with PTY support. Runs commands in configurable environments (local, docker, ssh, modal). |
| `tools/code_execution_tool.py` | **Critical** | Code execution in isolated environments. Runs Python and other languages safely. |
| `tools/delegate_tool.py` | **Critical** | Task delegation to subagents. Spawns isolated child agents with synchronous wait. Supports single and batch (parallel) delegation. |
| `tools/mcp_tool.py` | **Critical** | MCP (Model Context Protocol) tool integration. Connects to external MCP servers and exposes their tools to the agent. |
| `tools/browser_tool.py` | **High** | Browser automation tool (navigate, click, type, scroll). Uses browser_use, browserbase, or firecrawl backends. |
| `tools/computer_use_tool.py` | **High** | Computer use (CUA) desktop automation. Controls mouse and keyboard for GUI interaction. |
| `tools/file_operations.py` | **High** | Low-level file operation implementations. |
| `tools/image_generation_tool.py` | **High** | Image generation tool. Routes to DALL-E, xAI, or other providers. |
| `tools/interrupt.py` | **High** | Agent interrupt handling. Manages /stop, /pause, and user interrupts. |
| `tools/kanban_tools.py` | **High** | Kanban multi-agent work queue tools. Only exposed when HERMES_KANBAN_TASK is set (worker context). |
| `tools/mcp_oauth.py` / `mcp_oauth_manager.py` | **High** | MCP OAuth authentication. Handles OAuth flows for MCP servers. |
| `tools/memory_tool.py` | **High** | Memory tool for agent memory operations. |
| `tools/patch_parser.py` | **High** | Patch/hunk parser for file edits. Parses unified diff format for the patch tool. |
| `tools/send_message_tool.py` | **High** | Cross-platform messaging tool. Sends messages to configured platforms. |
| `tools/skills_hub.py` | **High** | Skills hub adapter for optional skills. Manages skill installation from the official hub. |
| `tools/skills_tool.py` | **High** | Skills list/view/manage tools. |
| `tools/video_generation_tool.py` | **High** | Video generation tool. |
| `tools/vision_tools.py` | **High** | Vision/image analysis tools. Sends images to vision-capable models. |
| `tools/web_tools.py` | **High** | Web search and extraction tools. |
| `tools/approval.py` | **High** | Tool approval system for gateway platforms. Handles user approval/denial of tool calls. |
| `tools/cronjob_tools.py` | **High** | Cron job management tools. |
| `tools/clarify_tool.py` | **Medium** | Clarifying questions tool. |
| `tools/clarify_gateway.py` | **Medium** | Clarify tool gateway integration. |
| `tools/browser_cdp_tool.py` | **Medium** | Chrome DevTools Protocol browser tool. |
| `tools/browser_camofox.py` | **Medium** | Camofox browser integration. |
| `tools/browser_camofox_state.py` | **Medium** | Camofox state persistence. |
| `tools/browser_dialog_tool.py` | **Medium** | Browser dialog handling. |
| `tools/browser_supervisor.py` | **Medium** | Browser process supervisor. |
| `tools/budget_config.py` | **Medium** | Budget configuration for tool usage. |
| `tools/checkpoint_manager.py` | **Medium** | Checkpoint management for long operations. |
| `tools/credential_files.py` | **Medium** | Credential file management. |
| `tools/discord_tool.py` | **Medium** | Discord messaging tool. |
| `tools/env_passthrough.py` | **Medium** | Environment variable passthrough for tools. |
| `tools/feishu_doc_tool.py` | **Medium** | Feishu (Lark) document tool. |
| `tools/feishu_drive_tool.py` | **Medium** | Feishu drive tool. |
| `tools/file_state.py` | **Medium** | File state tracking. |
| `tools/homeassistant_tool.py` | **Medium** | Home Assistant smart home control. |
| `tools/lazy_deps.py` | **Medium** | Lazy dependency loading. |
| `tools/managed_tool_gateway.py` | **Medium** | Managed tool gateway for cloud environments. |
| `tools/microsoft_graph_auth.py` / `microsoft_graph_client.py` | **Medium** | Microsoft Graph API integration. |
| `tools/mixture_of_agents_tool.py` | **Medium** | Mixture of Agents (MoA) tool. |
| `tools/neutts_synth.py` | **Medium** | NeuTTS speech synthesis. |
| `tools/openrouter_client.py` | **Medium** | OpenRouter API client. |
| `tools/osv_check.py` | **Medium** | OSV (Open Source Vulnerabilities) checking. |
| `tools/path_security.py` | **Medium** | Path traversal security guards. |
| `tools/process_registry.py` | **Medium** | Background process registry. |
| `tools/rl_training_tool.py` | **Medium** | RL training tool. |
| `tools/schema_sanitizer.py` | **Medium** | Tool schema sanitization. |
| `tools/session_search_tool.py` | **Medium** | Session history search. |
| `tools/skill_manager_tool.py` | **Medium** | Skill management tool. |
| `tools/skill_provenance.py` | **Medium** | Skill provenance tracking. |
| `tools/skill_usage.py` | **Medium** | Skill usage telemetry (sidecar JSON). |
| `tools/skills_guard.py` | **Medium** | Skills safety guards. |
| `tools/skills_sync.py` | **Medium** | Skills synchronization. |
| `tools/slash_confirm.py` | **Medium** | Slash command confirmation. |
| `tools/tirith_security.py` | **Medium** | Tirith security policy checking. |
| `tools/todo_tool.py` | **Medium** | Todo/planning tool. Intercepted at agent level. |
| `tools/tool_backend_helpers.py` | **Medium** | Backend helper utilities. |
| `tools/tool_output_limits.py` | **Medium** | Tool output size limits. |
| `tools/tool_result_storage.py` | **Medium** | Tool result storage for large outputs. |
| `tools/transcription_tools.py` | **Medium** | Speech-to-text transcription. |
| `tools/tts_tool.py` | **Medium** | Text-to-speech tool. |
| `tools/url_safety.py` | **Medium** | URL safety checking. |
| `tools/voice_mode.py` | **Medium** | Voice mode for gateway platforms. |
| `tools/website_policy.py` | **Medium** | Website policy compliance. |
| `tools/xai_http.py` | **Medium** | xAI (Grok) HTTP client. |
| `tools/yuanbao_tools.py` | **Medium** | Yuanbao (Tencent) tools. |
| `tools/ansi_strip.py` | **Low** | ANSI escape sequence stripping. |
| `tools/debug_helpers.py` | **Low** | Debugging utilities. |
| `tools/fuzzy_match.py` | **Low** | Fuzzy string matching. |
| `tools/binary_extensions.py` | **Low** | Binary file extension list. |
| `tools/__init__.py` | **Low** | Package init. |

### tools/environments/ — Terminal Backends

| Path | Importance | Description |
|------|------------|-------------|
| `tools/environments/local.py` | **Critical** | Local shell execution environment. Runs commands on the host machine. |
| `tools/environments/base.py` | **High** | Base environment ABC. Defines the interface all terminal backends implement. |
| `tools/environments/docker.py` | **High** | Docker container environment. Runs commands in isolated Docker containers. |
| `tools/environments/ssh.py` | **High** | SSH remote execution environment. Runs commands on remote machines. |
| `tools/environments/modal.py` | **High** | Modal cloud sandbox environment. Runs commands in ephemeral cloud sandboxes. |
| `tools/environments/managed_modal.py` | **Medium** | Managed Modal environment. |
| `tools/environments/daytona.py` | **Medium** | Daytona sandbox environment. |
| `tools/environments/singularity.py` | **Medium** | Singularity/Apptainer container environment. |
| `tools/environments/vercel_sandbox.py` | **Medium** | Vercel sandbox environment. |
| `tools/environments/file_sync.py` | **Medium** | File synchronization between host and sandbox. |
| `tools/environments/modal_utils.py` | **Low** | Modal utilities. |
| `tools/environments/__init__.py` | **Low** | Package init. |

### tools/browser_providers/ — Browser Backends

| Path | Importance | Description |
|------|------------|-------------|
| `tools/browser_providers/` | **Medium** | Browser backend providers (browser_use, browserbase, firecrawl). Pluggable browser automation engines. |

### tools/computer_use/ — CUA Backend

| Path | Importance | Description |
|------|------------|-------------|
| `tools/computer_use/` | **High** | Computer Use (CUA) backend implementations. Contains the CUA backend, schema, and tool wrapper for desktop automation. |

---

## gateway/ — Messaging Gateway

### Core Gateway

| Path | Importance | Description |
|------|------------|-------------|
| `gateway/run.py` | **Critical** | Gateway runtime. Main event loop, message dispatch, session management, and slash command handling. The persistent service that runs on messaging platforms. |
| `gateway/session.py` | **Critical** | Gateway session lifecycle. Creates, resumes, splits, and resets sessions. Manages the agent lifecycle per conversation. |
| `gateway/config.py` | **High** | Gateway configuration loading. Reads user YAML and bridges config to env vars. |
| `gateway/delivery.py` | **High** | Message delivery abstraction across platforms. Handles formatting, splitting, and sending messages. |
| `gateway/stream_consumer.py` | **High** | Streaming response consumer. Handles real-time token streaming from the LLM to the platform. |
| `gateway/hooks.py` | **Medium** | Gateway hook system. Extension point for custom pre/post message processing. |
| `gateway/mirror.py` | **Medium** | Session mirroring for cron deliveries. Ensures cron deliveries don't disrupt main conversation flow. |
| `gateway/pairing.py` | **Medium** | Device pairing for gateway. |
| `gateway/platform_registry.py` | **Medium** | Platform registration and discovery. |
| `gateway/restart.py` | **Medium** | Gateway restart handling. |
| `gateway/runtime_footer.py` | **Medium** | Runtime footer for messages. |
| `gateway/session_context.py` | **Medium** | Session context management. |
| `gateway/shutdown_forensics.py` | **Medium** | Shutdown diagnostics. |
| `gateway/slash_access.py` | **Medium** | Slash command access control. |
| `gateway/status.py` | **Medium** | Gateway status tracking and scoped locks for profile isolation. |
| `gateway/sticker_cache.py` | **Low** | Sticker caching for messaging platforms. |
| `gateway/channel_directory.py` | **Medium** | Channel directory management. |
| `gateway/display_config.py` | **Medium** | Display configuration for gateway. |
| `gateway/whatsapp_identity.py` | **Medium** | WhatsApp identity management. |
| `gateway/builtin_hooks/` | **Low** | Built-in hooks (currently empty extension point). |
| `gateway/assets/` | **Low** | Gateway static assets. |
| `gateway/__init__.py` | **Low** | Package init. |

### gateway/platforms/ — Platform Adapters

| Path | Importance | Description |
|------|------------|-------------|
| `gateway/platforms/base.py` | **Critical** | Base platform adapter ABC. Message queuing, session management, approval controls. All platform adapters inherit from this. |
| `gateway/platforms/telegram.py` | **Critical** | Telegram Bot adapter with inline buttons, reactions, voice, and photo handling. |
| `gateway/platforms/discord.py` | **Critical** | Discord Bot adapter with slash commands, components, voice, and attachments. |
| `gateway/platforms/slack.py` | **High** | Slack adapter with slash commands and approval buttons. |
| `gateway/platforms/whatsapp.py` | **High** | WhatsApp adapter (Cloud API). |
| `gateway/platforms/signal.py` | **High** | Signal messenger adapter. |
| `gateway/platforms/matrix.py` | **High** | Matrix protocol adapter with E2EE support. |
| `gateway/platforms/webhook.py` | **High** | Generic webhook adapter for custom integrations. |
| `gateway/platforms/api_server.py` | **High** | REST API server for programmatic access. |
| `gateway/platforms/mattermost.py` | **Medium** | Mattermost adapter. |
| `gateway/platforms/homeassistant.py` | **Medium** | Home Assistant integration. |
| `gateway/platforms/email.py` | **Medium** | Email platform adapter. |
| `gateway/platforms/sms.py` | **Medium** | SMS platform adapter. |
| `gateway/platforms/dingtalk.py` | **Medium** | DingTalk (Alibaba) adapter. |
| `gateway/platforms/wecom.py` / `wecom_crypto.py` / `wecom_callback.py` | **Medium** | WeCom (WeChat Work) adapter suite. |
| `gateway/platforms/weixin.py` | **Medium** | WeChat adapter. |
| `gateway/platforms/feishu.py` / `feishu_comment.py` / `feishu_comment_rules.py` | **Medium** | Feishu (Lark) adapter suite. |
| `gateway/platforms/qqbot/` | **Medium** | QQ Bot adapter (8 files: adapter, crypto, keyboards, chunked upload, onboard). |
| `gateway/platforms/bluebubbles.py` | **Medium** | BlueBubbles (iMessage) adapter. |
| `gateway/platforms/yuanbao.py` / `yuanbao_proto.py` / `yuanbao_media.py` / `yuanbao_sticker.py` | **Medium** | Yuanbao (Tencent) adapter suite. |
| `gateway/platforms/msgraph_webhook.py` | **Medium** | Microsoft Graph webhook. |
| `gateway/platforms/telegram_network.py` | **Medium** | Telegram network monitoring. |
| `gateway/platforms/signal_rate_limit.py` | **Medium** | Signal rate limiting. |
| `gateway/platforms/_http_client_limits.py` | **Medium** | HTTP client limit configuration. |
| `gateway/platforms/helpers.py` | **Medium** | Shared platform helpers. |
| `gateway/platforms/ADDING_A_PLATFORM.md` | **Medium** | Guide for adding new platform adapters. |
| `gateway/platforms/__init__.py` | **Low** | Package init. |

---

## hermes_cli/ — CLI Subcommands

### Core CLI

| Path | Importance | Description |
|------|------------|-------------|
| `hermes_cli/main.py` | **Critical** | Main entry point. Argparse setup, profile handling, command routing, and plugin discovery. The `hermes` command starts here. |
| `hermes_cli/commands.py` | **Critical** | Central slash command registry (COMMAND_REGISTRY). Drives CLI, gateway, Telegram, Slack, autocomplete, and help. All commands derive from this single source. |
| `hermes_cli/config.py` | **Critical** | Configuration loading. DEFAULT_CONFIG, env var mapping, YAML merge, and config version migration. |
| `hermes_cli/setup.py` | **High** | Interactive setup wizard. Guides users through initial configuration, API key entry, and provider selection. |
| `hermes_cli/plugins.py` | **High** | Plugin manager. Discovers plugins from ~/.hermes/plugins/, repo plugins/, and pip entry points. Manages plugin lifecycle. |
| `hermes_cli/skin_engine.py` | **High** | Skin/theme engine. Data-driven CLI theming via YAML. Controls banner colors, spinner faces, tool prefixes, and response boxes. |
| `hermes_cli/curses_ui.py` | **High** | Curses-based interactive UI. Preferred over simple_term_menu for interactive menus. |
| `hermes_cli/auth.py` | **High** | Authentication management. Handles OAuth flows and API key storage. |
| `hermes_cli/profiles.py` | **High** | Multi-profile management. Create, list, switch, and delete profiles. Each profile has its own HERMES_HOME. |
| `hermes_cli/cron.py` | **High** | Cron CLI commands. List, add, edit, pause, resume, run, and remove scheduled jobs. |
| `hermes_cli/curator.py` | **High** | Curator CLI. Status, run, pause, pin, archive, restore, prune, backup, and rollback skill lifecycle operations. |
| `hermes_cli/kanban.py` | **High** | Kanban CLI. Init, create, list, show, assign, link, comment, complete, block, archive, tail, dispatch, daemon, and gc. |
| `hermes_cli/kanban_db.py` | **High** | Kanban database operations. SQLite backend for the kanban board. |
| `hermes_cli/gateway.py` | **High** | Gateway management CLI. Start, stop, status, and restart the messaging gateway. |
| `hermes_cli/web_server.py` | **High** | Web dashboard server with PTY bridge websocket. Serves the React dashboard and embeds hermes --tui. |
| `hermes_cli/pty_bridge.py` | **High** | PTY bridge for dashboard. Spawns hermes --tui as a PTY child and bridges bytes over WebSocket. |
| `hermes_cli/models.py` | **Medium** | Model selection and configuration. |
| `hermes_cli/model_catalog.py` | **Medium** | Model catalog management. |
| `hermes_cli/model_normalize.py` | **Medium** | Model name normalization. |
| `hermes_cli/model_switch.py` | **Medium** | Model switching logic. |
| `hermes_cli/providers.py` | **Medium** | Provider configuration. |
| `hermes_cli/runtime_provider.py` | **Medium** | Runtime provider resolution. |
| `hermes_cli/codex_models.py` | **Medium** | Codex-specific model handling. |
| `hermes_cli/codex_runtime_switch.py` | **Medium** | Codex runtime switching. |
| `hermes_cli/auth_commands.py` | **Medium** | Auth-related CLI commands. |
| `hermes_cli/copilot_auth.py` | **Medium** | GitHub Copilot authentication. |
| `hermes_cli/vercel_auth.py` | **Medium** | Vercel authentication. |
| `hermes_cli/dingtalk_auth.py` | **Medium** | DingTalk authentication. |
| `hermes_cli/profile_distribution.py` | **Medium** | Profile export/import. |
| `hermes_cli/backup.py` | **Medium** | Configuration backup. |
| `hermes_cli/uninstall.py` | **Medium** | Uninstallation support. |
| `hermes_cli/doctor.py` | **Medium** | Diagnostic command. |
| `hermes_cli/status.py` | **Medium** | Status display. |
| `hermes_cli/inventory.py` | **Medium** | Resource inventory. |
| `hermes_cli/logs.py` | **Medium** | Log browsing command. |
| `hermes_cli/hooks.py` | **Medium** | CLI hook system. |
| `hermes_cli/callbacks.py` | **Medium** | Agent callback wiring. |
| `hermes_cli/checkpoints.py` | **Medium** | Session checkpoint management. |
| `hermes_cli/claw.py` | **Medium** | Claw integration. |
| `hermes_cli/clipboard.py` | **Medium** | Clipboard operations. |
| `hermes_cli/browser_connect.py` | **Medium** | Browser connection helpers. |
| `hermes_cli/kanban_diagnostics.py` | **Medium** | Kanban diagnostics. |
| `hermes_cli/kanban_specify.py` | **Medium** | Kanban task specification. |
| `hermes_cli/goals.py` | **Medium** | Goal tracking commands. |
| `hermes_cli/memory_setup.py` | **Medium** | Memory provider setup wizard. |
| `hermes_cli/mcp_config.py` | **Medium** | MCP server configuration. |
| `hermes_cli/skills_config.py` | **Medium** | Skills configuration. |
| `hermes_cli/skills_hub.py` | **Medium** | Skills hub CLI. |
| `hermes_cli/platforms.py` | **Medium** | Platform configuration. |
| `hermes_cli/slack_cli.py` | **Medium** | Slack-specific CLI. |
| `hermes_cli/voice.py` | **Medium** | Voice mode CLI. |
| `hermes_cli/gateway_windows.py` | **Medium** | Windows-specific gateway support. |
| `hermes_cli/webhook.py` | **Medium** | Webhook CLI. |
| `hermes_cli/stdio.py` | **Medium** | Stdio transport. |
| `hermes_cli/oneshot.py` | **Medium** | One-shot mode. |
| `hermes_cli/relaunch.py` | **Medium** | Process relaunch. |
| `hermes_cli/timeouts.py` | **Medium** | Timeout configuration. |
| `hermes_cli/default_soul.py` | **Medium** | Default agent personality/soul. |
| `hermes_cli/azure_detect.py` | **Medium** | Azure detection. |
| `hermes_cli/nous_subscription.py` | **Medium** | Nous Research subscription handling. |
| `hermes_cli/security_advisories.py` | **Medium** | Security advisory display. |
| `hermes_cli/plugins_cmd.py` | **Medium** | Plugin management commands. |
| `hermes_cli/pairing.py` | **Medium** | Device pairing CLI. |
| `hermes_cli/env_loader.py` | **Medium** | .env file loader. |
| `hermes_cli/_parser.py` | **Medium** | Argument parsing helpers. |
| `hermes_cli/_subprocess_compat.py` | **Medium** | Subprocess compatibility layer. |
| `hermes_cli/cli_output.py` | **Medium** | CLI output formatting. |
| `hermes_cli/completion.py` | **Medium** | Slash command autocompletion. |
| `hermes_cli/tools_config.py` | **Medium** | Tool configuration via curses UI. |
| `hermes_cli/banner.py` | **Medium** | ASCII art banner with git state. |
| `hermes_cli/codex_runtime_plugin_migration.py` | **Low** | Codex migration utilities. |
| `hermes_cli/debug.py` | **Low** | Debug utilities. |
| `hermes_cli/dump.py` | **Low** | State dump for debugging. |
| `hermes_cli/tips.py` | **Low** | Tip display. |
| `hermes_cli/pt_input_extras.py` | **Low** | prompt_toolkit input extras (shift-enter aliases). |
| `hermes_cli/fallback_cmd.py` | **Low** | Fallback command handler. |
| `hermes_cli/colors.py` | **Low** | Color definitions. |
| `hermes_cli/__init__.py` | **Low** | Package init. |

---

## plugins/ — Plugin System

### Top-Level Plugins

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/teams_pipeline/` | **High** | Teams meeting pipeline plugin (9 files). Pipeline, meetings, subscriptions, store, models, runtime, and CLI. |
| `plugins/jade-identity/` | **Medium** | Jade identity plugin. Loads org config, registers core skills, provides /org and /whoami commands. |
| `plugins/oracule-adz-routing/` | **Medium** | Oracule ADZ routing plugin. Intelligent model selection with rate limit tracking, /routing-status, and /routing-override commands. |
| `plugins/google_meet/` | **Medium** | Google Meet integration plugin. |
| `plugins/spotify/` | **Medium** | Spotify integration plugin. |
| `plugins/hermes-achievements/` | **Low** | Gamified achievement tracking. |
| `plugins/disk-cleanup/` | **Low** | Disk cleanup plugin. Auto-tracks and cleans ephemeral files via plugin hooks. |
| `plugins/example-dashboard/` | **Low** | Example dashboard plugin. Reference implementation for custom dashboards. |
| `plugins/context_engine/__init__.py` | **Medium** | Context engine plugin. |
| `plugins/__init__.py` | **Low** | Package init. |

### plugins/memory/ — Memory Provider Plugins

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/memory/honcho/` | **High** | Honcho memory provider. Hierarchical memory with session-scoped and persistent layers. |
| `plugins/memory/mem0/` | **Medium** | Mem0 memory provider. |
| `plugins/memory/supermemory/` | **Medium** | Supermemory provider. |
| `plugins/memory/byterover/` | **Medium** | Byterover provider. |
| `plugins/memory/hindsight/` | **Medium** | Hindsight provider. |
| `plugins/memory/holographic/` | **Medium** | Holographic memory provider. |
| `plugins/memory/openviking/` | **Medium** | OpenViking provider. |
| `plugins/memory/retaindb/` | **Medium** | RetainDB provider. |
| `plugins/memory/__init__.py` | **Low** | Package init. |

### plugins/model-providers/ — Inference Backend Plugins

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/model-providers/anthropic/` | **Critical** | Anthropic Claude provider. Full support for Claude models with tool calling and thinking. |
| `plugins/model-providers/openai-codex/` | **High** | OpenAI Codex provider. |
| `plugins/model-providers/gemini/` | **High** | Google Gemini provider. |
| `plugins/model-providers/openrouter/` | **High** | OpenRouter provider. Aggregator for 100+ models. |
| `plugins/model-providers/deepseek/` | **High** | DeepSeek provider. |
| `plugins/model-providers/nous/` | **High** | Nous Research provider. |
| `plugins/model-providers/nvidia/` | **High** | NVIDIA provider. |
| `plugins/model-providers/bedrock/` | **High** | AWS Bedrock provider. |
| `plugins/model-providers/azure-foundry/` | **High** | Azure Foundry provider. |
| `plugins/model-providers/huggingface/` | **High** | HuggingFace provider. |
| `plugins/model-providers/xai/` | **Medium** | xAI (Grok) provider. |
| `plugins/model-providers/ollama-cloud/` | **Medium** | Ollama Cloud provider. |
| `plugins/model-providers/copilot/` | **Medium** | GitHub Copilot provider. |
| `plugins/model-providers/copilot-acp/` | **Medium** | Copilot ACP provider. |
| `plugins/model-providers/gmi/` | **Medium** | GMI provider. |
| `plugins/model-providers/minimax/` | **Medium** | MiniMax provider. |
| `plugins/model-providers/novita/` | **Medium** | Novita provider. |
| `plugins/model-providers/stepfun/` | **Medium** | StepFun provider. |
| `plugins/model-providers/alibaba/` | **Medium** | Alibaba provider. |
| `plugins/model-providers/alibaba-coding-plan/` | **Medium** | Alibaba coding plan provider. |
| `plugins/model-providers/kimi-coding/` | **Medium** | Kimi Coding provider. |
| `plugins/model-providers/qwen-oauth/` | **Medium** | Qwen OAuth provider. |
| `plugins/model-providers/xiaomi/` | **Medium** | Xiaomi provider. |
| `plugins/model-providers/zai/` | **Medium** | Zai provider. |
| `plugins/model-providers/ai-gateway/` | **Medium** | AI Gateway provider. |
| `plugins/model-providers/arcee/` | **Medium** | Arcee provider. |
| `plugins/model-providers/custom/` | **Medium** | Custom provider template for third parties. |
| `plugins/model-providers/kilocode/` | **Medium** | KiloCode provider. |
| `plugins/model-providers/opencode-zen/` | **Medium** | OpenCode Zen provider. |
| `plugins/model-providers/README.md` | **Medium** | Model provider plugin authoring guide. |

### plugins/kanban/ — Multi-Agent Work Queue

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/kanban/dashboard/` | **Medium** | Kanban web dashboard. React UI for viewing and managing kanban boards. |
| `plugins/kanban/systemd/` | **Low** | Systemd service file for the kanban dispatcher. |

### plugins/observability/ — Metrics & Traces

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/observability/langfuse/` | **High** | Langfuse observability integration. Traces, metrics, and logs for agent sessions. |

### plugins/image_gen/ — Image Generation Providers

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/image_gen/openai/` | **Medium** | OpenAI DALL-E provider. |
| `plugins/image_gen/openai-codex/` | **Medium** | OpenAI Codex image provider. |
| `plugins/image_gen/xai/` | **Medium** | xAI image provider. |

### plugins/video_gen/ — Video Generation Providers

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/video_gen/` | **Medium** | Video generation provider plugins. Similar structure to image_gen. |

### plugins/web/ — Web Search Providers

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/web/brave_free/` | **Medium** | Brave Free Search API. |
| `plugins/web/ddgs/` | **Medium** | DuckDuckGo (ddgs) search. |
| `plugins/web/exa/` | **Medium** | Exa AI search. |
| `plugins/web/firecrawl/` | **Medium** | Firecrawl web extraction. |
| `plugins/web/parallel/` | **Medium** | Parallel search provider. |
| `plugins/web/searxng/` | **Medium** | SearXNG self-hosted search. |
| `plugins/web/tavily/` | **Medium** | Tavily search API. |
| `plugins/web/__init__.py` | **Low** | Package init. |

### plugins/platforms/ — Additional Platform Plugins

| Path | Importance | Description |
|------|------------|-------------|
| `plugins/platforms/google_chat/` | **Medium** | Google Chat adapter. |
| `plugins/platforms/irc/` | **Medium** | IRC adapter plugin. |
| `plugins/platforms/line/` | **Medium** | LINE messenger adapter. |
| `plugins/platforms/teams/` | **Medium** | Microsoft Teams adapter. |

---

## cron/ — Scheduled Jobs

| Path | Importance | Description |
|------|------------|-------------|
| `cron/jobs.py` | **High** | Job store (SQLite-backed). Supports cron expressions, duration phrases, ISO timestamps, and context chaining. |
| `cron/scheduler.py` | **High** | Scheduler tick loop. Handles catchup windows, grace periods, file locking, and 3-minute hard interrupts. |
| `cron/__init__.py` | **Low** | Package init. |

---

## environments/ — RL Training Environments

| Path | Importance | Description |
|------|------------|-------------|
| `environments/hermes_swe_env/` | **High** | SWE (Software Engineering) benchmark environment. Runs the agent against SWE-bench tasks. |
| `environments/benchmarks/` | **High** | Benchmark configurations (tblite, terminalbench_2, yc_bench). |
| `environments/tool_call_parsers/` | **High** | Model-specific tool call parsers (deepseek, qwen, llama, mistral, kimi, glm, longcat). |
| `environments/hermes_base_env.py` | **Medium** | Base Hermes RL environment. |
| `environments/agent_loop.py` | **Medium** | Agent loop environment for RL training. |
| `environments/agentic_opd_env.py` | **Medium** | Agentic OPD environment. |
| `environments/web_research_env.py` | **Medium** | Web research RL environment. |
| `environments/terminal_test_env/` | **Medium** | Terminal test environment. |
| `environments/tool_context.py` | **Medium** | Tool context for RL. |
| `environments/patches.py` | **Medium** | Environment patches. |
| `environments/__init__.py` | **Low** | Package init. |

---

## skills/ — Built-in Skills (25 Categories)

| Path | Importance | Description |
|------|------------|-------------|
| `skills/github/` | **High** | GitHub workflow skills. Auth, code review, issues, PR workflow, repo management, codebase inspection. |
| `skills/mcp/` | **High** | MCP skills. Native MCP server configuration and usage. |
| `skills/software-development/` | **High** | Dev skills. Debugging, TDD, code review, planning, subagent-driven-development, Hermes skill authoring. |
| `skills/creative/` | **Medium** | Creative skills (20 entries). ASCII art, manim video, p5js, pixel art, excalidraw, comfyui, etc. |
| `skills/devops/` | **Medium** | DevOps skills. Kanban orchestrator, kanban worker, webhook subscriptions. |
| `skills/email/` | **Medium** | Email skills. Himalaya CLI integration. |
| `skills/media/` | **Medium** | Media skills. GIF search, Spotify, YouTube content, Heartmula, Songsee. |
| `skills/mlops/` | **Medium** | MLOps skills. Evaluation, HuggingFace hub, inference, models, research, training, vector databases. |
| `skills/note-taking/` | **Medium** | Note-taking. Obsidian integration. |
| `skills/productivity/` | **Medium** | Productivity skills. Airtable, Google Workspace, Linear, Maps, Notion, OCR, PowerPoint, Teams meeting. |
| `skills/research/` | **Medium** | Research skills. Arxiv, blogwatcher, LLM wiki, Polymarket, paper writing. |
| `skills/smart-home/` | **Medium** | Smart home. OpenHue integration. |
| `skills/apple/` | **Medium** | Apple ecosystem skills. Notes, reminders, FindMy, iMessage, macOS computer use. |
| `skills/autonomous-ai-agents/` | **Medium** | Agent usage skills. Claude Code, Codex, OpenCode, Hermes Agent. |
| `skills/data-science/` | **Medium** | Data science. Jupyter live kernel. |
| `skills/inference-sh/` | **Low** | Inference shell skills. |
| `skills/diagramming/` | **Low** | Diagramming skill descriptions. |
| `skills/dogfood/` | **Low** | Dogfooding skills. |
| `skills/domain/` | **Low** | Domain-specific skills. |
| `skills/gaming/` | **Low** | Gaming skills. Minecraft, Pokemon. |
| `skills/gifs/` | **Low** | GIF related skills. |
| `skills/red-teaming/` | **Low** | Red teaming. Godmode. |
| `skills/social-media/` | **Low** | Social media. Xurl. |
| `skills/yuanbao/` | **Low** | Yuanbao skills. |
| `skills/index-cache/` | **Low** | Skill index cache. |

---

## optional-skills/ — Optional Skills (18 Categories)

Heavier or niche skills NOT active by default. Installed explicitly via `hermes skills install`.

| Path | Importance | Description |
|------|------------|-------------|
| `optional-skills/autonomous-ai-agents/` | **Medium** | Autonomous agent skills. |
| `optional-skills/blockchain/` | **Medium** | Blockchain skills. |
| `optional-skills/communication/` | **Medium** | Communication skills. |
| `optional-skills/creative/` | **Medium** | Creative skills. |
| `optional-skills/devops/` | **Medium** | DevOps skills. |
| `optional-skills/email/` | **Medium** | Email skills. |
| `optional-skills/finance/` | **Medium** | Finance skills. |
| `optional-skills/health/` | **Medium** | Health skills. |
| `optional-skills/mcp/` | **Medium** | MCP skills. |
| `optional-skills/migration/` | **Medium** | Migration skills. |
| `optional-skills/mlops/` | **Medium** | MLOps skills. |
| `optional-skills/productivity/` | **Medium** | Productivity skills. |
| `optional-skills/research/` | **Medium** | Research skills. |
| `optional-skills/security/` | **Medium** | Security skills. |
| `optional-skills/software-development/` | **Medium** | Software development skills. |
| `optional-skills/web-development/` | **Medium** | Web development skills. |
| `optional-skills/dogfood/` | **Low** | Dogfooding skills. |

---

## tests/ — Test Suite (~17k tests, ~900 files)

| Path | Importance | Description |
|------|------------|-------------|
| `tests/conftest.py` | **Critical** | Pytest configuration with autouse fixtures. Isolates HERMES_HOME, unsets credentials, sets TZ=UTC, LANG=C.UTF-8. |
| `tests/agent/` | **Critical** | Agent unit tests (88 files). Adapters, compression, memory, credentials, curator, prompt builder, caching. |
| `tests/gateway/` | **Critical** | Gateway tests (247 files). All platform adapters, session management, delivery, hooks, shutdown forensics. |
| `tests/hermes_cli/` | **Critical** | CLI tests (207 files). Setup, profiles, config, models, skills, kanban, curator, gateway, plugins. |
| `tests/tools/` | **Critical** | Tool tests (214 files). All tools, environments, MCP, browser, terminal, file ops, delegation. |
| `tests/cron/` | **High** | Cron tests (14 files). Scheduler, jobs, script injection, workdir. |
| `tests/skills/` | **Medium** | Skill tests (10 files). |
| `tests/e2e/` | **Medium** | End-to-end tests (5 files). Matrix, Discord, platform commands. |
| `tests/stress/` | **Medium** | Stress/load tests. |
| `tests/integration/` | **Medium** | Integration tests. |
| `tests/plugins/` | **Medium** | Plugin tests. |
| `tests/providers/` | **Medium** | Provider tests. |
| `tests/run_agent/` | **Medium** | Agent runner tests. |
| `tests/hermes_state/` | **Medium** | State store tests. |
| `tests/honcho_plugin/` | **Medium** | Honcho plugin tests. |
| `tests/openviking_plugin/` | **Medium** | OpenViking plugin tests. |
| `tests/acp_adapter/` | **Medium** | ACP adapter tests. |
| `tests/acp/` | **Medium** | ACP tests. |
| `tests/cli/` | **Medium** | CLI tests. |
| `tests/environments/` | **Medium** | Environment tests. |
| `tests/tui_gateway/` | **Medium** | TUI gateway tests. |
| `tests/fakes/` | **Low** | Test fakes/mocks. |
| `tests/website/` | **Low** | Website tests. |
| Root-level test files (90+ files) | **Medium** | Integration tests for bootstrap, constants, logging, profiles, MCP, TTS, etc. |

---

## ui-tui/ — Terminal UI (Ink/React)

| Path | Importance | Description |
|------|------------|-------------|
| `ui-tui/src/entry.tsx` | **Critical** | Ink app entry point. Initializes the React terminal UI. |
| `ui-tui/src/app.tsx` | **Critical** | Main app component. Renders the transcript, composer, sidebar, and status panels. |
| `ui-tui/src/gatewayClient.ts` | **Critical** | JSON-RPC client. Communicates with the Python TUI gateway over stdio. |
| `ui-tui/src/components/` | **Critical** | UI components (22 files). Message rendering, tool activity, prompts, session picker, completions. |
| `ui-tui/src/theme.ts` | **Medium** | Theme definitions. Controls colors, fonts, and visual styling. |
| `ui-tui/src/branding.ts` | **Medium** | Branding configuration. Agent name, welcome message, prompt symbol. |
| `ui-tui/src/types.ts` / `gatewayTypes.ts` | **Medium** | TypeScript type definitions. |
| `ui-tui/src/hooks/` | **Medium** | React hooks (5 files). |
| `ui-tui/src/lib/` | **Medium** | Utility libraries. |
| `ui-tui/src/config/` | **Medium** | Configuration modules. |
| `ui-tui/src/content/` | **Medium** | Content handling. |
| `ui-tui/src/domain/` | **Medium** | Domain logic. |
| `ui-tui/src/protocol/` | **Medium** | Protocol definitions. |
| `ui-tui/src/app/` | **Medium** | App-level modules. |
| `ui-tui/src/__tests__/` | **Medium** | Unit tests. |
| `ui-tui/packages/hermes-ink/` | **Medium** | Hermes Ink package. |
| `ui-tui/package.json` | **Medium** | npm package config. |
| `ui-tui/vitest.config.ts` | **Low** | Vitest test config. |
| `ui-tui/tsconfig.json` | **Low** | TypeScript config. |

---

## tui_gateway/ — TUI Python Backend

| Path | Importance | Description |
|------|------------|-------------|
| `tui_gateway/server.py` | **Critical** | JSON-RPC server. Handles requests from Ink, manages sessions, tools, and model calls. |
| `tui_gateway/entry.py` | **High** | Entry point. Starts the TUI gateway process. |
| `tui_gateway/event_publisher.py` | **Medium** | Event publishing. Sends events (tool progress, message deltas) to Ink. |
| `tui_gateway/render.py` | **Medium** | Response rendering. Formats agent responses for the UI. |
| `tui_gateway/slash_worker.py` | **Medium** | Slash command worker. Runs slash commands in isolated subprocesses. |
| `tui_gateway/transport.py` | **Medium** | Transport layer. Handles stdio JSON-RPC communication. |
| `tui_gateway/ws.py` | **Medium** | WebSocket support. |
| `tui_gateway/__init__.py` | **Low** | Package init. |

---

## web/ — Dashboard Web App

| Path | Importance | Description |
|------|------------|-------------|
| `web/src/App.tsx` | **High** | Main app component. Layout with sidebar, chat pane, and status panels. |
| `web/src/components/` | **High** | React components (19 files). ChatSidebar, ModelPickerDialog, ToolCall, and supporting UI. |
| `web/src/pages/` | **High** | Page components (12 files). ChatPage, SettingsPage, and other dashboard views. |
| `web/src/main.tsx` | **Medium** | React entry point. |
| `web/src/hooks/` | **Medium** | React hooks (4 files). |
| `web/src/contexts/` | **Medium** | React contexts (6 files). |
| `web/src/lib/` | **Medium** | Utilities (8 files). |
| `web/src/plugins/` | **Medium** | Web plugin system (6 files). |
| `web/src/themes/` | **Medium** | Theme system (4 files). |
| `web/src/i18n/` | **Medium** | Internationalization. |
| `web/vite.config.ts` | **Medium** | Vite build config. |
| `web/index.html` | **Low** | HTML entry point. |

---

## website/ — Documentation Site

| Path | Importance | Description |
|------|------------|-------------|
| `website/docs/` | **High** | Documentation content. User guides, developer guides, feature docs, and API references. |
| `website/docusaurus.config.ts` | **Medium** | Docusaurus configuration. |
| `website/sidebars.ts` | **Medium** | Documentation sidebar structure. |
| `website/src/` | **Medium** | Custom site components. |
| `website/i18n/` | **Low** | Chinese translation. |
| `website/static/` | **Low** | Static assets. |
| `website/scripts/` | **Low** | Build scripts. |

---

## acp_adapter/ — ACP Server (IDE Integration)

| Path | Importance | Description |
|------|------------|-------------|
| `acp_adapter/server.py` | **High** | ACP protocol server. Implements the Agent Communication Protocol for IDE integration. |
| `acp_adapter/__main__.py` | **Medium** | Entry point for the ACP server. |
| `acp_adapter/session.py` | **Medium** | ACP session management. |
| `acp_adapter/tools.py` | **Medium** | ACP tool exposure. Exposes Hermes tools to the IDE. |
| `acp_adapter/auth.py` | **Medium** | ACP authentication. |
| `acp_adapter/permissions.py` | **Medium** | Permission management. |
| `acp_adapter/events.py` | **Medium** | Event handling. |
| `acp_adapter/entry.py` | **Medium** | Entry handling. |
| `acp_adapter/__init__.py` | **Low** | Package init. |

---

## scripts/ — Utility Scripts

| Path | Importance | Description |
|------|------------|-------------|
| `scripts/run_tests.sh` | **Critical** | Test runner with CI-parity. Unsets credentials, sets TZ=UTC, LANG=C.UTF-8, limits xdist to 4 workers. |
| `scripts/install.sh` | **High** | POSIX installation script. |
| `scripts/install.ps1` | **Medium** | Windows installation script (PowerShell). |
| `scripts/release.py` | **Medium** | Release automation. |
| `scripts/lint_diff.py` | **Medium** | Lint changed files. |
| `scripts/build_model_catalog.py` | **Medium** | Model catalog builder. |
| `scripts/build_skills_index.py` | **Medium** | Skills index builder. |
| `scripts/whatsapp-bridge/` | **Medium** | WhatsApp bridge (Node.js). |
| `scripts/install.cmd` | **Low** | Windows batch installer. |
| `scripts/lib/` | **Low** | Node bootstrap script. |

---

## remod/ — Re-modelling Session Artifacts

| Path | Importance | Description |
|------|------------|-------------|
| `remod/Session 1/` | **Medium** | Session 1 artifacts. Initial remodelling session notes and outputs. |
| `remod/Session 2/` | **Medium** | Session 2 artifacts. |
| `remod/Session 3/` | **Medium** | Session 3 artifacts. |
| `remod/Session 4/` | **Medium** | Session 4 artifacts. Core skill file creation (oracule-rules, agent-converse-protocol, slash-command-system, injection-guard, time-consciousness). |
| `remod/Session 5/` | **Medium** | Session 5 artifacts. Jade identity plugin design and implementation. |
| `remod/Session 6/` | **Medium** | Session 6 artifacts. Oracule ADZ Routing plugin design and implementation. |
| `remod/kanban_boards/` | **Medium** | Kanban board markdown files. Project tracking and task management. |
| `remod/jade_theme_preview.html` | **Medium** | Jade theme preview HTML. Visual mockup of the Jade UI theme. |

---

## Other Notable Directories

| Path | Importance | Description |
|------|------------|-------------|
| `providers/` | **Medium** | Legacy provider base class. Superseded by plugins/model-providers/. |
| `locales/` | **Medium** | 16 i18n YAML files for UI translation. |
| `.github/` | **Medium** | GitHub workflows, issue templates, and CI configuration. |
| `nix/` | **Low** | Nix package definitions (11 files). hermes-agent, TUI, web, devShell, overlays. |
| `packaging/homebrew/` | **Low** | Homebrew formula. |
| `docker/` | **Low** | Docker entrypoint script and SOUL.md. |
| `config-templates/agents/jade/` | **Low** | Jade agent config templates. |
| `config-templates/global/` | **Low** | Global config templates. |
| `config-templates/setup/` | **Low** | Setup guides. |
| `assets/` | **Low** | Static assets (banner.png). |

---

## File Dependency Chain

```
tools/registry.py  (no deps — imported by all tool files)
       ↑
tools/*.py  (each calls registry.register() at import time)
       ↑
model_tools.py  (imports tools/registry + triggers tool discovery)
       ↑
run_agent.py, cli.py, batch_runner.py, environments/
```

---

## Summary Statistics

- **Total directories**: ~200+
- **Total files**: ~2,000+
- **Lines of code**: ~200,000+ (Python + TypeScript)
- **Test coverage**: ~17,000 tests across ~900 files
- **Platform adapters**: 25+ (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, etc.)
- **Model providers**: 30+ (Anthropic, OpenAI, Gemini, DeepSeek, etc.)
- **Memory providers**: 8 (Honcho, Mem0, Supermemory, etc.)
- **Built-in skills**: 25 categories
- **Optional skills**: 18 categories
