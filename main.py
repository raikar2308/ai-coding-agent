"""
main.py

Entry point for the AI Coding Agent.
"""

from explorer import RepositoryExplorer
from analyzer import ProjectAnalyzer
from planner import Planner
from implementer import Implementer
from reporter import Reporter
from utils import (
    Logger,
    Timer,
    validate_repository,
    print_header
)


def main():

    print_header("AI Coding Agent")

    repository_path = input(
        "Enter repository path: "
    ).strip()

    user_request = input(
        "\nEnter user request:\n"
    ).strip()

    try:

        validate_repository(repository_path)

    except Exception as e:

        Logger.error(e)
        return

    timer = Timer()
    timer.start()

    Logger.info("Exploring repository...")

    explorer = RepositoryExplorer(repository_path)

    project_summary = explorer.project_summary()

    Logger.success(
        f"Detected Framework: {project_summary['framework']}"
    )

    Logger.info("Analyzing project...")

    analyzer = ProjectAnalyzer(project_summary)

    analysis = analyzer.analyze()

    Logger.success("Analysis complete.")

    Logger.info("Creating execution plan...")

    planner = Planner(
        analyzer,
        user_request
    )

    planner_result = planner.generate()

    planner.display(planner_result)

    Logger.info("Implementing changes...")

    implementer = Implementer(
        repository_path,
        planner_result
    )

    implementer.implement()

    implementer.print_summary()

    result = implementer.get_result()

    Logger.info("Generating report...")

    reporter = Reporter(repository_path)

    reporter.print_report(
        result["execution_plan"],
        result["changed_files"],
        result["failed_files"]
    )

    report = reporter.save_report(
        result["execution_plan"],
        result["changed_files"],
        result["failed_files"]
    )

    timer.stop()

    Logger.success(
        f"Finished in {timer.elapsed()} seconds."
    )

    Logger.success(
        f"Report saved to:\n{report}"
    )


if __name__ == "__main__":
    main()