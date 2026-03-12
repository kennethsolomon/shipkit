"""Auto-detection logic for project configuration."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ProjectConfig:
    """Detected project configuration."""

    language: str = "Unknown"
    framework: str = "None"
    database: str = "None"
    ui: str = "None"
    testing: str = "None"
    description: str = ""
    dev_command: str = ""
    build_command: str = ""
    test_command: str = ""
    lint_command: str = ""
    project_name: str = ""
    project_dir: str = ""


def detect_project(root_path: Path) -> ProjectConfig:
    """Auto-detect project configuration from files.

    Args:
        root_path: Root directory of the project

    Returns:
        ProjectConfig with detected values
    """
    config = ProjectConfig()
    config.project_dir = root_path.name
    config.project_name = root_path.name

    # Check package.json (Node.js)
    package_json = root_path / "package.json"
    if package_json.exists():
        return _detect_nodejs(root_path, config)

    # Check pyproject.toml or setup.py (Python)
    if (root_path / "pyproject.toml").exists() or (root_path / "setup.py").exists():
        return _detect_python(root_path, config)

    # Check go.mod (Go)
    if (root_path / "go.mod").exists():
        return _detect_go(root_path, config)

    # Check Cargo.toml (Rust)
    if (root_path / "Cargo.toml").exists():
        return _detect_rust(root_path, config)

    # Default: Generic project
    config.language = "JavaScript/TypeScript"
    config.dev_command = "npm run dev"
    config.build_command = "npm run build"
    config.test_command = "npm test"
    config.lint_command = "npm run lint"

    return config


def _detect_nodejs(root_path: Path, config: ProjectConfig) -> ProjectConfig:
    """Detect Node.js/JavaScript project details."""
    config.language = "JavaScript/TypeScript"

    try:
        with open(root_path / "package.json") as f:
            pkg = json.load(f)

        # Extract project info
        config.project_name = pkg.get("name", config.project_name)
        config.description = pkg.get("description", "")

        # Detect framework
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

        if "react" in deps or "next" in deps:
            config.framework = "React" if "react" in deps else "Next.js"
            config.ui = "React"
        elif "vue" in deps or "nuxt" in deps:
            config.framework = "Vue" if "vue" in deps else "Nuxt"
            config.ui = "Vue"
        elif "angular" in deps:
            config.framework = "Angular"
            config.ui = "Angular"
        elif "svelte" in deps:
            config.framework = "Svelte"
            config.ui = "Svelte"

        # Detect UI framework
        if "tailwindcss" in deps:
            config.ui = "Tailwind CSS"
        elif "styled-components" in deps:
            config.ui = "styled-components"
        elif "sass" in deps or "node-sass" in deps:
            config.ui = "Sass"

        # Detect database
        if "prisma" in deps:
            config.database = "Prisma"
        elif "drizzle-orm" in deps:
            config.database = "Drizzle"
        elif "mongoose" in deps:
            config.database = "MongoDB (Mongoose)"
        elif "sequelize" in deps:
            config.database = "PostgreSQL (Sequelize)"
        elif "typeorm" in deps:
            config.database = "TypeORM"

        # Detect testing
        if "vitest" in deps:
            config.testing = "Vitest"
        elif "jest" in deps:
            config.testing = "Jest"
        elif "mocha" in deps:
            config.testing = "Mocha"

        # Extract commands from package.json scripts
        scripts = pkg.get("scripts", {})
        config.dev_command = f"npm run {_find_script(scripts, ['dev', 'start'])}" if _find_script(scripts, ['dev', 'start']) else "npm run dev"
        config.build_command = f"npm run {_find_script(scripts, ['build'])}" if _find_script(scripts, ['build']) else "npm run build"
        config.test_command = f"npm test"
        config.lint_command = f"npm run {_find_script(scripts, ['lint'])}" if _find_script(scripts, ['lint']) else "npm run lint"

    except Exception as e:
        print(f"Warning: Could not fully parse package.json: {e}")

    return config


def _detect_python(root_path: Path, config: ProjectConfig) -> ProjectConfig:
    """Detect Python project details."""
    config.language = "Python"

    # Try pyproject.toml first
    pyproject = root_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text()

            # Simple detection without external dependency
            if "django" in content:
                config.framework = "Django"
            elif "fastapi" in content:
                config.framework = "FastAPI"
            elif "flask" in content:
                config.framework = "Flask"
            elif "starlette" in content:
                config.framework = "Starlette"

            if "sqlalchemy" in content or "alembic" in content:
                config.database = "SQLAlchemy"
            elif "django" in content:
                config.database = "Django ORM"

            if "pytest" in content:
                config.testing = "pytest"
        except Exception as e:
            print(f"Warning: Could not parse pyproject.toml: {e}")

    # Default Python commands
    config.dev_command = "python -m uvicorn main:app --reload"
    config.build_command = "pip install -e ."
    config.test_command = "pytest"
    config.lint_command = "pylint ."
    config.description = "Python project"

    return config


def _detect_go(root_path: Path, config: ProjectConfig) -> ProjectConfig:
    """Detect Go project details."""
    config.language = "Go"
    config.dev_command = "go run ."
    config.build_command = "go build -o bin/app ."
    config.test_command = "go test ./..."
    config.lint_command = "golangci-lint run"
    config.description = "Go project"

    return config


def _detect_rust(root_path: Path, config: ProjectConfig) -> ProjectConfig:
    """Detect Rust project details."""
    config.language = "Rust"
    config.dev_command = "cargo run"
    config.build_command = "cargo build --release"
    config.test_command = "cargo test"
    config.lint_command = "cargo clippy"
    config.description = "Rust project"

    return config


def _find_script(scripts: dict, candidates: list) -> Optional[str]:
    """Find first matching script from candidates."""
    for candidate in candidates:
        if candidate in scripts:
            return candidate
    return None
