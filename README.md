# Agent Codebase Analysis Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-111827.svg)](SKILL.md)
[![Codex](https://img.shields.io/badge/Codex-compatible-10a37f.svg)](https://developers.openai.com/codex/skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-6b5cff.svg)](https://code.claude.com/docs/en/skills)
[![中文 README](https://img.shields.io/badge/README-中文-red.svg)](README.zh-CN.md)

`analyze-agent-codebase` is an Agent Skill for understanding mature LLM-agent projects as runtime systems.

It helps agent developers explain how an unfamiliar project actually works: the harness, context flow, tools, permissions, RAG, memory, artifacts, single-agent loops, multi-agent coordination, observability, and safety boundaries.

It does **not** generate a file-by-file inventory. It produces a polished architecture report focused on design mechanisms.

## Example Report

- [View OpenClaw example report](https://htmlpreview.github.io/?https://github.com/yuecao365/agent-codebase-analysis-skill/blob/main/examples/openclaw/agent-architecture-analysis-en.html)
- [Open the HTML file in this repo](examples/openclaw/agent-architecture-analysis-en.html)

## Output

The skill writes one user-facing file:

```text
agent-codebase-analysis/agent-architecture-analysis.html
```

The report includes:

- Executive summary and design lessons.
- Harness/runtime loop and state-machine analysis.
- Context, memory, prompt, artifact, event, and persistence flow.
- Tool authorization, execution, retry, observation, and failure handling.
- RAG pipeline analysis when retrieval exists.
- Single-agent and multi-agent architecture analysis.
- Zoomable Mermaid diagrams.
- Project-specific and interview-relevant glossary.
- Reading path and verification gaps.

## Quick Install

Install for Codex and Claude Code:

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

Restart your agent host after installation.

## Other Install Options

Codex built-in installer:

```text
Use $skill-installer to install https://github.com/yuecao365/agent-codebase-analysis-skill.git globally.
```

GitHub CLI:

```bash
gh skill install yuecao365/agent-codebase-analysis-skill
```

Manual clone:

```bash
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git ~/.agents/skills/analyze-agent-codebase
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git ~/.claude/skills/analyze-agent-codebase
```

Windows manual clone:

```powershell
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.agents\skills\analyze-agent-codebase
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.claude\skills\analyze-agent-codebase
```

No Git installed: download the repository ZIP from GitHub, rename the folder to `analyze-agent-codebase`, and move it into your Codex or Claude skills directory.

## Usage

```text
Use $analyze-agent-codebase to analyze /path/to/agent-project.
```

More specific prompts:

```text
Use $analyze-agent-codebase to explain this repo as an agent harness, not as a file tree.
```

```text
Use $analyze-agent-codebase to create an HTML architecture report with zoomable Mermaid diagrams and a glossary.
```

```text
Use $analyze-agent-codebase to analyze whether this multi-agent design is justified or mostly coordination overhead.
```

## What It Focuses On

| Area | Question |
| --- | --- |
| Harness | What does the runtime decide instead of the model? |
| Context | What enters the prompt, and what stays hidden? |
| Tools | How are tool calls validated, authorized, executed, and observed? |
| RAG | How are documents ingested, chunked, indexed, retrieved, ranked, and cited? |
| Memory | What is temporary, persistent, user-specific, project-specific, or retrieved? |
| Agents | How does one agent advance long tasks, or how do multiple agents coordinate? |
| Safety | Where are permissions, approvals, sandboxes, retries, and failure paths enforced? |
| Observability | Can runs be traced, replayed, evaluated, or debugged? |

## Repository Layout

```text
SKILL.md
agents/openai.yaml
evals/evals.json
references/
scripts/repo_inventory.py
examples/openclaw/
```

## Development

```bash
python path/to/skill-creator/scripts/quick_validate.py .
python -m py_compile scripts/repo_inventory.py
git diff --check
```

## License

MIT
