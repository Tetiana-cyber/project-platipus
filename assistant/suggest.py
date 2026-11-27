"""Підказка найближчої команди (додаткове завдання). Owner: Tech Lead."""

from __future__ import annotations

import difflib


def suggest_command(text: str, commands: list[str]) -> str | None:
    """Повертає найближчу команду до `text` або None."""
    matches = difflib.get_close_matches(text, commands, n=1, cutoff=0.5)
    return matches[0] if matches else None
