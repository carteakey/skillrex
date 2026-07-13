#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MARKETPLACE_DIR = ROOT / "marketplace"


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict[str, object] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
            data[key.strip()] = items
        else:
            data[key.strip()] = value.strip("'\"")
    return data


def skill_entry(skill_md: Path) -> dict[str, object]:
    rel_dir = skill_md.parent.relative_to(SKILLS_DIR)
    parts = rel_dir.parts
    meta = parse_frontmatter(skill_md)
    name = str(meta.get("name") or parts[-1])
    category = parts[0] if len(parts) > 1 else ""
    scripts = sorted(
        str(path.relative_to(skill_md.parent))
        for path in skill_md.parent.glob("scripts/**/*")
        if path.is_file()
    )
    references = sorted(
        str(path.relative_to(skill_md.parent))
        for path in skill_md.parent.glob("references/**/*")
        if path.is_file()
    )
    templates = sorted(
        str(path.relative_to(skill_md.parent))
        for path in skill_md.parent.glob("templates/**/*")
        if path.is_file()
    )
    return {
        "name": name,
        "path": str(rel_dir),
        "category": category,
        "description": meta.get("description", ""),
        "version": meta.get("version", ""),
        "platforms": meta.get("platforms", []),
        "scripts": scripts,
        "references": references,
        "templates": templates,
    }


def main() -> None:
    MARKETPLACE_DIR.mkdir(exist_ok=True)
    skills = [skill_entry(path) for path in sorted(SKILLS_DIR.glob("**/SKILL.md"))]
    index = {
        "name": "skillrex",
        "description": "Kartikey's personal portable AI-agent skills marketplace.",
        "schema_version": 1,
        "skills": skills,
    }
    (MARKETPLACE_DIR / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    rows = ["# skillrex Catalog", ""]
    for skill in skills:
        rows.append(f"## {skill['name']}")
        rows.append("")
        rows.append(f"- Path: `{skill['path']}`")
        if skill["category"]:
            rows.append(f"- Category: `{skill['category']}`")
        if skill["description"]:
            rows.append(f"- Description: {skill['description']}")
        if skill["scripts"]:
            rows.append(f"- Scripts: {len(skill['scripts'])}")
        if skill["references"]:
            rows.append(f"- References: {len(skill['references'])}")
        if skill["templates"]:
            rows.append(f"- Templates: {len(skill['templates'])}")
        rows.append("")
    (MARKETPLACE_DIR / "catalog.md").write_text("\n".join(rows), encoding="utf-8")


if __name__ == "__main__":
    main()
