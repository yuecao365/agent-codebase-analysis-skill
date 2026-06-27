# Agent Codebase Analysis Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-111827.svg)](SKILL.md)
[![Codex](https://img.shields.io/badge/Codex-compatible-10a37f.svg)](https://developers.openai.com/codex/skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-6b5cff.svg)](https://code.claude.com/docs/en/skills)

`analyze-agent-codebase` is an Agent Skill for understanding mature LLM-agent projects as runtime systems.

It helps new agent developers read an unfamiliar agent codebase and answer the questions that matter: how the harness constrains model behavior, how context is assembled, how tools are authorized, how RAG works, how memory differs from task state, how single-agent or multi-agent execution advances, and how to explain the architecture clearly.

It does not create a file-by-file inventory. It creates a polished architecture report focused on system design.

## Quick Install

Recommended for most users:

```bash
npx skills add yuecao365/agent-codebase-analysis-skill -g --agent codex claude-code
```

Then restart your agent host and ask:

```text
Use $analyze-agent-codebase to analyze /path/to/agent-project.
```

## Contents

- [What This Skill Produces](#what-this-skill-produces)
- [Who It Is For](#who-it-is-for)
- [Install Options](#install-options)
- [Usage](#usage)
- [What The Report Explains](#what-the-report-explains)
- [Example Prompts](#example-prompts)
- [Repository Layout](#repository-layout)
- [Update Or Remove](#update-or-remove)
- [Development](#development)
- [License](#license)

## What This Skill Produces

The final user-facing output is a single self-contained HTML file:

```text
agent-codebase-analysis/agent-architecture-analysis.html
```

The report includes:

- Executive summary of the project thesis, agent type, dominant complexity, and design lessons.
- System boundary, request lifecycle, harness loop, and state-machine analysis.
- Context, memory, prompt, artifact, event, and persistence flow.
- Tool registration, permission checks, action execution, retries, observations, and failure handling.
- RAG and knowledge pipeline analysis when retrieval exists.
- Single-agent long-task behavior.
- Multi-agent topology and coordination-cost analysis when multiple agents exist.
- Zoomable Mermaid architecture diagrams embedded in the same HTML report.
- A glossary for project-specific, English-only, and interview-relevant agent architecture terms.
- Interview-ready callouts that help a reader explain the system clearly.
- A short reading path with high-leverage files instead of a directory dump.
- Unknowns and verification checks for claims static reading cannot prove.

## Who It Is For

Use this skill when you want to understand or explain:

- An open-source agent project.
- A coding agent or browser agent runtime.
- A single-agent harness with tools, memory, permissions, or long tasks.
- A multi-agent system with workers, roles, routing, or coordination.
- A RAG-powered agent with ingestion, indexing, retrieval, reranking, or citations.
- A platform runtime with gateways, event streams, sandboxes, persistence, or replay.

The skill is especially useful when the goal is learning, onboarding, architecture review, or interview-style explanation.

## Install Options

This repository is a standard Agent Skill repository. You can install it several ways.

### Option 1: Universal `npx skills` CLI

Use this when you want one command that can target multiple agent hosts.

```bash
npx skills add yuecao365/agent-codebase-analysis-skill -g --agent codex claude-code
```

Install only for Codex:

```bash
npx skills add yuecao365/agent-codebase-analysis-skill -g --agent codex
```

Install only for Claude Code:

```bash
npx skills add yuecao365/agent-codebase-analysis-skill -g --agent claude-code
```

List detected skills before installing:

```bash
npx skills add yuecao365/agent-codebase-analysis-skill --list
```

If Claude Code does not detect a skill installed through `npx skills`, install with `gh skill` or use the manual Claude Code path below. Some installer versions use `~/.agents/skills/` as the canonical location, while Claude Code reads `~/.claude/skills/`.

### Option 2: Codex Skill Installer

In Codex, ask the built-in installer to download this GitHub repository:

```text
Use $skill-installer to install https://github.com/yuecao365/agent-codebase-analysis-skill.git globally.
```

Restart Codex if the skill does not appear immediately.

### Option 3: GitHub CLI Agent Skills

If your GitHub CLI is v2.90.0 or later, install from the repository:

```bash
gh skill install yuecao365/agent-codebase-analysis-skill
```

Install directly for Codex:

```bash
gh skill install yuecao365/agent-codebase-analysis-skill analyze-agent-codebase --agent codex --scope user
```

Install directly for Claude Code:

```bash
gh skill install yuecao365/agent-codebase-analysis-skill analyze-agent-codebase --agent claude-code --scope user
```

Preview before installing:

```bash
gh skill preview yuecao365/agent-codebase-analysis-skill analyze-agent-codebase
```

### Option 4: Manual Git Clone

Codex:

```powershell
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.agents\skills\analyze-agent-codebase
```

Claude Code:

```powershell
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.claude\skills\analyze-agent-codebase
```

macOS/Linux examples:

```bash
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git ~/.agents/skills/analyze-agent-codebase
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git ~/.claude/skills/analyze-agent-codebase
```

### Option 5: Download ZIP

Use this when Git is not installed.

1. Open <https://github.com/yuecao365/agent-codebase-analysis-skill>.
2. Click **Code**.
3. Click **Download ZIP**.
4. Unzip the folder.
5. Rename the unzipped folder to `analyze-agent-codebase`.
6. Move it to one of these locations:

```text
Codex:      ~/.agents/skills/analyze-agent-codebase
Claude:     ~/.claude/skills/analyze-agent-codebase
```

On Windows, `~` means your user profile directory, for example:

```text
C:\Users\<you>\.agents\skills\analyze-agent-codebase
C:\Users\<you>\.claude\skills\analyze-agent-codebase
```

Restart the agent after installation.

## Usage

Run the skill against a target repository:

```text
Use $analyze-agent-codebase to analyze C:\path\to\agent-project.
```

or:

```text
Use $analyze-agent-codebase to create a polished single-file HTML architecture analysis for this LLM-agent project.
```

The skill runs a read-only evidence finder first, then selectively reads high-signal files such as entrypoints, harness/runtime loops, prompt builders, model adapters, tool registries, permission layers, memory/RAG modules, event streams, persistence, replay, tests, and evaluation code.

## What The Report Explains

The analysis is organized around design mechanisms, not filenames:

| Area | What the report answers |
| --- | --- |
| System boundary | What enters the system, what leaves it, and who decides success. |
| Harness | How the runtime turns an open-ended user request into controlled, recoverable behavior. |
| State machine | What states a task can enter, how it stops, retries, fails, resumes, or completes. |
| Context | What the model sees versus what remains hidden runtime state. |
| Memory | Which facts are temporary, persistent, user-specific, project-specific, or retrieved. |
| Tools | How model tool requests become validated, authorized, executed actions. |
| RAG | How sources are ingested, chunked, indexed, retrieved, ranked, inserted, cited, and refreshed. |
| Artifacts and events | How outputs, traces, tool results, progress, and replayable history are stored. |
| Single agent | How one agent plans, advances, recovers, verifies, and finishes long tasks. |
| Multi-agent | How agents divide work, share context, communicate, merge results, and control coordination cost. |
| Safety and observability | How permissions, logs, traces, costs, latency, evals, and human intervention are handled. |

## Example Prompts

```text
Use $analyze-agent-codebase to analyze this repo as an agent harness, not as a file tree.
```

```text
Use $analyze-agent-codebase to explain how this project manages context, tools, RAG, memory, and artifacts.
```

```text
Use $analyze-agent-codebase to produce an HTML report with zoomable Mermaid diagrams and a glossary.
```

```text
Use $analyze-agent-codebase to analyze whether this multi-agent architecture is justified or mostly coordination overhead.
```

## Repository Layout

```text
SKILL.md
agents/
  openai.yaml
evals/
  evals.json
references/
  agent-design-taxonomy.md
  interview-explanation-guide.md
  llm-agent-patterns.md
  report-template.md
scripts/
  repo_inventory.py
```

Key files:

- `SKILL.md`: main workflow and required output contract.
- `references/agent-design-taxonomy.md`: architecture checklist for harness, context, tools, RAG, memory, single-agent, and multi-agent analysis.
- `references/report-template.md`: final HTML structure, diagram requirements, zoom behavior, and glossary rules.
- `references/interview-explanation-guide.md`: plain-language and interview-ready explanation guidance.
- `scripts/repo_inventory.py`: read-only evidence finder used as private scratch, not as a user-facing report.

## Update Or Remove

If installed with `git clone`:

```bash
cd ~/.agents/skills/analyze-agent-codebase
git pull
```

or:

```bash
cd ~/.claude/skills/analyze-agent-codebase
git pull
```

If installed with `npx skills`, rerun the install command to refresh the local copy.

You can also check and update skills managed by `npx skills`:

```bash
npx skills list
npx skills check
npx skills update
```

If installed with `gh skill`:

```bash
gh skill update
```

To remove the skill, delete the installed `analyze-agent-codebase` folder from your agent skills directory and restart the agent.

## Development

Validate the skill metadata:

```powershell
python path\to\skill-creator\scripts\quick_validate.py .
```

Check the inventory script:

```powershell
python -m py_compile scripts\repo_inventory.py
```

Check repository state before publishing:

```bash
git status -sb
git diff --check
```

## License

MIT
