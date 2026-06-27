#!/usr/bin/env python3
"""Build a read-only internal evidence inventory for LLM-agent design analysis."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".turbo",
    ".parcel-cache",
    "target",
    "out",
    ".idea",
    ".vscode",
}

SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_dsa",
    "id_ed25519",
    "credentials",
    "credentials.json",
    "secrets.json",
}

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".7z",
    ".mp4",
    ".mov",
    ".avi",
    ".mp3",
    ".wav",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".pyc",
}

MANIFEST_NAMES = {
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "poetry.lock",
    "uv.lock",
    "Pipfile",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "Makefile",
    "docker-compose.yml",
    "Dockerfile",
}

ENTRYPOINT_NAMES = {
    "main.py",
    "app.py",
    "server.py",
    "cli.py",
    "index.ts",
    "index.tsx",
    "index.js",
    "index.jsx",
    "main.ts",
    "main.js",
    "server.ts",
    "server.js",
}

INSTRUCTION_MEMORY_NAMES = {
    "agents.md",
    "claude.md",
    "skill.md",
    "skills.md",
    "memory.md",
    "profile.md",
    "user.md",
    "soul.md",
    "persona.md",
}

AGENT_TERMS = {
    "harness": ["harness", "runtime", "runner", "bootstrap", "entrypoint", "invoke", "dispatch", "gateway"],
    "agent": ["agent", "planner", "executor", "orchestrator", "workflow", "graph", "stategraph", "supervisor", "worker"],
    "tools": ["tool", "tools", "function_call", "function call", "mcp", "action", "actions"],
    "model": ["llm", "model", "openai", "anthropic", "claude", "chatcompletion", "responses", "generate"],
    "prompt": ["prompt", "system message", "system_prompt", "template", "jinja"],
    "state-context": ["state", "context", "session", "thread", "checkpoint", "history", "resume", "replay"],
    "memory-rag": ["memory", "retriever", "retrieval", "rag", "vector", "embedding", "knowledge", "index"],
    "artifact-event": ["artifact", "event", "stream", "trace", "checkpoint", "approval", "observation"],
    "permission-safety": ["permission", "policy", "sandbox", "approval", "secret", "credential", "allowlist", "denylist"],
    "eval-observability": ["eval", "evaluation", "benchmark", "dataset", "judge", "golden", "trace", "telemetry", "metric"],
    "instruction-memory": ["soul", "persona", "profile", "user preference", "instruction", "memory"],
}

MAX_TEXT_BYTES = 512_000
MAX_FILES = 20_000


@dataclass
class FileRecord:
    path: str
    size: int
    extension: str
    role: list[str]
    term_hits: dict[str, int]


def is_ignored_dir(path: Path) -> bool:
    return path.name in IGNORE_DIRS


def is_sensitive(path: Path) -> bool:
    lower_name = path.name.lower()
    if lower_name in SENSITIVE_NAMES:
        return True
    sensitive_fragments = ("secret", "token", "private_key", "apikey", "api_key")
    return any(fragment in lower_name for fragment in sensitive_fragments)


def is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return False
    return True


def iter_files(root: Path) -> Iterable[Path]:
    count = 0
    for current_root, dirs, files in os.walk(root):
        current_path = Path(current_root)
        dirs[:] = [directory for directory in dirs if not is_ignored_dir(current_path / directory)]
        for file_name in files:
            path = current_path / file_name
            if is_sensitive(path) or not is_probably_text(path):
                continue
            count += 1
            if count > MAX_FILES:
                return
            yield path


def read_text_for_scan(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_TEXT_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def classify_roles(path: Path, rel_path: str, text: str) -> list[str]:
    lower_path = rel_path.lower().replace("\\", "/")
    name = path.name
    roles: list[str] = []

    if name in MANIFEST_NAMES:
        roles.append("manifest")
    if name.lower().startswith("readme") or "/docs/" in f"/{lower_path}":
        roles.append("docs")
    if name in ENTRYPOINT_NAMES or "if __name__ == \"__main__\"" in text:
        roles.append("entrypoint")
    if name.lower() in INSTRUCTION_MEMORY_NAMES:
        roles.append("instruction-memory")
    if any(part in lower_path for part in ("/test", "tests/", "__tests__", ".spec.", ".test.")):
        roles.append("test")
    if any(part in lower_path for part in ("harness", "runtime", "runner", "bootstrap", "gateway")):
        roles.append("harness")
    if any(part in lower_path for part in ("agent", "planner", "executor", "orchestrator", "workflow", "graph", "supervisor", "worker")):
        roles.append("agent-core")
    if any(part in lower_path for part in ("tool", "tools", "mcp", "action", "actions")):
        roles.append("tools")
    if any(part in lower_path for part in ("prompt", "prompts", "template", "templates")):
        roles.append("prompts")
    if any(part in lower_path for part in ("memory", "retrieval", "retriever", "rag", "vector", "embedding")):
        roles.append("memory-rag")
    if any(part in lower_path for part in ("state", "context", "session", "thread", "checkpoint", "replay")):
        roles.append("state-context")
    if any(part in lower_path for part in ("artifact", "artifacts", "event", "events", "stream", "trace", "traces")):
        roles.append("artifact-event")
    if any(part in lower_path for part in ("permission", "policy", "sandbox", "approval", "guard", "auth", "security")):
        roles.append("permission-safety")
    if any(part in lower_path for part in ("model", "llm", "provider", "openai", "anthropic", "claude")):
        roles.append("model-provider")
    if any(part in lower_path for part in ("eval", "benchmark", "dataset", "golden", "telemetry", "observability")):
        roles.append("eval")
    if any(part in lower_path for part in ("api", "routes", "server", "controller")):
        roles.append("api")
    if any(part in lower_path for part in ("ui", "frontend", "app/", "pages/", "components/")):
        roles.append("ui")

    if not roles:
        roles.append("source" if path.suffix else "other")
    return roles


def count_terms(text: str) -> dict[str, int]:
    lower_text = text.lower()
    hits: dict[str, int] = {}
    for group, terms in AGENT_TERMS.items():
        total = sum(lower_text.count(term) for term in terms)
        if total:
            hits[group] = total
    return hits


def build_inventory(root: Path) -> dict:
    records: list[FileRecord] = []
    ext_counter: Counter[str] = Counter()
    role_counter: Counter[str] = Counter()
    directory_roles: dict[str, Counter[str]] = defaultdict(Counter)

    for path in iter_files(root):
        try:
            size = path.stat().st_size
        except OSError:
            continue
        rel_path = path.relative_to(root).as_posix()
        text = read_text_for_scan(path)
        roles = classify_roles(path, rel_path, text)
        hits = count_terms(text)
        extension = path.suffix.lower() or "[none]"

        ext_counter[extension] += 1
        for role in roles:
            role_counter[role] += 1
            top_dir = rel_path.split("/", 1)[0]
            directory_roles[top_dir][role] += 1

        if roles != ["source"] or hits:
            records.append(FileRecord(rel_path, size, extension, roles, hits))

    priority = {
        "entrypoint": 0,
        "harness": 1,
        "agent-core": 2,
        "state-context": 3,
        "instruction-memory": 4,
        "tools": 5,
        "permission-safety": 6,
        "artifact-event": 7,
        "model-provider": 8,
        "prompts": 9,
    }
    records.sort(key=lambda item: (min((priority.get(role, 20) for role in item.role), default=20), item.path))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "file_count": sum(ext_counter.values()),
        "extensions": dict(ext_counter.most_common()),
        "roles": dict(role_counter.most_common()),
        "directories": {
            directory: dict(counter.most_common())
            for directory, counter in sorted(directory_roles.items())
        },
        "high_signal_files": [asdict(record) for record in records[:500]],
        "limits": {
            "max_files": MAX_FILES,
            "max_text_bytes_per_file": MAX_TEXT_BYTES,
        },
    }


def write_outputs(root: Path, out_dir: Path, inventory: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a read-only internal evidence inventory for LLM-agent design analysis.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository root to inspect.")
    parser.add_argument("--out", default="agent-codebase-analysis/.analysis-work", help="Internal output directory for inventory.json.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.repo).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Repository path does not exist or is not a directory: {root}")
    out_dir = Path(args.out).expanduser()
    if not out_dir.is_absolute():
        out_dir = root / out_dir
    inventory = build_inventory(root)
    write_outputs(root, out_dir.resolve(), inventory)
    print(f"Wrote {out_dir / 'inventory.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

