"""Validate skill discovery metadata, references, examples and plugin packaging."""

import json
from pathlib import Path
import re
import sys
import tomllib

import yaml

REPO = Path(__file__).resolve().parents[1]


def validate(repo=REPO):
    errors = []
    repo = Path(repo)
    plugin = json.loads((repo / "plugin.json").read_text(encoding="utf-8"))
    if plugin.get("name") != "unreal-engine-skills-for-codex":
        errors.append("Unexpected plugin identity")
    for entry in sorted((repo / "skills").glob("*/SKILL.md")):
        skill = entry.parent
        text = entry.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append(f"{entry}: missing YAML frontmatter")
            continue
        data = yaml.safe_load(match.group(1))
        name = data.get("name", "")
        if name != skill.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) >= 64:
            errors.append(f"{entry}: invalid name")
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            errors.append(f"{entry}: missing description")
        ui = yaml.safe_load((skill / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        interface = ui.get("interface", {})
        if not 25 <= len(interface.get("short_description", "")) <= 64:
            errors.append(f"{skill}: short_description must have 25-64 characters")
        if f"${name}" not in interface.get("default_prompt", ""):
            errors.append(f"{skill}: default_prompt must mention skill")
        reached = {entry.resolve()}
        pending = [entry]
        while pending:
            doc = pending.pop()
            # Ignore fenced examples, which can illustrate nonexistent project paths.
            body = re.sub(r"```.*?```", "", doc.read_text(encoding="utf-8"), flags=re.S)
            for link in re.findall(r"\]\(([^)]+)\)", body):
                if re.match(r"[a-zA-Z]+:|#", link):
                    continue
                path = (doc.parent / link.split("#")[0]).resolve()
                if not path.is_relative_to(skill.resolve()) or not path.is_file():
                    errors.append(f"{doc}: broken or nonportable reference {link}")
                elif path.suffix == ".md" and path not in reached:
                    reached.add(path)
                    pending.append(path)
        for reference in (skill / "references").glob("*.md"):
            if reference.resolve() not in reached:
                errors.append(f"{reference}: unreachable reference")
        print(f"Validated {skill.name}")
    for example in (repo / "examples").glob("*.toml"):
        tomllib.loads(example.read_text(encoding="utf-8"))
    if len(list((repo / "skills").glob("*/SKILL.md"))) != 3:
        errors.append("Expected all three ported skills")
    return errors


if __name__ == "__main__":
    problems = validate()
    for problem in problems:
        print(problem, file=sys.stderr)
    sys.exit(bool(problems))
