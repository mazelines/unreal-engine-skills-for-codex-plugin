"""Build complete, reproducible per-skill ZIPs and an integrity manifest."""

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

REPO = Path(__file__).resolve().parents[1]


def package(repo, output):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    if output.is_relative_to(repo / "skills"):
        raise ValueError("Output must be outside the skill folders")
    output.mkdir(parents=True, exist_ok=True)
    manifest = {"plugin": json.loads((repo / "plugin.json").read_text(encoding="utf-8")), "skills": {}}
    for entry in sorted((repo / "skills").glob("*/SKILL.md")):
        skill = entry.parent
        files = {p.relative_to(skill).as_posix(): p.read_bytes() for p in sorted(skill.rglob("*")) if p.is_file()}
        files["LICENSE"] = (repo / "LICENSE").read_bytes()
        archive = output / f"{skill.name}.zip"
        with ZipFile(archive, "w", compression=ZIP_DEFLATED) as zipped:
            for relative, data in sorted(files.items()):
                info = ZipInfo(f"{skill.name}/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                zipped.writestr(info, data)
        manifest["skills"][skill.name] = {
            "archive": archive.name,
            "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())},
        }
        print(f"Packaged {skill.name}: {len(files)} files")
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPO / "dist")
    arguments = parser.parse_args()
    package(REPO, arguments.output)
