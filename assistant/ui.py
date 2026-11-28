"""Спільний UI. Owner: TL. Сигнатури не змінювати без узгодження."""

from __future__ import annotations


def ask(prompt: str) -> str:
    """Запитує рядок у користувача."""
    return input(prompt)


def print_message(text: str) -> None:
    """Звичайне повідомлення."""
    print(text)


def print_error(text: str) -> None:
    """Повідомлення про помилку."""
    raise NotImplementedError


def print_table(headers: list[str], rows: list[list[str]]) -> str:
    """Повертає текстову таблицю."""
    raise NotImplementedError


def print_menu(commands: dict[str, str]) -> None:
    """Головне меню."""
    raise NotImplementedError
