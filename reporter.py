"""
reporter.py

Generates the final implementation report.
"""

from pathlib import Path
from datetime import datetime

from llm import LLMClient
from prompts import Prompts


class Reporter:
    """
    Generates implementation reports.
    """

    def __init__(self, repository_path: str):

        self.repository_path = Path(repository_path)

        self.llm = LLMClient()

    def generate_summary(
        self,
        execution_plan: str,
        changed_files: list
    ):
        """
        Generate AI summary.
        """

        prompt = Prompts.summary_prompt(
            execution_plan,
            changed_files
        )

        summary = self.llm.ask_summary(prompt)

        return summary

    def save_report(
        self,
        execution_plan: str,
        changed_files: list,
        failed_files: list
    ):
        """
        Save implementation report.
        """

        summary = self.generate_summary(
            execution_plan,
            changed_files
        )

        report_path = self.repository_path / "implementation_report.md"

        with open(report_path, "w", encoding="utf-8") as f:

            f.write("# AI Coding Agent Report\n\n")

            f.write(
                f"Generated: {datetime.now()}\n\n"
            )

            f.write("---\n\n")

            f.write("## Execution Plan\n\n")

            f.write(execution_plan)

            f.write("\n\n---\n\n")

            f.write("## Changed Files\n\n")

            if changed_files:

                for file in changed_files:
                    f.write(f"- {file}\n")

            else:

                f.write("No files modified.\n")

            f.write("\n\n---\n\n")

            f.write("## Failed Files\n\n")

            if failed_files:

                for file in failed_files:
                    f.write(f"- {file}\n")

            else:

                f.write("None\n")

            f.write("\n\n---\n\n")

            f.write("## AI Summary\n\n")

            f.write(summary)

        return report_path

    def print_report(
        self,
        execution_plan,
        changed_files,
        failed_files
    ):

        print("\n")

        print("=" * 60)
        print("IMPLEMENTATION REPORT")
        print("=" * 60)

        print("\nExecution Plan\n")

        print(execution_plan)

        print("\n")

        print("=" * 60)

        print("Modified Files")

        print("=" * 60)

        if changed_files:

            for file in changed_files:
                print(f"✓ {file}")

        else:

            print("No modified files")

        print("\n")

        print("=" * 60)

        print("Failed Files")

        print("=" * 60)

        if failed_files:

            for file in failed_files:
                print(f"✗ {file}")

        else:

            print("None")

        print("\n")

        summary = self.generate_summary(
            execution_plan,
            changed_files
        )

        print("=" * 60)

        print("SUMMARY")

        print("=" * 60)

        print(summary)

        print("\n")