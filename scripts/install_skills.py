"""Copy complete skill folders without overwriting unrelated or edited installs."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

REPO = Path(__file__).resolve().parents[1]
RECEIPT = ".unreal-codex-install.json"


def hashes(folder):
    return {
        p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(folder.rglob("*"))
        if p.is_file() and p.name != RECEIPT
    }


def install(source_root, destination, update=False):
    source_root = Path(source_root).resolve()
    destination = Path(destination).resolve()
    sources = sorted(p.parent for p in source_root.glob("*/SKILL.md"))
    if not sources:
        raise ValueError(f"No skills found in {source_root}")
    plans = []
    # Preflight all targets before touching any install.
    for source in sources:
        target = destination / source.name
        if target == source or target.is_relative_to(source) or source.is_relative_to(target):
            raise ValueError(f"Source and destination overlap: {target}")
        if target.is_symlink() or getattr(target, "is_junction", lambda: False)():
            raise ValueError(f"Refusing linked destination: {target}")
        if target.exists():
            receipt = target / RECEIPT
            if not update or not receipt.is_file():
                raise ValueError(f"Existing skill; preserve or relocate it first: {target}")
            recorded = json.loads(receipt.read_text(encoding="utf-8"))
            if recorded.get("source") != str(source):
                raise ValueError(f"Skill belongs to a different source: {target}")
            if recorded.get("files") != hashes(target):
                raise ValueError(f"Skill has local edits; refusing overwrite: {target}")
        plans.append((source, target))
    destination.mkdir(parents=True, exist_ok=True)
    for source, target in plans:
        # Stage the complete new folder; retain the previous install until success.
        with tempfile.TemporaryDirectory(prefix=".unreal-install-", dir=destination) as stage:
            staged = Path(stage) / source.name
            shutil.copytree(source, staged)
            (staged / "LICENSE").write_bytes((source_root.parent / "LICENSE").read_bytes())
            (staged / RECEIPT).write_text(
                json.dumps({"source": str(source), "files": hashes(staged)}, indent=2) + "\n",
                encoding="utf-8",
            )
            backup = Path(stage) / "previous"
            if target.exists():
                target.rename(backup)
            try:
                staged.rename(target)
            except OSError:
                if backup.exists():
                    backup.rename(target)
                raise
        print(f"Installed {source.name}: {target}")
    return [target for _, target in plans]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--project", type=Path, help="Install in PROJECT/.agents/skills")
    scope.add_argument("--destination", type=Path, help="Explicit skill root")
    parser.add_argument("--update", action="store_true", help="Update unmodified managed installs")
    args = parser.parse_args()
    if args.project and not args.project.is_dir():
        parser.error("--project must name an existing project directory")
    destination = args.destination or (
        args.project / ".agents" / "skills" if args.project else Path.home() / ".agents" / "skills"
    )
    try:
        install(REPO / "skills", destination, args.update)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f"Install stopped: {error}\n")


if __name__ == "__main__":
    main()
