import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


def _load_apply_module():
    skill_root = Path(__file__).resolve().parents[1]
    script_path = skill_root / "scripts" / "apply_setup_claude.py"
    spec = importlib.util.spec_from_file_location("apply_setup_claude", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestApplySetupClaude(unittest.TestCase):
    def test_print_detection_exits_without_writes(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "package.json").write_text(
                json.dumps(
                    {
                        "name": "demo",
                        "description": "Demo repo",
                        "scripts": {"dev": "next dev", "test": "vitest"},
                        "dependencies": {"next": "1.0.0", "react": "1.0.0"},
                        "devDependencies": {"vitest": "1.0.0"},
                    }
                ),
                encoding="utf-8",
            )

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = mod.main(["apply_setup_claude.py", str(repo_root), "--print-detection"])
            self.assertEqual(rc, 0)
            data = json.loads(buf.getvalue().strip())
            self.assertEqual(data["project_name"], "demo")
            self.assertEqual(data["framework"], "Next.js (App Router)")

            self.assertFalse((repo_root / "tasks").exists())
            self.assertFalse((repo_root / ".claude").exists())

    def test_dry_run_does_not_write_files_or_dirs(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "package.json").write_text(json.dumps({"name": "demo"}), encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=True,
                    detection=mod.detect(repo_root),
                )
            self.assertEqual(rc, 0)

            self.assertFalse((repo_root / "tasks").exists())
            self.assertFalse((repo_root / ".claude").exists())

    def test_marker_guarded_updates(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "package.json").write_text(
                json.dumps({"name": "demo", "scripts": {"dev": "node dev"}}),
                encoding="utf-8",
            )
            detection = mod.detect(repo_root)

            # Create an agent-modified file (no marker): should NOT be overwritten.
            no_marker_path = repo_root / ".claude" / "commands" / "status.md"
            no_marker_path.parent.mkdir(parents=True, exist_ok=True)
            no_marker_path.write_text("# custom status\n", encoding="utf-8")

            # Create a generated file with marker but wrong content: should be updated.
            marker_path = repo_root / ".claude" / "commands" / "plan.md"
            marker_path.write_text(f"{mod.GENERATED_MARKER}\n# old\n", encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=True,
                    dry_run=False,
                    detection=detection,
                )
            self.assertEqual(rc, 0)

            self.assertEqual(no_marker_path.read_text(encoding="utf-8"), "# custom status\n")

            tpl = (skill_root / "templates" / "commands" / "plan.md.template").read_text(encoding="utf-8")
            expected = mod.render_template(tpl, detection)
            self.assertEqual(marker_path.read_text(encoding="utf-8"), expected)

    def test_workflow_status_created_on_fresh_setup(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "package.json").write_text(json.dumps({"name": "demo"}), encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=mod.detect(repo_root),
                )
            self.assertEqual(rc, 0)

            # workflow-status.md should NOT be created (removed from workflow)
            wf_path = repo_root / "tasks" / "workflow-status.md"
            self.assertFalse(wf_path.exists())

    def test_existing_custom_claude_md_writes_sidecar(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "package.json").write_text(json.dumps({"name": "demo"}), encoding="utf-8")
            (repo_root / "CLAUDE.md").write_text("# Custom\n", encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=mod.detect(repo_root),
                )
            self.assertEqual(rc, 0)

            self.assertEqual((repo_root / "CLAUDE.md").read_text(encoding="utf-8"), "# Custom\n")
            self.assertTrue((repo_root / "CLAUDE.setup-claude.md").exists())
            self.assertIn("Notes:", buf.getvalue())


    def test_laravel_detection_inertia_react(self):
        mod = _load_apply_module()

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "composer.json").write_text(
                json.dumps({
                    "require": {"laravel/framework": "^12.0"},
                    "require-dev": {
                        "pestphp/pest": "^3.0",
                        "inertiajs/inertia-laravel": "^2.0",
                    },
                }),
                encoding="utf-8",
            )
            (repo_root / "package.json").write_text(
                json.dumps({"dependencies": {"react": "^19.0"}}),
                encoding="utf-8",
            )
            (repo_root / "database" / "migrations").mkdir(parents=True)

            detection = mod.detect(repo_root)
            self.assertEqual(detection.framework, "Laravel (Inertia + React)")
            self.assertEqual(detection.language, "PHP")
            self.assertEqual(detection.database, "Eloquent ORM")
            self.assertEqual(detection.testing, "Pest")
            self.assertEqual(detection.dev_cmd, "php artisan serve")
            self.assertEqual(detection.lint_cmd, "vendor/bin/pint")
            self.assertEqual(detection.test_cmd, "vendor/bin/pest")

    def test_laravel_detection_livewire(self):
        mod = _load_apply_module()

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "composer.json").write_text(
                json.dumps({
                    "require": {
                        "laravel/framework": "^12.0",
                        "livewire/livewire": "^3.0",
                    },
                }),
                encoding="utf-8",
            )

            detection = mod.detect(repo_root)
            self.assertEqual(detection.framework, "Laravel (Livewire)")

    def test_laravel_detection_api_only(self):
        mod = _load_apply_module()

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "composer.json").write_text(
                json.dumps({"require": {"laravel/framework": "^12.0"}}),
                encoding="utf-8",
            )

            detection = mod.detect(repo_root)
            self.assertEqual(detection.framework, "Laravel (API)")

    def test_mcp_json_created_for_laravel(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "composer.json").write_text(
                json.dumps({"require": {"laravel/framework": "^12.0"}}),
                encoding="utf-8",
            )

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=mod.detect(repo_root),
                )

            mcp_path = repo_root / ".mcp.json"
            self.assertTrue(mcp_path.exists())
            mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
            self.assertIn("laravel-boost", mcp_data["mcpServers"])
            self.assertEqual(mcp_data["mcpServers"]["laravel-boost"]["command"], "php")

    def test_mcp_json_not_created_for_nextjs(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "package.json").write_text(
                json.dumps({
                    "name": "demo",
                    "dependencies": {"next": "15.0.0", "react": "19.0.0"},
                }),
                encoding="utf-8",
            )

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=mod.detect(repo_root),
                )

            mcp_path = repo_root / ".mcp.json"
            if mcp_path.exists():
                mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
                self.assertNotIn("laravel-boost", mcp_data.get("mcpServers", {}))

    def test_mcp_json_removed_when_stack_changes(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            # Start with Laravel — creates .mcp.json with laravel-boost
            (repo_root / "composer.json").write_text(
                json.dumps({"require": {"laravel/framework": "^12.0"}}),
                encoding="utf-8",
            )
            laravel_detection = mod.detect(repo_root)

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=laravel_detection,
                )

            mcp_path = repo_root / ".mcp.json"
            self.assertTrue(mcp_path.exists())
            mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
            self.assertIn("laravel-boost", mcp_data["mcpServers"])

            # Switch to Next.js — laravel-boost should be removed
            (repo_root / "composer.json").unlink()
            (repo_root / "package.json").write_text(
                json.dumps({
                    "name": "demo",
                    "dependencies": {"next": "15.0.0", "react": "19.0.0"},
                }),
                encoding="utf-8",
            )
            nextjs_detection = mod.detect(repo_root)

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=nextjs_detection,
                )

            mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
            self.assertNotIn("laravel-boost", mcp_data.get("mcpServers", {}))

    def test_mcp_json_sail_detection(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "composer.json").write_text(
                json.dumps({"require": {"laravel/framework": "^12.0"}}),
                encoding="utf-8",
            )
            # Simulate Sail being present
            (repo_root / "vendor" / "bin").mkdir(parents=True)
            (repo_root / "vendor" / "bin" / "sail").write_text("#!/bin/sh\n", encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=mod.detect(repo_root),
                )

            mcp_path = repo_root / ".mcp.json"
            mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
            self.assertEqual(
                mcp_data["mcpServers"]["laravel-boost"]["command"],
                "vendor/bin/sail",
            )

    def test_mcp_json_preserves_user_entries(self):
        mod = _load_apply_module()
        skill_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "composer.json").write_text(
                json.dumps({"require": {"laravel/framework": "^12.0"}}),
                encoding="utf-8",
            )

            # Pre-existing user MCP entry
            (repo_root / ".mcp.json").write_text(
                json.dumps({
                    "mcpServers": {
                        "my-custom-server": {"command": "node", "args": ["server.js"]},
                    },
                }),
                encoding="utf-8",
            )

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.apply(
                    repo_root,
                    skill_root,
                    update_generated=False,
                    dry_run=False,
                    detection=mod.detect(repo_root),
                )

            mcp_data = json.loads((repo_root / ".mcp.json").read_text(encoding="utf-8"))
            self.assertIn("my-custom-server", mcp_data["mcpServers"])
            self.assertIn("laravel-boost", mcp_data["mcpServers"])

    def test_laravel_rules_filter(self):
        mod = _load_apply_module()

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "composer.json").write_text(
                json.dumps({"require": {"laravel/framework": "^12.0"}}),
                encoding="utf-8",
            )
            detection = mod.detect(repo_root)
            rule_filter = mod._rules_filter(detection)
            self.assertTrue(rule_filter("laravel.md.template"))
            self.assertTrue(rule_filter("tests.md.template"))

    def test_nextjs_rules_filter_excludes_laravel(self):
        mod = _load_apply_module()

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / "package.json").write_text(
                json.dumps({
                    "dependencies": {"next": "15.0.0", "react": "19.0.0"},
                }),
                encoding="utf-8",
            )
            detection = mod.detect(repo_root)
            rule_filter = mod._rules_filter(detection)
            self.assertFalse(rule_filter("laravel.md.template"))
            self.assertTrue(rule_filter("react.md.template"))


if __name__ == "__main__":
    unittest.main()
