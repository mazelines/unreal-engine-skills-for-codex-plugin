import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install_skills import install, RECEIPT
from package_skills import package


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.skills = self.repo / "skills"
        self.destination = Path(self.temp.name) / "installed"
        self.skills.mkdir(parents=True)
        (self.repo / "LICENSE").write_text("Example license", encoding="utf-8")
        (self.repo / "plugin.json").write_text('{"name":"test"}', encoding="utf-8")
        for name in ("a", "b"):
            root = self.skills / name
            (root / "references").mkdir(parents=True)
            (root / "SKILL.md").write_text(name, encoding="utf-8")
            (root / "references" / "guide.md").write_text("guide", encoding="utf-8")

    def test_complete_install_and_managed_update_remove_stale_files(self):
        install(self.skills, self.destination)
        self.assertEqual((self.destination / "a/references/guide.md").read_text(), "guide")
        self.assertTrue((self.destination / "a/LICENSE").is_file())
        (self.skills / "a/references/guide.md").unlink()
        (self.skills / "a/SKILL.md").write_text("revised", encoding="utf-8")
        install(self.skills, self.destination, update=True)
        self.assertFalse((self.destination / "a/references/guide.md").exists())
        self.assertEqual((self.destination / "a/SKILL.md").read_text(), "revised")

    def test_unmanaged_collision_does_not_partially_install(self):
        (self.destination / "b").mkdir(parents=True)
        (self.destination / "b/SKILL.md").write_text("user content", encoding="utf-8")
        with self.assertRaises(ValueError):
            install(self.skills, self.destination, update=True)
        self.assertFalse((self.destination / "a").exists())
        self.assertEqual((self.destination / "b/SKILL.md").read_text(), "user content")

    def test_local_edits_block_update(self):
        install(self.skills, self.destination)
        (self.destination / "b/references/guide.md").write_text("user edit", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "local edits"):
            install(self.skills, self.destination, update=True)
        self.assertEqual((self.destination / "b/references/guide.md").read_text(), "user edit")

    def test_overlap_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            install(self.skills, self.skills)

    def test_packages_include_all_files_and_hashes_are_reproducible(self):
        output = Path(self.temp.name) / "dist"
        first = package(self.repo, output)
        second = package(self.repo, output)
        self.assertEqual(first, second)
        for name, record in first["skills"].items():
            archive = output / record["archive"]
            self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), record["sha256"])
            with ZipFile(archive) as zipped:
                self.assertIsNone(zipped.testzip())
                self.assertEqual(set(zipped.namelist()), {f"{name}/{p}" for p in record["files"]})
                for relative, expected in record["files"].items():
                    self.assertEqual(hashlib.sha256(zipped.read(f"{name}/{relative}")).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
