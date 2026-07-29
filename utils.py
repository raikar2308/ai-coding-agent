"""
utils.py

Common utility functions for the AI Coding Agent.
"""

import json
import time
from pathlib import Path
from datetime import datetime


class Timer:
    """
    Simple execution timer.
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def elapsed(self):
        if self.start_time is None:
            return 0

        end = self.end_time or time.time()

        return round(end - self.start_time, 2)


class Logger:
    """
    Simple console logger.
    """

    @staticmethod
    def info(message):
        print(f"[INFO] {message}")

    @staticmethod
    def success(message):
        print(f"[SUCCESS] {message}")

    @staticmethod
    def warning(message):
        print(f"[WARNING] {message}")

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")


def read_file(file_path):
    """
    Read file contents.
    """

    file = Path(file_path)

    return file.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def write_file(file_path, content):
    """
    Write content to file.
    """

    file = Path(file_path)

    file.write_text(
        content,
        encoding="utf-8"
    )


def ensure_directory(directory):
    """
    Create directory if it doesn't exist.
    """

    Path(directory).mkdir(
        parents=True,
        exist_ok=True
    )


def save_json(file_path, data):
    """
    Save dictionary as JSON.
    """

    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_json(file_path):
    """
    Load JSON file.
    """

    with open(file_path, "r", encoding="utf-8") as file:

        return json.load(file)


def file_exists(file_path):
    """
    Check if file exists.
    """

    return Path(file_path).exists()


def get_timestamp():
    """
    Return current timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def list_project_files(project_path):
    """
    List all files inside a project.
    """

    project = Path(project_path)

    files = []

    for file in project.rglob("*"):

        if file.is_file():

            files.append(
                str(file.relative_to(project))
            )

    return files


def validate_repository(project_path):
    """
    Check whether repository exists.
    """

    project = Path(project_path)

    if not project.exists():
        raise FileNotFoundError(
            f"Repository not found: {project_path}"
        )

    if not project.is_dir():
        raise ValueError(
            "Repository path must be a directory."
        )


def print_header(title):
    """
    Pretty console header.
    """

    line = "=" * 70

    print("\n")
    print(line)
    print(title.center(70))
    print(line)
    print()


def print_section(title):
    """
    Pretty section header.
    """

    print()
    print("-" * 50)
    print(title)
    print("-" * 50)


def shorten_text(text, limit=300):
    """
    Shorten long text.
    """

    if len(text) <= limit:
        return text

    return text[:limit] + "\n...\n"


def unique_files(file_list):
    """
    Remove duplicate file names.
    """

    return sorted(
        list(
            set(file_list)
        )
    )