"""Спільний UI. Owner: Tech Lead. Сигнатури не змінювати без узгодження.

Усі команди друкують результат ТІЛЬКИ через ці функції (або повертають str).
"""

from __future__ import annotations


def ask(prompt: str) -> str:
    """Запитує рядок у користувача."""
    return input(prompt).strip()


def print_message(text: str) -> None:
    """Звичайне повідомлення."""
    if text:
        print(text)


def print_error(text: str) -> None:
    """Повідомлення про помилку."""
    print(f"Помилка: {text}")


def print_table(headers: list[str], rows: list[list[str]]) -> str:
    """Повертає текстову таблицю (щоб команда могла повернути її як str)."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * w for w in widths)
    body = [
        " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(row)) for row in rows
    ]
    return "\n".join([line, sep, *body])


def print_menu(commands: dict[str, str]) -> None:
    """Головне меню — показуємо ЛИШЕ при запуску."""
    print("=== Персональний помічник ===")
    for name, help_text in commands.items():
        print(f"  {help_text or name}")
    print("  exit / close / quit — вийти\n")
