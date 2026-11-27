"""Реєстр команд. Owner: Tech Lead.

Кожен розробник реєструє свої команди у своєму commands.py:

    @register("add-contact", "add-contact <name> <phone> — додати контакт")
    def add_contact(args: list[str], ctx: Context) -> str: ...
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assistant.context import Context

Handler = Callable[[list[str], "Context"], str]

_COMMANDS: dict[str, tuple[Handler, str]] = {}


def register(name: str, help_text: str) -> Callable[[Handler], Handler]:
    """Декоратор: реєструє обробник команди під іменем `name`."""

    def decorator(func: Handler) -> Handler:
        if name in _COMMANDS:
            raise ValueError(f"Команда '{name}' уже зареєстрована")
        _COMMANDS[name] = (func, help_text)
        return func

    return decorator


def get(name: str) -> Handler | None:
    entry = _COMMANDS.get(name)
    return entry[0] if entry else None


def all_commands() -> dict[str, str]:
    """Повертає {назва_команди: опис}."""
    return {name: help_text for name, (_, help_text) in sorted(_COMMANDS.items())}
