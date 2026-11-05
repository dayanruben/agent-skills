"""Exercise packaging failures that could hide an incomplete or nonportable skill."""

from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import validate_repository


class SkillValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills" / "example-skill"
        self.skill.mkdir(parents=True)
        self.manifest = self.skill / "SKILL.md"
        self.manifest.write_text(
            "---\nname: example-skill\ndescription: Review example inputs.\n---\n\n# Instructions\nRead inputs.\n",
            encoding="utf-8",
        )
        (self.root / "README.md").write_text("[Skill](skills/example-skill/SKILL.md)\n", encoding="utf-8")

    def assert_invalid(self, expected):
        _, errors = validate_repository(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_package(self):
        self.assertEqual(validate_repository(self.root), (1, []))

    def test_directory_manifest_mismatch(self):
        self.manifest.write_text(self.manifest.read_text().replace("name: example-skill", "name: different"))
        self.assert_invalid("must match")

    def test_duplicate_yaml_keys(self):
        self.manifest.write_text(self.manifest.read_text().replace("description:", "name: override\ndescription:"))
        self.assert_invalid("duplicate YAML key")

    def test_unsafe_yaml_tag(self):
        self.manifest.write_text("---\nname: example-skill\ndescription: !!python/object:builtins.object {}\n---\nRead.\n")
        self.assert_invalid("could not determine a constructor")

    def test_empty_description(self):
        self.manifest.write_text(self.manifest.read_text().replace("Review example inputs.", "''"))
        self.assert_invalid("description must be")

    def test_missing_relative_reference(self):
        self.manifest.write_text(self.manifest.read_text() + "\n[Guide](references/missing.md)\n")
        self.assert_invalid("missing link target")

    def test_reference_escape(self):
        self.manifest.write_text(self.manifest.read_text() + "\n[Private](../../README.md)\n")
        self.assert_invalid("escapes package boundary")

    def test_symlink_resource_rejected(self):
        (self.skill / "outside.md").symlink_to(self.root / "README.md")
        self.assert_invalid("symlinks")

    def test_symlink_skills_root_rejected(self):
        (self.root / "skills").rename(self.root / "elsewhere")
        (self.root / "skills").symlink_to(self.root / "elsewhere", target_is_directory=True)
        self.assert_invalid("skills directory must not be a symlink")

    def test_external_url_does_not_require_network(self):
        self.manifest.write_text(self.manifest.read_text() + "\n[Docs](https://example.invalid/unavailable)\n")
        self.assertEqual(validate_repository(self.root), (1, []))

    def test_installed_dependency_docs_are_outside_repository_link_checks(self):
        dependency = self.root / "node_modules" / "example"
        dependency.mkdir(parents=True)
        (dependency / "README.md").write_text("[Unshipped source](missing.md)\n")
        self.assertEqual(validate_repository(self.root), (1, []))

    def test_catalog_entry_required(self):
        (self.root / "README.md").write_text("# Catalog\n")
        self.assert_invalid("missing catalog entry")

    def test_ui_prompt_uses_actual_skill(self):
        (self.skill / "agents").mkdir()
        (self.skill / "agents" / "openai.yaml").write_text('interface:\n  default_prompt: "Use $another-skill."\n')
        self.assert_invalid("must mention the skill invocation")

    def test_selected_skill_does_not_require_external_catalog_changes(self):
        (self.root / "README.md").unlink()
        self.assertEqual(validate_repository(self.root, "example-skill"), (1, []))


if __name__ == "__main__":
    unittest.main()
