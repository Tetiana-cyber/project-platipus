"""Command suggestion contract for the skeleton."""

from collections.abc import Iterable


def suggest_command(text: str, commands: Iterable[str]) -> str | None:
    raise NotImplementedError
