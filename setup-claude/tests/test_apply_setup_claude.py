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


if __name__ == "__main__":
    unittest.main()
