"""Реєстр команд застосунку."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

COMMANDS: dict[str, tuple[str, Callable[..., Any]]] = {}


def register(name: str, description: str = "") -> Callable:
    """Реєструє команду у словнику COMMANDS."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        COMMANDS[name] = (description, func)
        return func

    return decorator
