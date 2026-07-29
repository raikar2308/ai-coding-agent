"""
explorer.py

Scans a repository and collects all relevant source files
while respecting .gitignore.
"""

from pathlib import Path
import pathspec

# Directories to ignore
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
    ".pytest_cache",
}

# File extensions to scan
SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".json",
    ".md",
    ".txt",
    ".sql",
    ".yaml",
    ".yml",
}


class RepositoryExplorer:
    """
    Explore a repository and collect useful project files.
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self.gitignore = self._load_gitignore()

    def _load_gitignore(self):
        """
        Load .gitignore rules if present.
        """
        gitignore = self.repo_path / ".gitignore"

        if gitignore.exists():
            with open(gitignore, "r", encoding="utf-8") as f:
                return pathspec.PathSpec.from_lines(
                    "gitwildmatch",
                    f.readlines()
                )

        return None

    def _is_ignored(self, path: Path):
        """
        Check whether a file should be ignored.
        """

        relative = path.relative_to(self.repo_path)

        for part in relative.parts:
            if part in IGNORE_DIRS:
                return True

        if self.gitignore:
            if self.gitignore.match_file(str(relative)):
                return True

        return False

    def collect_files(self):
        """
        Return list of project source files.
        """

        project_files = []

        for file in self.repo_path.rglob("*"):

            if file.is_dir():
                continue

            if self._is_ignored(file):
                continue

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                project_files.append({
                    "path": str(file),
                    "relative_path": str(
                        file.relative_to(self.repo_path)
                    ),
                    "extension": file.suffix,
                    "size": len(content),
                    "content": content
                })

            except Exception as e:

                print(f"Could not read {file}: {e}")

        return project_files

    def detect_framework(self):
        """
        Detect project framework.
        """

        files = {
            f.name.lower()
            for f in self.repo_path.rglob("*")
            if f.is_file()
        }

        framework = "Unknown"

        if "manage.py" in files:
            framework = "Django"

        elif "app.py" in files or "requirements.txt" in files:
            framework = "Flask / Python"

        elif "package.json" in files:

            package = self.repo_path / "package.json"

            if package.exists():

                text = package.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()

                if "react" in text:
                    framework = "React"

                elif "express" in text:
                    framework = "Express"

                elif "next" in text:
                    framework = "Next.js"

        return framework

    def project_summary(self):
        """
        Return repository summary.
        """

        files = self.collect_files()

        summary = {
            "framework": self.detect_framework(),
            "total_files": len(files),
            "files": files
        }

        return summary