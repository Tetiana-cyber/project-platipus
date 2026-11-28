"""Contracts for the UTF-8 JSON store.

Version 1 uses the schema_version, contacts, and notes keys and lives at
~/.personal_assistant/data.json. The skeleton does not access this file.
"""

from pathlib import Path


class SaveError(OSError):
    """Report that changes in memory could not be saved."""


def load_data(path: Path) -> dict:
    raise NotImplementedError


def save_data(data: dict, path: Path) -> None:
    raise NotImplementedError
