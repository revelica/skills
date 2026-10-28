"""Public upload contracts; no backend or external services required."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PackageOpenAITest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "plugins/revelica"
        shutil.copytree(ROOT / "plugins/revelica", self.source)
        (self.root / "scripts").mkdir()
        shutil.copyfile(ROOT / "scripts/package-openai.py", self.root / "scripts/package-openai.py")
        self.manifest_path = self.source / ".codex-plugin/plugin.json"
        self.manifest = json.loads(self.manifest_path.read_text())

    def build(self, output, success=True):
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/package-openai.py"), "--output", str(output)],
            capture_output=True, text=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_portable_upload_preserves_review_listing_skills_and_endpoint(self):
        output = self.root / "upload.zip"
        (self.source / "skills/.DS_Store").write_bytes(b"not part of the plugin")
        self.build(output)
        with zipfile.ZipFile(output) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(set(archive.namelist()), {
                "revelica/plugin.json", "revelica/mcp.json",
                "revelica/assets/revelica-icon-512.png",
                "revelica/assets/revelica-icon-1024.png",
                "revelica/assets/revelica-logo.svg",
                "revelica/skills/drive-product-outcome/SKILL.md",
                "revelica/skills/ingestion/SKILL.md",
                "revelica/skills/interview-snapshot/SKILL.md",
                "revelica/skills/setup-revelica/SKILL.md",
            })
            exported = json.loads(archive.read("revelica/plugin.json"))
            self.assertEqual(exported["version"], self.manifest["version"])
            self.assertEqual(exported["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
            for incompatible in ("interface", "skills", "mcpServers", "apps"):
                self.assertNotIn(incompatible, exported)
            openai = exported["extensions"]["com.openai"]
            self.assertEqual(openai["interface"], self.manifest["interface"])
            for key in ("review", "publication", "onboardingSkill"):
                self.assertEqual(openai[key], self.manifest["extensions"]["com.openai"][key])
            original_servers = json.loads((self.source / ".mcp.json").read_text())["mcpServers"]
            servers = json.loads(archive.read("revelica/mcp.json"))["mcpServers"]
            self.assertEqual(set(servers), set(original_servers))
            for name, server in servers.items():
                self.assertEqual(server["type"], "streamable-http")
                self.assertEqual(server["url"], original_servers[name]["url"])
                self.assertEqual({k: v for k, v in server.items() if k != "type"},
                                 {k: v for k, v in original_servers[name].items() if k != "type"})
            for skill in (self.source / "skills").glob("*/SKILL.md"):
                self.assertEqual(archive.read("revelica/" + skill.relative_to(self.source).as_posix()),
                                 skill.read_bytes())

    def test_build_is_byte_reproducible(self):
        first, second = self.root / "first.zip", self.root / "second.zip"
        self.build(first)
        self.build(second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertTrue(all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist()))

    def test_existing_archive_is_never_overwritten(self):
        output = self.root / "dist" / f"revelica-openai-{self.manifest['version']}.zip"
        output.parent.mkdir()
        output.write_bytes(b"preserve the exact submitted artifact")
        result = self.build(output, success=False)
        self.assertIn("Refusing to overwrite", result.stderr)
        self.assertEqual(output.read_bytes(), b"preserve the exact submitted artifact")

    def test_private_app_bindings_are_rejected(self):
        output = self.root / "upload.zip"
        binding = self.source / ".app.json"
        binding.write_text('{"apps": {"private": {"id": "private-id"}}}')
        self.assertIn(".app.json", self.build(output, success=False).stderr)
        self.assertFalse(output.exists())
        binding.unlink()
        for path in ("root", "openai"):
            with self.subTest(path=path):
                manifest = json.loads(json.dumps(self.manifest))
                target = manifest if path == "root" else manifest["extensions"]["com.openai"]
                target["apps"] = "./private.json"
                self.manifest_path.write_text(json.dumps(manifest))
                self.assertIn("cannot declare", self.build(output, success=False).stderr)
                self.assertFalse(output.exists())

    def test_incomplete_review_cases_are_rejected(self):
        self.manifest["extensions"]["com.openai"]["review"]["test_cases"]["positive"].pop()
        self.manifest_path.write_text(json.dumps(self.manifest))
        output = self.root / "upload.zip"
        self.assertIn("at least 5 positive", self.build(output, success=False).stderr)
        self.assertFalse(output.exists())


class SourceVersionTest(unittest.TestCase):
    def test_host_manifests_and_marketplace_use_the_same_version(self):
        plugin = ROOT / "plugins/revelica"
        codex = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
        claude = json.loads((plugin / ".claude-plugin/plugin.json").read_text())
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(codex["version"], claude["version"])
        self.assertEqual(codex["version"], marketplace["plugins"][0]["version"])
        registry = json.loads((ROOT / "server.json").read_text())
        self.assertEqual(codex["version"], registry["version"])


if __name__ == "__main__":
    unittest.main()
