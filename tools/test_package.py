"""Focused packaging regression; uses only the Python standard library."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parent.parent


class PackageValidationTests(unittest.TestCase):
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
                     ("implicit invocation", original.replace("false", "true"), False)]
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


if __name__ == "__main__":
    unittest.main()
