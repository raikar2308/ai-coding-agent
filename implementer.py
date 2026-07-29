"""
implementer.py

Generates and applies code changes using the LLM.
"""

from pathlib import Path

from llm import LLMClient
from prompts import Prompts
from patcher import PatchApplier


class Implementer:
    """
    Implements the execution plan by generating and applying patches.
    """

    def __init__(self, repository_path: str, planner_result: dict):
        self.repository_path = Path(repository_path)

        self.execution_plan = planner_result["plan"]
        self.target_files = planner_result["files"]

        self.llm = LLMClient()
        self.patcher = PatchApplier(repository_path)

        self.changed_files = []
        self.failed_files = []

    def _read_file(self, relative_path: str):
        """
        Read a project file.
        """

        file_path = self.repository_path / relative_path

        if not file_path.exists():
            print(f"[ERROR] File not found: {relative_path}")
            return None

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    def _generate_patch(
        self,
        file_path: str,
        file_content: str
    ):
        """
        Ask the LLM to generate a unified diff patch.
        """

        prompt = Prompts.patch_prompt(
            file_path=file_path,
            file_content=file_content,
            execution_plan=self.execution_plan
        )

        patch = self.llm.ask_patch(prompt)

        return patch

    def implement(self):
        """
        Generate and apply patches.
        """

        print("\n==============================")
        print("IMPLEMENTATION STARTED")
        print("==============================\n")

        if not self.target_files:
            print("No files selected for modification.")
            return

        for relative_path in self.target_files:

            print(f"Processing: {relative_path}")

            file_content = self._read_file(relative_path)

            if file_content is None:
                self.failed_files.append(relative_path)
                continue

            try:

                patch = self._generate_patch(
                    relative_path,
                    file_content
                )

                if not patch.strip():
                    print("No patch generated.\n")
                    continue

                success = self.patcher.apply_patch(patch)

                if success:

                    print("✓ Patch applied\n")
                    self.changed_files.append(relative_path)

                else:

                    print("✗ Patch failed\n")
                    self.failed_files.append(relative_path)

            except Exception as e:

                print(f"Error: {e}\n")
                self.failed_files.append(relative_path)

        print("==============================")
        print("IMPLEMENTATION COMPLETE")
        print("==============================")

    def get_result(self):
        """
        Return implementation result.
        """

        return {
            "execution_plan": self.execution_plan,
            "changed_files": self.changed_files,
            "failed_files": self.failed_files
        }

    def print_summary(self):
        """
        Print implementation summary.
        """

        print("\n========== SUMMARY ==========\n")

        print(f"Files Modified : {len(self.changed_files)}")
        print(f"Files Failed   : {len(self.failed_files)}")

        if self.changed_files:

            print("\nModified Files")

            for file in self.changed_files:
                print(f"  ✓ {file}")

        if self.failed_files:

            print("\nFailed Files")

            for file in self.failed_files:
                print(f"  ✗ {file}")

        print("\n=============================\n")