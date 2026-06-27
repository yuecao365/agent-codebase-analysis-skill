# Agent Architecture HTML Report Template

Use this structure for `agent-codebase-analysis/agent-architecture-analysis.html`. The final report must combine design explanation, key mechanisms, and architecture visuals in one self-contained HTML file.

## Output Contract

Produce one user-facing file:

`agent-codebase-analysis/agent-architecture-analysis.html`

Do not produce user-facing `design-report.md`, `key-mechanisms.md`, `architecture-visuals.md`, `inventory.json`, or `evidence-map.html`. `inventory.json` may exist only under `.analysis-work/` as internal scratch data.

## HTML Composition

Build a static HTML page with:

- `<title>` containing the project name and "Agent Architecture Analysis".
- A top summary band with project thesis, agent type, main complexity, and strongest design lesson.
- A sticky or clearly visible table of contents.
- The table of contents must include a visible link to the terminology glossary whenever the glossary section exists. Prefer `<a href="#terminology-glossary">Terminology Glossary</a>` and use `id="terminology-glossary"` on the section.
- Sections that combine prose, mechanism explanation, diagrams, and evidence citations.
- Inline CSS. Do not require external CSS assets.
- Responsive layout for desktop and mobile.
- Mermaid diagrams are mandatory. Compile to inline SVG when possible; always retain Mermaid source or a renderable Mermaid block in the HTML.
- If Mermaid cannot be compiled locally, include Mermaid.js initialization and renderable `<div class="mermaid">...</div>` blocks. Do not omit diagrams.
- Every diagram must be zoomable. Use an inline modal/lightbox, `<dialog>`, or full-width expandable panel so users can enlarge complex SVG/Mermaid diagrams without losing readability.

## Diagram Readability And Zoom

Mermaid diagrams often become unreadable when too much architecture is forced into one canvas. Apply these rules:

- Split any diagram with more than about 12 nodes, 16 edges, or 4 visual clusters into smaller diagrams.
- Prefer 2-4 focused diagrams over one giant diagram.
- Use short labels in diagrams; put detailed explanation in prose beside the diagram.
- Keep Mermaid direction readable: `LR` for system boundaries and pipelines, `TD` for state/context hierarchy, `sequenceDiagram` for lifecycle.
- Use `themeVariables` or CSS so diagram text is at least 14px when rendered.
- Wrap every diagram in a zoomable container with a visible "Open larger" or "Zoom" control.
- In the zoom view, allow horizontal scrolling and preserve SVG/vector clarity.

Minimum inline behavior:

```html
<button class="diagram-zoom" data-diagram="request-lifecycle-diagram">Open larger</button>
<div id="request-lifecycle-diagram" class="diagram-card">
  <div class="mermaid">
sequenceDiagram
  participant User
  participant Harness
  participant Model
  User->>Harness: request
  Harness->>Model: prompt plus context
  Model-->>Harness: next action or answer
  </div>
</div>

<dialog id="diagram-modal">
  <button id="close-diagram">Close</button>
  <div id="diagram-modal-body"></div>
</dialog>
```

The corresponding script may clone the selected diagram into the modal. Keep all CSS/JS inline in the HTML file.

Recommended CSS/JS behavior:

```html
<style>
  .diagram-card { overflow-x: auto; border: 1px solid #d8dee9; border-radius: 8px; padding: 16px; background: #fff; }
  .diagram-card svg { max-width: none; min-width: 720px; height: auto; }
  .diagram-zoom { margin: 8px 0 12px; }
  #diagram-modal { width: min(96vw, 1400px); height: min(92vh, 900px); border: 0; border-radius: 10px; padding: 16px; }
  #diagram-modal::backdrop { background: rgba(15, 23, 42, .55); }
  #diagram-modal-body { overflow: auto; height: calc(100% - 48px); }
  #diagram-modal-body svg { max-width: none; min-width: 1100px; height: auto; }
  @media (max-width: 720px) {
    .diagram-card svg { min-width: 640px; }
  }
</style>
<script>
  document.querySelectorAll('.diagram-zoom').forEach((button) => {
    button.addEventListener('click', () => {
      const source = document.getElementById(button.dataset.diagram);
      const body = document.getElementById('diagram-modal-body');
      body.innerHTML = source ? source.innerHTML : '';
      document.getElementById('diagram-modal').showModal();
    });
  });
  document.getElementById('close-diagram')?.addEventListener('click', () => {
    document.getElementById('diagram-modal').close();
  });
</script>
```

If the report uses Mermaid.js runtime rendering, run Mermaid initialization before users click zoom buttons, or re-run Mermaid rendering inside the modal after cloning.

## Mermaid Block Pattern

Each major diagram section should use this structure:

```html
<section id="request-lifecycle">
  <h2>Request Lifecycle</h2>
  <p class="plain">Plain-language explanation of what the diagram teaches.</p>
  <div class="diagram-card">
    <h3>How one user request moves through the runtime</h3>
    <div class="mermaid">
sequenceDiagram
  participant User
  participant Harness
  participant Model
  participant Tools
  participant Store
  User->>Harness: request
  Harness->>Model: prompt + context
  Model-->>Harness: next action
  Harness->>Tools: authorized tool call
  Tools-->>Harness: observation
  Harness->>Store: event/artifact update
  Harness-->>User: final result
    </div>
    <p class="evidence">Evidence: <code>path/to/runtime</code>, <code>path/to/tools</code></p>
  </div>
</section>
```

If compiled SVG is available, place the SVG inside `.diagram-card` and keep Mermaid source in a collapsible `<details>` block.

## Required Diagram Set

The HTML must include these diagrams unless truly not applicable:

1. **System boundary**: user entry surfaces, harness, model provider, tools, memory/RAG, artifact store, event stream, persistence, and external systems.
2. **Request lifecycle**: user request, harness initialization, context assembly, model call, tool/RAG/memory interaction, event/artifact update, and response.
3. **Harness state machine**: run/task statuses and transitions, including error, approval, cancellation, retry, and completion when present.
4. **Context and memory flow**: model-visible context versus hidden runtime state, plus memory, RAG, artifacts, and tool observations.
5. **Tool/action/RAG flow**: registration, permission check, execution, observation, failure/retry, context reinsertion.
6. **Multi-agent topology** when present, otherwise **control-plane/execution-plane split** when present. If neither exists, include a short "not applicable" explanation.

Every diagram must have a plain-language explanation before or beside it. A diagram without explanation is incomplete.

## Recommended Layout

### 1. Executive Summary

Cover:

- What the project does for the user.
- What type of agent system it is.
- The main harness idea.
- The biggest architectural complexity.
- The three most important design lessons.

Use concise cards or callouts. This section should be understandable before reading any code.

Add a "How to explain this in an interview" callout:

- One sentence for the system type.
- One sentence for the harness control idea.
- One sentence for the hardest reliability/safety/cost tradeoff.

### 2. System Boundary

Explain the product contract:

- Inputs.
- Outputs.
- Entry surfaces.
- Success/failure judge.
- External systems: model providers, tools, browsers, databases, vector stores, workers, queues, APIs.

Include a system boundary diagram.

### 3. Request Lifecycle

Explain one representative request from user input to final answer/action.

Cover:

- Entry object or request message.
- Harness initialization.
- Context assembly.
- Model call.
- Tool/RAG/memory interaction.
- Artifact/event persistence.
- Completion or handoff.

Include a sequence diagram.

Use plain-language verbs. Do not write only "ClassA calls functionB"; explain what the system is deciding or changing at each step.

### 4. Harness And State Machine

Explain how the harness constrains behavior.

Cover:

- Runtime loop, graph, workflow, or framework-managed control flow.
- State transitions.
- Stop, retry, timeout, cancellation, interruption, and resume.
- Why this makes the agent controllable, recoverable, or auditable.

Include a state-machine or lifecycle diagram if the project exposes explicit states.

If explicit states are not named in code, infer the conceptual states from behavior and label them as inferred.

### 5. Context, Memory, And Project Concepts

Explain the system's working memory.

Cover:

- Model-visible prompt context.
- Hidden runtime state.
- Session/thread/task state.
- Message history, plans, tool observations, artifacts, RAG snippets, user/project metadata.
- Context budget strategy: summarization, trimming, retrieval, ranking, scoped artifacts, checkpoints.
- Long-term memory versus project knowledge versus task state.

Special cases:

- If `SOUL.md` and `USER.md` exist, include a comparison table: purpose, owner, write path, read path, prompt visibility, persistence, conflict rules, privacy risk, and why the separation matters.
- If instruction files such as `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `MEMORY.md`, or `PROFILE.md` exist, explain how they enter or influence the harness.
- Define project-native concepts such as session, thread, workspace, node, channel, skill, artifact, memory, or task before using them.

Include a context/state flow diagram.

For each context source, explain:

- Why it exists.
- How it is selected.
- Whether the model can see it.
- How it can become stale or unsafe.

### 5A. Terminology Glossary

Add this section when the report contains English architecture terms, project-specific nouns, or framework terms that a newcomer may not know.

The table of contents must link to this section. Do not create a glossary that is missing from the navigation.

Select terms from:

- Common agent architecture terms used in the report.
- Project-native terms that appear in code, docs, prompts, memory files, or UI labels.
- English-only phrases that are hard to translate directly.
- Interview-frequency agent design terms when they help the reader explain this project.

Include short explanations for terms such as:

- Workspace bootstrap files.
- Harness.
- Runtime.
- Context.
- Hidden runtime state.
- Artifact.
- Observation.
- Tool calling.
- Function calling.
- Tool validation.
- Guardrail.
- ReAct.
- Planner-executor.
- Agent orchestration.
- State management.
- Context engineering.
- MCP.
- Agentic RAG.
- GraphRAG.
- Control plane.
- Execution plane.
- Checkpoint.
- Replay.
- Trace.
- Handoff.
- Human-in-the-loop.
- Observability.
- Evals.
- Latency.
- Cost control.
- Rate limit.
- Fallback.
- RAG.
- Vector store.
- Rerank.

Each glossary item should be one to three sentences. Prefer practical meaning in this project over dictionary definitions.

Do not dump every term above. Include a term only when it appears in the project, the report uses it, or it is needed to explain a tradeoff a reader would likely be asked about in an agent architecture interview.

### 6. Model, Prompt, Tool, And Permission System

Explain how state becomes model calls and side effects.

Cover:

- Prompt assembly.
- Model/provider abstraction.
- Tool registry/discovery.
- Tool routing/filtering.
- Permission gates and sandbox boundaries.
- Tool execution, timeout, retry, errors, stdout/stderr, file/browser/database side effects.
- Observation format and context reinsertion.

Include a tool/action flow diagram.

Explain tool execution as a safety boundary: the model can request an action, but the runtime decides whether and how it happens.

### 7. RAG / Knowledge Pipeline

Use only when retrieval exists. If absent, explain what replaces it.

Cover:

- Sources and ingestion path.
- Parsing/chunking.
- Index/store construction.
- Retrieval trigger.
- Ranking/filtering/reranking/summarization.
- Prompt insertion and citations.
- Updates/invalidation/reindexing.
- Retrieval evals or quality checks.

Include a RAG pipeline diagram when present.

### 8. Single-Agent Long-Task Behavior

Use when one agent loop owns most work.

Cover:

- Goal/constraint/plan formation.
- Task workbench: todos, evidence, current files, artifacts, failures, partial results.
- Plan update, interruption, resume, and verification.
- Error recovery.
- Completion criteria.
- Main strengths and failure risks.

### 9. Multi-Agent Coordination

Use when multiple agents, roles, workers, or delegated loops exist.

Cover:

- Topology.
- Responsibility boundaries.
- Shared versus isolated state.
- Communication protocol.
- Context transfer.
- Permission model and final authority.
- Merge/adjudication/verification.
- Termination and loop prevention.
- Coordination cost and whether it is justified.

Include a multi-agent topology diagram when present.

### 10. Control Plane, Execution Plane, Events, And Safety

Use when the project has gateways, sandboxes, workers, queues, distributed runtime, browser automation, or policy boundaries.

Cover:

- Scheduling, routing, authorization, audit.
- Actual model/tool/browser/terminal/workflow execution.
- Event protocol and streaming.
- Human intervention points.
- Filesystem, terminal, network, database, browser, third-party API, and secret boundaries.

Include a control-plane/execution-plane diagram when useful.

### 11. Observability, Evaluation, And Replay

Explain how the project knows what happened and whether the agent works.

Cover:

- Traces, logs, model/tool events, costs, latency, state transitions, artifacts, errors.
- Session search, replay, audit, debugging workflow.
- Tests, evals, benchmarks, golden tasks, judge models, regression checks.
- Known quality gaps if static reading cannot prove effectiveness.

### 12. Design Judgment

Explain what a newcomer should learn.

Cover:

- Why the architecture likely exists.
- What it makes easier.
- What it makes harder.
- What could be simplified in a smaller project.
- Reusable patterns.
- Highest-risk assumptions.

Add interview-style explanation prompts:

- "If asked why this is more than a simple LLM wrapper, say..."
- "If asked how it handles long tasks, say..."
- "If asked how it controls unsafe actions, say..."
- "If asked how you would evaluate this system, say..."

### 13. Reading Path

Give a short ordered reading path. For each file:

- Why to read it.
- What design question it answers.
- What to read next.

Keep this list short. It is not a directory catalog.

### 14. Unknowns And Verification Checks

List important questions static reading could not prove.

For each:

- Unknown.
- Why it matters.
- File, test, command, trace, or runtime action that would verify it.

## Evidence Style

Use evidence citations like:

`src/runtime/harness.py::AgentHarness.run`

or:

`packages/server/src/events.ts`

Do not cite every supporting file. Cite only enough to make each architectural claim credible.

Explain first, cite second. File names, class names, and function names are evidence, not the explanation itself.

## Explanation Depth

Each major section must include three layers:

1. **Plain-language explanation**: explain the mechanism as if the reader knows LLMs but not this codebase.
2. **Architecture detail**: describe state, data flow, decisions, failure paths, and tradeoffs.
3. **Code evidence**: cite representative files/functions/classes that prove the claim.

Do not skip the first layer. A technically correct section that only names classes, modules, or functions is incomplete.

## Visual Style

Use:

- Clean typography.
- Left or top navigation.
- Section cards only when they group repeated items or callouts.
- Readable tables for comparisons such as `SOUL.md` versus `USER.md`.
- Diagram containers with titles, explanations, and source notes.
- Callouts for "Why it matters", "Design tradeoff", and "Risk".

Avoid:

- Decorative gradients or visual clutter.
- Giant directory trees.
- Raw inventory tables.
- Byte counts, extension histograms, exhaustive function lists, per-line explanations, or implementation recreation checklists.
