#!/usr/bin/env python3
"""Install only into an explicitly chosen workspace; never replace an existing skill."""
import argparse
from pathlib import Path
import shutil
import tempfile


def install(source, workspace):
    source = Path(source).resolve()
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir() or workspace == Path.home() or workspace == Path(workspace.anchor):
        raise ValueError("choose an existing project workspace, not home or filesystem root")
    if source == workspace or source in workspace.parents:
        raise ValueError("workspace must be outside the skill source (avoid recursive copying)")
    if workspace.name in {".codex", ".agents", ".claude", "skills"}:
        raise ValueError("choose the project root, not a global configuration or skills folder")
    # Do not traverse a linked install directory into another project/global configuration.
    for path in (workspace / ".agents", workspace / ".agents/skills"):
        if path.is_symlink():
            raise ValueError("installation parents cannot be symlinks")
    parent = workspace / ".agents/skills"
    target = parent / "film-visual"
    if target.exists() or target.is_symlink():
        raise FileExistsError("film-visual already exists; inspect and merge manually")
    if not (source / "SKILL.md").is_file():
        raise ValueError("source SKILL.md missing")
    if any(p.is_symlink() for p in source.rglob("*")):
        raise ValueError("skill source must be self-contained (no symlinks)")
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".film-visual-", dir=parent) as temp:
        stage = Path(temp) / "film-visual"
        shutil.copytree(source, stage, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        # Reserve destination exclusively; a concurrent install cannot be replaced.
        target.mkdir()
        try:
            for entry in stage.iterdir():
                entry.rename(target / entry.name)
        except OSError:
            # Leave the explicit partial folder for inspection instead of deleting user files.
            raise
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True,
                        help="existing authorized project directory")
    args = parser.parse_args()
    try:
        print(install(Path(__file__).resolve().parents[1], args.workspace))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
