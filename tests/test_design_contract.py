"""Check portable references and the maintained design-to-registry boundary."""

import re
import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/market-brief"


class DesignContractTests(unittest.TestCase):
    def test_local_markdown_links_resolve_within_their_artifact(self):
        files = [ROOT / "README.md", *ROOT.glob("design-docs/*.md"), *SKILL.rglob("*.md")]
        for file in files:
            for link in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                with self.subTest(file=file.relative_to(ROOT), link=link):
                    self.assertTrue((file.parent / link.split("#")[0]).is_file())
                    if file.is_relative_to(SKILL):
                        self.assertTrue((file.parent / link).resolve().is_relative_to(SKILL))

    def test_every_market_and_cadence_reference_is_portable(self):
        with (SKILL / "registry.toml").open("rb") as handle:
            config = tomllib.load(handle)
        for market_id, market in config["markets"].items():
            for reference in [f"{market['asset_type']}.md", f"markets/{market_id}.md",
                              *[f"cadences/{c}.md" for c in market["cadences"]]]:
                with self.subTest(reference=reference):
                    self.assertTrue((SKILL / "references" / reference).is_file())

    def test_design_task_tiers_and_report_ids_match_registry(self):
        with (SKILL / "registry.toml").open("rb") as handle:
            config = tomllib.load(handle)
        design = (ROOT / "design-docs/market-brief-skill-design.md").read_text()
        designed_tiers = dict(re.findall(r"\| `([a-z_]+)` \| [^\n|]+ \| (light|medium|heavy) \|", design))
        implemented_tiers = {task: tier for tier, tasks in config["tiers"].items() for task in tasks}
        self.assertEqual(designed_tiers, implemented_tiers)
        designed_reports = set(re.findall(r"`((?:cn_equity|us_equity|crypto)\.[a-z]+)`", design))
        implemented_reports = {f"{mid}.{c}" for mid, market in config["markets"].items() for c in market["cadences"]}
        self.assertEqual(designed_reports, implemented_reports)


if __name__ == "__main__":
    unittest.main()
