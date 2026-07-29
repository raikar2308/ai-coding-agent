"""
prompts.py

Contains all prompts used by the AI Coding Agent.
"""


class Prompts:
    """
    Collection of prompts for different stages of the agent.
    """

    @staticmethod
    def planning_prompt(project_summary: str, user_request: str) -> str:
        return f"""
You are a Senior Software Engineer and AI Coding Agent.

Your task is to understand an existing software project and decide how to
implement the requested feature.

=========================
PROJECT SUMMARY
=========================

{project_summary}

=========================
USER REQUEST
=========================

{user_request}

=========================
YOUR TASK
=========================

1. Understand the application.
2. Decide the best feature to implement.
3. Preserve existing functionality.
4. Modify the smallest number of files possible.
5. Explain your reasoning.

Return ONLY the following format:

Execution Plan

Feature:
Reason:

Files To Modify:
- file1
- file2

Implementation Steps:
1.
2.
3.

Testing:
- Test 1
- Test 2
"""

    @staticmethod
    def implementation_prompt(
        file_path: str,
        file_content: str,
        execution_plan: str
    ) -> str:
        return f"""
You are an expert software engineer.

Execution Plan

{execution_plan}

=====================
CURRENT FILE
=====================

File:

{file_path}

=====================
CODE
=====================

{file_content}

=====================
TASK
=====================

Modify ONLY this file if necessary.

Rules:

- Preserve formatting.
- Preserve comments.
- Do not remove existing functionality.
- Only implement the required feature.
- If no changes are required,
  return the original code unchanged.

Return ONLY valid source code.
"""

    @staticmethod
    def patch_prompt(
        file_path: str,
        file_content: str,
        execution_plan: str
    ) -> str:
        return f"""
You are an expert software engineer.

Execution Plan

{execution_plan}

Current File

{file_path}

Code

{file_content}

Generate ONLY a unified diff patch.

Requirements

- Modify only necessary lines.
- Do not rewrite the whole file.
- Preserve formatting.
- Output ONLY a unified diff.
"""

    @staticmethod
    def summary_prompt(
        execution_plan: str,
        changed_files: list
    ) -> str:

        file_list = "\n".join(changed_files)

        return f"""
You implemented the following execution plan.

{execution_plan}

Changed Files

{file_list}

Write a concise implementation summary.

Include

- Feature implemented
- Files modified
- Why they were modified
- Existing functionality preserved

Keep it under 250 words.
"""

    @staticmethod
    def framework_detection_prompt(project_summary: str) -> str:
        return f"""
You are an expert software architect.

Repository Summary

{project_summary}

Determine

1. Framework
2. Backend language
3. Frontend framework
4. Database
5. Architecture

Return only a short summary.
"""

    @staticmethod
    def file_selection_prompt(
        project_summary: str,
        user_request: str
    ) -> str:
        return f"""
You are an AI Coding Agent.

Repository

{project_summary}

User Request

{user_request}

Identify ONLY the files that need modification.

Return one file path per line.

Do not explain.
"""

    @staticmethod
    def validation_prompt(
        code: str,
        file_path: str
    ) -> str:
        return f"""
You are a senior software engineer.

Validate the following source code.

File

{file_path}

Code

{code}

Check for

- Syntax errors
- Missing imports
- Obvious bugs
- Invalid formatting

If everything is correct return

VALID

Otherwise explain the problem.
"""

    @staticmethod
    def bug_fix_prompt(
        code: str,
        error_message: str
    ) -> str:
        return f"""
You generated code with an error.

Error

{error_message}

Code

{code}

Fix ONLY the error.

Return ONLY corrected source code.
"""