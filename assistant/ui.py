"""Спільний UI. Owner: TL. Сигнатури не змінювати без узгодження.

Усі команди друкують результат ТІЛЬКИ через ці функції (або повертають str).
"""

from __future__ import annotations


def ask(prompt: str) -> str:
    """Запитує рядок у користувача."""
    raise NotImplementedError


def print_message(text: str) -> None:
    """Звичайне повідомлення."""
    raise NotImplementedError


def print_error(text: str) -> None:
    """Повідомлення про помилку."""
    raise NotImplementedError


def print_table(headers: list[str], rows: list[list[str]]) -> str:
    """Повертає текстову таблицю (щоб команда могла повернути її як str)."""
    raise NotImplementedError


def print_menu(commands: dict[str, str]) -> None:
    """Головне меню — показуємо ЛИШЕ при запуску."""
    raise NotImplementedError
