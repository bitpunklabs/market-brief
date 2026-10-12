"""Verify distribution integrity and failure boundaries, without model calls."""

import contextlib
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check import ROOT, check, package_files
from package_release import build


class PackageTests(unittest.TestCase):
    def test_reproducible_archive_and_extracted_package(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            first = build(base / "first")
            second = build(base / "second")
            self.assertEqual(first["sha256"], second["sha256"])
            archive = base / "first" / first["archive"]
            self.assertEqual(first["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())
            with zipfile.ZipFile(archive) as bundle:
                bundle.extractall(base / "extracted")
            extracted = base / "extracted/market-brief"
            self.assertEqual(check(extracted)["prompts"], check()["prompts"])
            for path in package_files():
                self.assertEqual(path.read_bytes(), (extracted / path.relative_to(ROOT)).read_bytes())
            self.assertFalse((extracted / "temp").exists())
            self.assertFalse((extracted / ".git").exists())

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            sentinel = output / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "new or empty"):
                build(output)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(output.iterdir()), [sentinel])

    def test_mismatched_tag_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "new"
            with self.assertRaisesRegex(ValueError, "tag does not match"):
                build(output, tag="v999.0.0")
            self.assertFalse(output.exists())

    @contextlib.contextmanager
    def copied_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in package_files():
                destination = root / path.relative_to(ROOT)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, destination)
            yield root

    def test_missing_prompt_is_rejected(self):
        with self.copied_package() as root:
            next((root / "assets/prompts").glob("*.md")).unlink()
            with self.assertRaisesRegex(ValueError, "Skill routing must reference every prompt"):
                check(root)

    def test_new_market_requires_route_and_readme_link(self):
        with self.copied_package() as root:
            expected_count = check(root)["prompts"] + 1
            prompt = root / "assets/prompts/test-equity-premarket-prompt.md"
            # Use a real full prompt to exercise library registration, not its semantics.
            shutil.copyfile(root / "assets/prompts/us-premarket-prompt.md", prompt)
            with self.assertRaisesRegex(ValueError, "Skill routing must reference every prompt"):
                check(root)
            link = "[Test market](assets/prompts/test-equity-premarket-prompt.md)"
            with (root / "SKILL.md").open("a", encoding="utf-8") as handle:
                handle.write("\n| Test equity market | Premarket | " + link + " |\n")
            with self.assertRaisesRegex(ValueError, "README must link every supported prompt"):
                check(root)
            with (root / "README.md").open("a", encoding="utf-8") as handle:
                handle.write("\n" + link + "\n")
            self.assertEqual(check(root)["prompts"], expected_count)
            self.assertIn(prompt, package_files(root))
            output = root / "distribution"
            subprocess.run(
                [sys.executable, str(root / "scripts/package_release.py"), "--output", str(output)],
                check=True, capture_output=True, text=True,
            )
            with zipfile.ZipFile(next(output.glob("*.zip"))) as bundle:
                self.assertEqual(
                    bundle.read("market-brief/assets/prompts/" + prompt.name), prompt.read_bytes()
                )
                bundle.extractall(root / "extracted")
            self.assertEqual(check(root / "extracted/market-brief")["prompts"], expected_count)

    def test_empty_prompt_library_is_rejected(self):
        with self.copied_package() as root:
            for prompt in (root / "assets/prompts").glob("*.md"):
                prompt.unlink()
            with self.assertRaisesRegex(ValueError, "Prompt library must contain at least one"):
                check(root)

    def test_duplicate_prompt_route_is_rejected(self):
        with self.copied_package() as root:
            with (root / "SKILL.md").open("a", encoding="utf-8") as handle:
                handle.write("\n[Duplicate](assets/prompts/us-premarket-prompt.md)\n")
            with self.assertRaisesRegex(ValueError, "Skill routing must reference every prompt"):
                check(root)

    def test_adaptation_guide_is_required_in_package(self):
        with self.copied_package() as root:
            (root / "references/market-adaptation.md").unlink()
            with self.assertRaisesRegex(ValueError, "Missing file.*market-adaptation"):
                check(root)

    def test_broken_documentation_link_is_rejected(self):
        with self.copied_package() as root:
            with (root / "README.md").open("a", encoding="utf-8") as handle:
                handle.write("\n[Missing file](missing.md)\n")
            with self.assertRaisesRegex(ValueError, "Broken local link"):
                check(root)


if __name__ == "__main__":
    unittest.main()
