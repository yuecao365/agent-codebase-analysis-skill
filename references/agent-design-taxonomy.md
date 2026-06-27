# Agent System Design Taxonomy

Use this checklist to analyze an LLM-agent repository as a system. Answer only what is present or architecturally important. Do not force every heading if the project clearly lacks that mechanism.

## 0. System Task Boundary

Identify the product contract before reading implementation details.

Questions:

- What user job does the system perform?
- What are the main inputs and outputs?
- Is the output an answer, action, workflow result, code diff, file, report, browser state, database change, or long-running session?
- Who decides success: user, test, eval, workflow condition, reviewer, or external system?
- What type of agent system is it: chat assistant, coding agent, research agent, browser agent, workflow agent, agent framework, or platform runtime?
- What is the dominant complexity: context, tools, safety, collaboration, long-running execution, deployment, or evaluation?

## 1. Harness / Runtime

The harness is the runtime that constrains model behavior.

Questions:

- What is the entry protocol: CLI, API, UI, IDE, queue, gateway, SDK, chat platform, or webhook?
- Where does the main run begin?
- Is control flow a ReAct loop, graph, workflow, planner/executor, router, queue worker, framework-managed loop, or deterministic pipeline?
- What state machine exists for a run? Look for running, planning, tool_calling, waiting_approval, failed, cancelled, completed, or equivalent states.
- How are runtime dependencies created and passed: config, model client, tool registry, memory, stores, workspace, event sink, permissions?
- What are the stop conditions?
- How are cancellation, interruption, timeout, retry, resume, and recovery handled?

## 2. Context And State

Separate model-visible context from hidden runtime state.

Questions:

- What is the session/thread/task state?
- What enters the prompt and what stays hidden?
- How are message history, tool observations, memory, RAG snippets, artifacts, plans, and user metadata selected?
- How does the project compress, summarize, trim, rank, or retrieve context?
- What persists across turns or process restarts?
- Are reducers, checkpoints, database rows, files, event logs, or in-memory stores responsible for state transitions?
- Can the system search, replay, audit, or resume a session?

## 2A. Project-Native Concepts And Instruction Files

Use this section when the project defines named concepts or persistent instruction/memory files.

Questions:

- Does the project define concepts such as session, thread, workspace, node, channel, skill, memory, artifact, task, persona, profile, or soul?
- Which concepts are user-facing and which are internal runtime abstractions?
- Are there instruction or memory files such as `SOUL.md`, `USER.md`, `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `MEMORY.md`, `PROFILE.md`, or project-specific equivalents?
- For each such file, what information does it store?
- Who writes it: user, agent, tool, setup command, sync job, or runtime?
- Who reads it: harness, prompt builder, memory system, tool layer, UI, or evaluator?
- Does it enter the prompt directly, get summarized, get retrieved, or stay hidden as runtime state?
- How is conflict handled when two files or memory sources disagree?
- What privacy, staleness, prompt-injection, or personalization risk does it create?

Special case:

- If both `SOUL.md` and `USER.md` exist, compare them explicitly. Usually the important design question is whether one represents agent identity/persona/system-level self-model while the other represents user profile/preferences/session-specific memory. Verify this from code before claiming it.

## 3. Prompt And Model Layer

Questions:

- Where are system/developer/user prompts assembled?
- Which runtime variables enter prompts?
- How does the project select model provider and model configuration?
- How does it normalize tool calling, streaming, structured output, vision, reasoning, fallback, or provider-specific capabilities?
- How are malformed model outputs handled?

## 4. Tool And Action Layer

Questions:

- How are tools declared, registered, discovered, and exposed to the model?
- Are tools selected freely by the model, routed deterministically, filtered by context, or gated by policy?
- What permission model controls risky actions?
- How are timeouts, retries, errors, stdout/stderr, file changes, browser changes, and observations represented?
- Which side effects can tools perform: filesystem, terminal, browser, network, database, third-party APIs?
- How do tool results re-enter context or artifacts?

## 5. Artifact And Event Model

Use this when the project has plans, files, diffs, reports, traces, UI events, checkpoints, or generated assets.

Questions:

- What artifacts are first-class objects?
- Who owns and mutates artifacts: model, harness, tools, UI, worker, or user?
- How are artifacts stored, versioned, diffed, streamed, or attached to sessions?
- What events exist: user_message, model_delta, tool_call, tool_result, approval_request, progress, error, checkpoint, completion?
- Does the event stream power UI rendering, replay, audit, or worker coordination?

## 6. Control Plane And Execution Plane

Use this when the system has gateways, sandboxes, workers, queues, distributed services, browser automation, or permission layers.

Questions:

- Which components schedule, authorize, audit, and route work?
- Which components actually execute model calls, tools, terminal commands, browser actions, or workflows?
- Where are policies enforced?
- How are secrets, workspaces, filesystem access, network access, database access, and browser state isolated?
- Can execution be paused, cancelled, retried, or moved to another worker?

## 7. RAG / Knowledge Layer

Use when the project has retrieval, document search, embeddings, indexes, semantic search, project knowledge, or vector stores.

Questions:

- What data sources feed knowledge?
- How is content loaded, parsed, chunked, embedded, and indexed?
- Where does the index/store live?
- What triggers retrieval: automatic context injection, explicit tool call, router decision, or user action?
- How are results ranked, filtered, reranked, summarized, or inserted into the prompt?
- Are citations or sources surfaced?
- How are indexes updated, invalidated, or rebuilt?
- How is retrieval quality evaluated?

## 8. Memory Layer

Questions:

- Does the system distinguish message history, task state, project knowledge, and long-term user memory?
- How is memory written?
- How is memory retrieved and ranked?
- Who can edit or delete memory?
- How does memory differ from RAG?
- What privacy, staleness, or contamination risks exist?

## 9. Single-Agent Long-Task Design

Use when one agent loop owns most work.

Questions:

- How is the user request converted into goal, constraints, and plan?
- Can the plan be updated, interrupted, resumed, or verified?
- How is the working set maintained: todo list, task state, artifacts, current files, evidence, failures?
- How are tool failures, invalid outputs, context overflow, missing permissions, and partial completion recovered?
- How does the agent decide it is done?
- What self-check, test, review, or final acceptance gate exists?

## 10. Multi-Agent Coordination

Use when multiple agents, roles, workers, experts, or delegated loops exist.

Questions:

- What topology is used: supervisor-worker, router-expert, planner-executor, debate, blackboard, pipeline, graph, or swarm?
- What is each agent's input, output, permission set, tools, and completion condition?
- What state is shared and what is isolated?
- Do agents communicate through natural language, structured tasks, artifacts, events, queues, or shared stores?
- How much context does the parent pass to children?
- Do children return summaries, artifacts, patches, votes, or full traces?
- Who has final execution authority?
- How are outputs merged, adjudicated, verified, deduplicated, or tested?
- What prevents delegation loops, waiting cycles, endless debate, and runaway cost?
- Does multi-agent design reduce complexity, or mainly add token/latency/debugging cost?

## 11. Observability, Evaluation, And Safety

Questions:

- What is logged or traced: prompts, model outputs, tool calls, errors, cost, latency, state transitions, artifacts?
- Can a run be replayed or audited?
- What evals, golden tests, benchmarks, or regression suites exist?
- Are failure types classified?
- Where can a human take over?
- What security boundaries protect files, terminal, network, database, browser, third-party APIs, and secrets?

## Required Mermaid Visuals

Create Mermaid diagrams that explain the design. These are required in the final HTML, not optional supporting material.

1. System boundary diagram.
2. Request lifecycle sequence.
3. Context/state flow, separating model-visible context and hidden runtime state.
4. Tool/RAG/action flow when relevant.
5. Multi-agent topology when present.
6. Control-plane/execution-plane split when relevant.

For each diagram:

- Use Mermaid syntax or compiled SVG generated from Mermaid.
- Include a plain-language explanation of the design idea.
- Cite representative evidence files/functions/classes after the explanation.
- Label inferred states or flows as inferred when the code does not name them explicitly.

Diagrams must be project-specific and conceptual. Do not generate directory trees as visual aids.
