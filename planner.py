"""
planner.py

Uses the LLM to create an execution plan and identify
the files that need to be modified.
"""

from llm import LLMClient
from prompts import Prompts


class Planner:
    """
    Creates an implementation plan for the requested feature.
    """

    def __init__(self, analyzer, user_request: str):
        """
        Parameters
        ----------
        analyzer : ProjectAnalyzer
            Analyzer object.

        user_request : str
            User's feature request.
        """

        self.analyzer = analyzer
        self.user_request = user_request

        self.llm = LLMClient()

    def create_plan(self):
        """
        Generate execution plan using LLM.
        """

        project_summary = self.analyzer.to_prompt()

        prompt = Prompts.planning_prompt(
            project_summary=project_summary,
            user_request=self.user_request
        )

        print("\nGenerating execution plan...\n")

        plan = self.llm.ask(prompt)

        return plan

    def select_files(self):
        """
        Ask LLM which files should be modified.
        """

        project_summary = self.analyzer.to_prompt()

        prompt = Prompts.file_selection_prompt(
            project_summary=project_summary,
            user_request=self.user_request
        )

        print("Finding relevant files...\n")

        response = self.llm.ask(prompt)

        files = []

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("-"):
                line = line[1:].strip()

            files.append(line)

        return files

    def generate(self):
        """
        Generate complete planning result.
        """

        plan = self.create_plan()

        files = self.select_files()

        result = {
            "request": self.user_request,
            "plan": plan,
            "files": files
        }

        return result

    def display(self, result):
        """
        Print execution plan.
        """

        print("=" * 60)
        print("EXECUTION PLAN")
        print("=" * 60)

        print(result["plan"])

        print("\n")

        print("=" * 60)
        print("FILES TO MODIFY")
        print("=" * 60)

        if not result["files"]:
            print("No files identified.")

        else:

            for file in result["files"]:
                print(f"- {file}")

        print("=" * 60)