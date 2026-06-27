# LLM Agent Design Patterns

Use these pattern cues to interpret project code. Do not substitute generic pattern explanations for project-specific analysis.

## Runtime Shapes

- Manual ReAct loop: project code explicitly cycles through model call, tool call, observation, and stop condition.
- Graph runtime: state moves through nodes and edges; reducers, checkpoints, and streaming often come from a graph framework.
- Workflow pipeline: deterministic stages transform the request before or after LLM calls.
- Planner/executor: one component creates or updates a plan; another executes steps.
- Router/expert: a router selects specialized chains, tools, agents, or workflows.
- Supervisor/worker: a parent agent delegates tasks and judges child results.
- Queue worker: requests become jobs; workers execute asynchronously with retry and persistence.
- Framework-managed loop: project supplies prompts, tools, config, and state while a library owns the model/tool loop.

## Harness Mechanisms

- Entry protocol: the boundary object converting UI/API/CLI events into a run request.
- State machine: explicit or implicit status transitions that make a task observable.
- Runtime context: hidden metadata such as user id, thread id, workspace, selected model, feature flags, permissions, and event sink.
- Artifact store: durable objects produced during a run, such as plans, diffs, files, reports, traces, browser snapshots, and search results.
- Event stream: append-only or streamed facts used by UI, replay, workers, or audit.
- Control plane: routing, scheduling, permissions, policy, audit, and orchestration.
- Execution plane: model calls, tool execution, terminal/browser actions, jobs, and side effects.

## Context Patterns

- Message history: previous conversation turns carried forward.
- Task workbench: current goal, constraints, plan, todos, evidence, failures, partial outputs, and next action.
- Tool observations: outputs from actions returned to the model or stored as artifacts.
- RAG context: retrieved documents or project knowledge inserted into prompts.
- Memory: long-term facts about user, project, preferences, or prior outcomes.
- Summaries/checkpoints: compressed state enabling long-running work, resume, rollback, or audit.
- Context firewall: policy deciding what sensitive data, hidden state, or tool output must not enter the model.

## Instruction And Memory File Patterns

- Persona/system identity file: describes the agent's identity, behavioral contract, values, or long-lived self-model. A file like `SOUL.md` may serve this role, but verify from code.
- User profile file: stores user preferences, facts, project context, or interaction history. A file like `USER.md` may serve this role, but verify from code.
- Project instruction file: constrains behavior inside a repository or workspace, such as `AGENTS.md`, `CLAUDE.md`, or project-specific guidance.
- Skill/plugin manifest: declares reusable capabilities, tool bindings, prompt snippets, or activation conditions.
- Memory ledger: append-only or summarized durable memory written by the agent over time.

When explaining these files, focus on ownership, write path, read path, prompt visibility, persistence, conflict resolution, and privacy/staleness risk.

## RAG Patterns

- Offline ingestion: loaders, parsers, chunkers, embeddings, and index construction.
- Runtime retrieval tool: model explicitly asks for search.
- Automatic context injection: harness retrieves before model call.
- Hybrid/rerank: dense, sparse, metadata, or reranker stages improve precision.
- Source grounding: citations or source ids tie answers back to documents.
- Index lifecycle: update, invalidation, reindex, and retrieval evals.

## Multi-Agent Patterns

- Supervisor-worker: parent assigns tasks and validates outputs.
- Router-expert: route based on task class or domain.
- Planner-executor: planner decomposes, executor acts.
- Debate/review: independent agents produce critiques or votes.
- Blackboard: agents coordinate through shared artifacts/state.
- Pipeline: agents operate in fixed stages.

Useful multi-agent systems usually have clear boundaries, isolated context, constrained permissions, explicit merge logic, and termination rules. Weak multi-agent systems often duplicate context, amplify cost, and make failures harder to debug.

## How To Explain A Mechanism

For each important mechanism, answer:

- What design problem does it solve?
- What component owns it?
- What evidence file/function/class proves it?
- What state, context, artifact, or event does it read/write?
- How does it interact with neighboring mechanisms?
- What tradeoff or failure mode does it introduce?
