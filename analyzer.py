"""
analyzer.py

Analyzes a repository and creates a compact project summary
that can be sent to the LLM.
"""

from pathlib import Path
from collections import defaultdict


class ProjectAnalyzer:
    """
    Analyze repository structure and identify important files.
    """

    MODEL_KEYWORDS = [
        "model",
        "models",
        "entity",
        "schema",
        "table",
    ]

    ROUTE_KEYWORDS = [
        "route",
        "routes",
        "controller",
        "views",
        "api",
        "endpoint",
    ]

    TEMPLATE_KEYWORDS = [
        "template",
        "templates",
        "html",
        "jinja",
    ]

    DATABASE_KEYWORDS = [
        "sqlite",
        "mysql",
        "postgres",
        "database",
        "db",
        "sqlalchemy",
    ]

    NOTE_KEYWORDS = [
        "note",
        "notes",
        "notebook",
        "memo",
    ]

    def __init__(self, project_summary: dict):
        self.project = project_summary
        self.files = project_summary.get("files", [])

    def analyze(self):
        """
        Main analysis entry point.
        """

        report = {
            "framework": self.project.get("framework"),
            "statistics": self._statistics(),
            "important_files": self._important_files(),
            "notes_related": self._notes_related(),
            "database": self._database_files(),
            "entry_points": self._entry_points(),
            "project_description": self._project_description(),
        }

        return report

    def _statistics(self):

        extension_count = defaultdict(int)

        total_lines = 0

        for file in self.files:

            extension_count[file["extension"]] += 1

            total_lines += file["content"].count("\n") + 1

        return {
            "total_files": len(self.files),
            "total_lines": total_lines,
            "extensions": dict(extension_count),
        }

    def _important_files(self):

        important = {
            "models": [],
            "routes": [],
            "templates": [],
            "configuration": [],
        }

        for file in self.files:

            path = file["relative_path"].lower()

            if any(word in path for word in self.MODEL_KEYWORDS):
                important["models"].append(file["relative_path"])

            if any(word in path for word in self.ROUTE_KEYWORDS):
                important["routes"].append(file["relative_path"])

            if any(word in path for word in self.TEMPLATE_KEYWORDS):
                important["templates"].append(file["relative_path"])

            if (
                "config" in path
                or ".env" in path
                or "settings" in path
            ):
                important["configuration"].append(file["relative_path"])

        return important

    def _database_files(self):

        database = []

        for file in self.files:

            path = file["relative_path"].lower()
            content = file["content"].lower()

            if any(word in path for word in self.DATABASE_KEYWORDS):
                database.append(file["relative_path"])
                continue

            if any(word in content for word in self.DATABASE_KEYWORDS):
                database.append(file["relative_path"])

        return database

    def _notes_related(self):

        note_files = []

        for file in self.files:

            path = file["relative_path"].lower()
            content = file["content"].lower()

            if any(word in path for word in self.NOTE_KEYWORDS):
                note_files.append(file["relative_path"])
                continue

            if any(word in content for word in self.NOTE_KEYWORDS):
                note_files.append(file["relative_path"])

        return note_files

    def _entry_points(self):

        entry = []

        candidates = [
            "app.py",
            "main.py",
            "manage.py",
            "server.py",
            "index.js",
            "index.ts",
        ]

        for file in self.files:

            name = Path(file["relative_path"]).name.lower()

            if name in candidates:
                entry.append(file["relative_path"])

        return entry

    def _project_description(self):

        description = []

        description.append(
            f"Framework: {self.project.get('framework')}"
        )

        description.append(
            f"Source files: {len(self.files)}"
        )

        stats = self._statistics()

        description.append(
            f"Total lines: {stats['total_lines']}"
        )

        if self._notes_related():

            description.append(
                "Project appears to contain a notes feature."
            )

        if self._database_files():

            description.append(
                "Database layer detected."
            )

        return " ".join(description)

    def to_prompt(self):

        """
        Compact text sent to the LLM.
        """

        analysis = self.analyze()

        lines = []

        lines.append("# Project Summary")
        lines.append("")

        lines.append(f"Framework: {analysis['framework']}")
        lines.append(
            f"Files: {analysis['statistics']['total_files']}"
        )
        lines.append(
            f"Lines: {analysis['statistics']['total_lines']}"
        )

        lines.append("")
        lines.append("Important Files:")

        for category, files in analysis["important_files"].items():

            if files:

                lines.append(f"- {category}")

                for file in files:
                    lines.append(f"    - {file}")

        if analysis["notes_related"]:

            lines.append("")
            lines.append("Notes Related Files:")

            for file in analysis["notes_related"]:
                lines.append(f"- {file}")

        if analysis["database"]:

            lines.append("")
            lines.append("Database Files:")

            for file in analysis["database"]:
                lines.append(f"- {file}")

        return "\n".join(lines)
