"""Read AI/ML learnings from the knowledge folder. Stdlib only. Read-only on knowledge/."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Learning:
    path: str
    title: str
    body: str
    pillar: str


def read_knowledge(knowledge_dir="knowledge"):
    """Return learnings from *.md files in knowledge_dir, sorted by filename.

    Each file may start with `Pillar: <name>`. The title is the first H1 heading,
    falling back to the filename stem. README.md is skipped.
    """
    knowledge_dir = Path(knowledge_dir)
    learnings = []
    if not knowledge_dir.exists():
        return learnings
    for path in sorted(knowledge_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        pillar = "general"
        body = text
        first = text.split("\n", 1)[0].strip()
        if first.lower().startswith("pillar:"):
            pillar = first.split(":", 1)[1].strip()
            body = text.split("\n", 1)[1] if "\n" in text else ""
        title = path.stem
        for line in body.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break
        learnings.append(Learning(str(path), title, body.strip(), pillar))
    return learnings
