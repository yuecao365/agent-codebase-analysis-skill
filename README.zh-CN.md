# Agent Codebase Analysis Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-111827.svg)](SKILL.md)
[![Codex](https://img.shields.io/badge/Codex-compatible-10a37f.svg)](https://developers.openai.com/codex/skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-6b5cff.svg)](https://code.claude.com/docs/en/skills)
[![English README](https://img.shields.io/badge/README-English-blue.svg)](README.md)

`analyze-agent-codebase` 是一个用于分析 LLM Agent 项目的 Agent Skill。

它的目标不是生成文件清单，而是帮助你快速理解一个成熟 agent 项目“作为系统是如何运转的”：harness 如何约束模型行为、上下文如何进入 prompt、工具如何授权和执行、RAG 如何检索、memory 和状态如何区分、单 agent 如何推进长任务、多 agent 如何协作，以及这些设计如何清楚地讲给别人听。

## 示例报告

- [查看 OpenClaw 中文示例报告](https://htmlpreview.github.io/?https://github.com/yuecao365/agent-codebase-analysis-skill/blob/main/examples/openclaw/agent-architecture-analysis.html)
- [打开仓库中的 HTML 文件](examples/openclaw/agent-architecture-analysis.html)

## 输出结果

Skill 会生成一个面向用户阅读的 HTML 文件：

```text
agent-codebase-analysis/agent-architecture-analysis.html
```

报告通常包括：

- 项目定位、agent 类型和核心设计结论。
- harness / runtime loop / 状态机分析。
- context、memory、prompt、artifact、event、persistence 的流转。
- 工具注册、权限检查、执行、重试、observation 和失败处理。
- 如果项目有 RAG，会分析 ingestion、chunking、index、retrieval、rerank、citation。
- 单智能体长任务推进机制。
- 多智能体拓扑、职责边界、通信、合并和协调成本。
- 可放大的 Mermaid 架构图。
- 项目术语、英文术语、面试高频 agent 术语表。
- 高价值源码阅读路径和静态分析无法确认的问题。

## 快速安装

同时安装到 Codex 和 Claude Code：

```bash
npx skills add yuecao365/agent-codebase-analysis-skill -g --agent codex claude-code
```

只安装到 Codex：

```bash
npx skills add yuecao365/agent-codebase-analysis-skill -g --agent codex
```

只安装到 Claude Code：

```bash
npx skills add yuecao365/agent-codebase-analysis-skill -g --agent claude-code
```

安装后重启对应的 agent 环境。

## 其他安装方式

Codex 内置安装器：

```text
Use $skill-installer to install https://github.com/yuecao365/agent-codebase-analysis-skill.git globally.
```

GitHub CLI：

```bash
gh skill install yuecao365/agent-codebase-analysis-skill
```

手动 clone：

```bash
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git ~/.agents/skills/analyze-agent-codebase
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git ~/.claude/skills/analyze-agent-codebase
```

Windows 手动 clone：

```powershell
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.agents\skills\analyze-agent-codebase
git clone https://github.com/yuecao365/agent-codebase-analysis-skill.git $env:USERPROFILE\.claude\skills\analyze-agent-codebase
```

没有安装 Git 时，可以在 GitHub 页面点击 **Code -> Download ZIP**，解压后把文件夹改名为 `analyze-agent-codebase`，再放进 Codex 或 Claude 的 skills 目录。

## 使用方式

```text
Use $analyze-agent-codebase to analyze /path/to/agent-project.
```

也可以更明确地要求：

```text
Use $analyze-agent-codebase to explain this repo as an agent harness, not as a file tree.
```

```text
Use $analyze-agent-codebase to create an HTML architecture report with zoomable Mermaid diagrams and a glossary.
```

```text
Use $analyze-agent-codebase to analyze whether this multi-agent design is justified or mostly coordination overhead.
```

## 分析重点

| 方向 | 关键问题 |
| --- | --- |
| Harness | runtime 负责哪些决策，而不是让模型自由发挥？ |
| Context | 哪些内容进入 prompt，哪些只是隐藏运行时状态？ |
| Tools | 工具调用如何校验、授权、执行并转回 observation？ |
| RAG | 文档如何进入索引，如何检索、排序、引用和更新？ |
| Memory | 临时状态、长期记忆、项目知识、用户偏好如何区分？ |
| Agents | 单 agent 如何推进长任务，多 agent 如何分工协作？ |
| Safety | 权限、审批、沙箱、重试和失败路径在哪里控制？ |
| Observability | 一次运行能否 trace、replay、eval 和 debug？ |

## 仓库结构

```text
SKILL.md
agents/openai.yaml
evals/evals.json
references/
scripts/repo_inventory.py
examples/openclaw/
```

## 开发校验

```bash
python path/to/skill-creator/scripts/quick_validate.py .
python -m py_compile scripts/repo_inventory.py
git diff --check
```

## License

MIT
