"""
- Use via python build/release.py

Triggers a full release:
- Bumps patch version in pyproject.toml
- Builds the project using PyInstaller
- Commits the version change
- Tags the commit
- Pushes to origin (including tag)

This automatically triggers the GitHub Actions build + upload.
"""

import re
import subprocess
from pathlib import Path

from build.version import bump_patch_version


def get_new_version(pyproject: Path) -> str:
    """
    Extracts the version string from pyproject.toml.
    """
    content = pyproject.read_text(encoding="utf-8")
    version_line = re.search(r'version\s*=\s*"([\d.]+)"', content)
    if not version_line:
        raise ValueError("Could not find version in pyproject.toml")
    return version_line.group(1)


def main() -> None:
    """
    Bumps the version, builds the app, commits and tags the release, and pushes to GitHub.
    """
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        raise FileNotFoundError("pyproject.toml not found")

    # Step 1: Bump patch version
    version = bump_patch_version()
    print(f"🔢 Bumped to version v{version}")

    # Step 2: Build
    subprocess.run(["python", "build/build.py"], check=True)

    # Step 3: Git commit + tag
    tag = f"v{version}"
    subprocess.run(["git", "add", "pyproject.toml"], check=True)
    subprocess.run(["git", "commit", "-m", f"🔖 Release {tag}"], check=True)
    subprocess.run(["git", "tag", tag], check=True)
    subprocess.run(["git", "push"], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)

    print(f"\n✅ Release {tag} pushed. GitHub Actions will now build and publish.\n")


if __name__ == "__main__":
    main()
