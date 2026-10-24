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
    def test_web_prompts_preserve_relevant_context_and_async_routing(self):
        web = (ROOT / "skills/codex-lazier/references/web.md").read_text(encoding="utf-8")
        continuity = web.split("For `[C2C Plan]`, `[C2C Task]` and `[C2C Fix]`", 1)[1]
        continuity = " ".join(continuity.split("A handoff whose first line", 1)[0].split())
        for intent, required in {
            "Plan": ["goals", "constraints", "checked evidence", "options/trade-offs",
                     "unresolved questions"],
            "Task": ["settled Plan decisions (if any)", "verified findings", "file/line",
                     "repair direction", "validation", "does not require a prior Plan"],
            "Fix": ["latest audit", "file/line", "evidence", "impact", "proposed fix"],
        }.items():
            section = continuity.split(f"**{intent}:**", 1)[1].split(" - **", 1)[0]
            for requirement in required:
                with self.subTest(intent=intent, requirement=requirement):
                    self.assertIn(requirement, section)
        for requirement in [
            "only relevant, still-valid context",
            "separating verified findings, assumptions and open questions",
            "Do not require Codex to re-audit everything Web checked",
            "inspection of current source before editing",
            "preserve routing and an already-selected `async=true`",
            "Never switch to manual, reuse a callback ticket or create a new task to evade limits",
        ]:
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, continuity)

    def test_skill_links_must_resolve_in_the_installed_package(self):
        with TemporaryDirectory(prefix="codex-lazier-links-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            (root / "README.md").write_text("Repository-only documentation.\n", encoding="utf-8")
            manifest = root / "skills/codex-lazier/SKILL.md"
            original = manifest.read_text(encoding="utf-8")
            for target in ["references/missing.md", "../../README.md"]:
                with self.subTest(target=target):
                    manifest.write_text(original + f"\n[Reference]({target})\n", encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(root / "tools/package.py"), "--build"],
                        capture_output=True, text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Broken package link", result.stderr)
                    self.assertFalse((root / "dist").exists())

    def test_interface_text_can_change_without_weakening_validation(self):
        with TemporaryDirectory(prefix="codex-lazier-metadata-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
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

    def test_distribution_includes_current_references_and_rejects_stale_bytes(self):
        with TemporaryDirectory(prefix="codex-lazier-archive-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
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
                self.assertCountEqual(bundle.namelist(), [
                    "codex-lazier/SKILL.md", "codex-lazier/agents/openai.yaml",
                    "codex-lazier/references/policy.md", "codex-lazier/references/web.md",
                    "codex-lazier/references/codex.md", "codex-lazier/LICENSE",
                ])
                for reference in ["policy.md", "codex.md", "web.md"]:
                    self.assertEqual(bundle.read("codex-lazier/references/" + reference),
                                     (root / "skills/codex-lazier/references" / reference).read_bytes())
                self.assertEqual(bundle.read("codex-lazier/LICENSE"), (root / "LICENSE").read_bytes())
                installed = root / "installed"
                bundle.extractall(installed)
            skill = (installed / "codex-lazier").resolve()
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)",
                               (skill / "SKILL.md").read_text(encoding="utf-8"))
            for reference in ["policy", "codex", "web"]:
                self.assertIn(f"references/{reference}.md", links)
            for source in skill.rglob("*.md"):
                for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                    if "://" not in target and not target.startswith("#"):
                        resolved = (source.parent / target.split("#", 1)[0]).resolve()
                        self.assertTrue(resolved.is_relative_to(skill))
                        self.assertTrue(resolved.is_file(), target)
            self.assertEqual(run("--build").returncode, 0)
            self.assertEqual(archive.read_bytes(), before, "Build must be reproducible")

            for name in ["codex", "web"]:
                with self.subTest(stale_reference=name):
                    reference = root / f"skills/codex-lazier/references/{name}.md"
                    reference.write_text(reference.read_text(encoding="utf-8") + "\nNew default.\n", encoding="utf-8")
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
