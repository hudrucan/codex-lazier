"""Focused packaging regression; uses only the Python standard library."""

from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent.parent


class PackageValidationTests(unittest.TestCase):
    def test_interface_text_can_change_without_weakening_validation(self):
        with TemporaryDirectory(prefix="codex-lazier-metadata-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copytree(ROOT / "adapters", root / "adapters")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            metadata = root / "skills/codex-lazier/agents/openai.yaml"
            original = metadata.read_text(encoding="utf-8")
            changed = re.sub(r'(?m)^  display_name:.*$', '  display_name: "Codex Lazier"', original)
            changed = re.sub(r'(?m)^  short_description:.*$', '  short_description: "Review engineering complexity"', changed)
            changed = re.sub(r'(?m)^  default_prompt:.*$', '  default_prompt: "Review the supplied design."', changed)
            cases = [("changed UI text", changed, True),
                     ("missing interface", "policy:\n  allow_implicit_invocation: false\n", False),
                     ("explicit-only invocation", original.replace("true", "false"), False)]
            for field in ["display_name", "short_description", "default_prompt"]:
                cases.append((f"missing {field}", re.sub(rf"(?m)^  {field}:.*\n", "", original), False))
                cases.append((f"empty {field}", re.sub(rf"(?m)^  {field}:.*$", f'  {field}: " "', original), False))
            cases.append(("invalid quoted string", re.sub(r'(?m)^  display_name:.*$',
                                                          '  display_name: "Codex "Lazier""', original), False))
            for label, content, valid in cases:
                with self.subTest(label=label):
                    metadata.write_text(content, encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(root / "tools/package.py"), "--build"],
                        capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode == 0, valid, result.stderr)
                    self.assertEqual("PASS:" in result.stdout, valid)
                    if not valid:
                        self.assertIn("FAIL:", result.stderr)

    def test_description_with_unquoted_colon_is_rejected(self):
        with TemporaryDirectory(prefix="codex-lazier-regression-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copytree(ROOT / "adapters", root / "adapters")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            manifest = root / "skills/codex-lazier/SKILL.md"
            manifest.write_text(re.sub(
                r"(?m)^description:.*$",
                "description: Review changes: keep them simple.",
                manifest.read_text(encoding="utf-8"),
            ), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(root / "tools/package.py"), "--build"],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL:", result.stderr)
            self.assertNotIn("PASS:", result.stdout)

    def test_distribution_includes_current_adapters_and_rejects_stale_bytes(self):
        with TemporaryDirectory(prefix="codex-lazier-archive-") as directory:
            root = Path(directory)
            for name in ["skills", "adapters"]:
                shutil.copytree(ROOT / name, root / name)
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")

            def run(*args):
                return subprocess.run(
                    [sys.executable, str(root / "tools/package.py"), *args],
                    capture_output=True, text=True,
                )

            version = runpy.run_path(str(root / "tools/package.py"))["VERSION"]
            for tag in ["v0.0.0", version, f"v{version}-rc.1"]:
                with self.subTest(tag=tag):
                    rejected = run("--build", "--tag", tag)
                    self.assertNotEqual(rejected.returncode, 0)
                    self.assertIn("Release tag mismatch", rejected.stderr)
                    self.assertFalse((root / "dist").exists(), "Reject mismatched tags before building")

            built = run("--build", "--tag", f"v{version}")
            self.assertEqual(built.returncode, 0, built.stderr)
            archive = next((root / "dist").glob("*.zip"))
            before = archive.read_bytes()
            with ZipFile(archive) as bundle:
                self.assertEqual(len(bundle.namelist()), 6)
                for adapter in ["codex/AGENTS.md", "chatgpt/project-instructions.md"]:
                    self.assertEqual(bundle.read("codex-lazier/adapters/" + adapter),
                                     (root / "adapters" / adapter).read_bytes())
                self.assertEqual(bundle.read("codex-lazier/LICENSE"), (root / "LICENSE").read_bytes())
            self.assertEqual(run("--build").returncode, 0)
            self.assertEqual(archive.read_bytes(), before, "Build must be reproducible")

            adapter = root / "adapters/codex/AGENTS.md"
            adapter.write_text(adapter.read_text(encoding="utf-8") + "\nNew default.\n", encoding="utf-8")
            stale = run()
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("Stale archive content", stale.stderr)
            self.assertNotIn("PASS:", stale.stdout)

            self.assertEqual(run("--build").returncode, 0)
            archive.with_suffix(".sha256").write_text("wrong\n", encoding="utf-8")
            corrupt = run()
            self.assertNotEqual(corrupt.returncode, 0)
            self.assertIn("checksum mismatch", corrupt.stderr)


if __name__ == "__main__":
    unittest.main()
