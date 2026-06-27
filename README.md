# Agent Codebase Analysis Skill

`analyze-agent-codebase` is a Codex/Claude skill for studying mature LLM-agent projects as systems.

It is designed for agent developers who want to quickly understand how an open-source agent project is designed: how the harness works, how context is maintained, how tools are controlled, how RAG is implemented, how single-agent or multi-agent execution advances, and how the system can be explained clearly to others.

The skill does not produce a file-by-file inventory. It produces a polished architecture report focused on runtime behavior and design mechanisms.

## What It Produces

The final user-facing output is:

```text
agent-codebase-analysis/agent-architecture-analysis.html
```

The HTML report includes:

- Executive summary of the project design.
- System boundary and request lifecycle.
- Harness/runtime loop and state-machine analysis.
- Context, memory, prompt, artifact, and event flow.
- Tool, permission, action, and RAG pipeline analysis.
- Single-agent long-task behavior.
- Multi-agent coordination analysis when relevant.
- Zoomable Mermaid architecture diagrams.
- Project-specific terminology glossary.
- Interview-ready explanation callouts.
- Short reading path with high-leverage files.
- Unknowns and verification checks.

## Why This Skill Exists

When reading an agent project, beginners often get buried in scripts, classes, and directory trees. That makes it hard to answer the architectural questions that actually matter:

- What turns a user request into a controlled agent run?
- What does the model decide, and what does the runtime decide?
- What enters the prompt, and what stays hidden as runtime state?
- How are tools authorized, executed, retried, and observed?
- How does memory differ from RAG, task state, and artifacts?
- What stops the agent from looping forever or taking unsafe actions?
- If the system has multiple agents, how are responsibilities split and merged?

This skill pushes the analysis toward those questions.

## Install For Codex

Clone this repository into your Codex skills directory:

```powershell
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.agents\skills\analyze-agent-codebase
```

Restart Codex so the new skill is discovered.

## Install For Claude

Clone this repository into your Claude skills directory:

```powershell
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.claude\skills\analyze-agent-codebase
```

Restart Claude Code so the new skill is discovered.

## Usage

Ask your agent to use the skill against a target repository:

```text
Use $analyze-agent-codebase to analyze C:\path\to\agent-project.
```

Or:

```text
Analyze this LLM-agent project and create a polished HTML architecture report with zoomable Mermaid diagrams.
```

The skill first runs a read-only evidence finder to locate high-signal files, then selectively reads runtime, context, tool, memory, RAG, event, persistence, safety, and evaluation code.

## Report Focus

The analysis is organized around:

- **Harness**: how the runtime constrains model behavior.
- **Single-agent design**: how one agent handles long tasks, state, recovery, and completion.
- **Multi-agent design**: whether coordination is justified, how agents communicate, and how outputs merge.
- **RAG and knowledge systems**: ingestion, chunking, indexing, retrieval trigger, reranking, citations, updates, and evaluation.
- **Context and memory**: model-visible prompt context versus hidden runtime state.
- **Tools and permissions**: registration, validation, authorization, execution, retries, and observations.
- **Observability and replay**: traces, logs, costs, errors, evals, checkpoints, and auditability.

## Repository Layout

```text
SKILL.md
agents/openai.yaml
evals/evals.json
references/
  agent-design-taxonomy.md
  interview-explanation-guide.md
  llm-agent-patterns.md
  report-template.md
scripts/
  repo_inventory.py
```

## Development

Validate the skill metadata:

```powershell
python path\to\skill-creator\scripts\quick_validate.py .
```

Check the inventory script:

```powershell
python -m py_compile scripts\repo_inventory.py
```

## License

MIT
