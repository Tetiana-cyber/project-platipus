"""Точка входу Персонального помічника. Owner: TL.

TODO (TL): реалізувати цикл CLI:
1. завантажити дані (storage.load_data) і створити Context;
2. показати меню один раз (ui.print_menu);
3. у циклі: ввести команду, розібрати (parse_input), знайти обробник
   у registry, викликати handler(args, ctx), зберегти дані;
4. ловити AssistantError і показувати повідомлення, не закриваючи програму;
5. на exit / close / quit — зберегти дані й вийти.
"""

from __future__ import annotations

import assistant.contacts.commands  # noqa: F401  (реєструє команди)
import assistant.notes.commands  # noqa: F401  (реєструє команди)
from assistant.context import Context  # noqa: F401
from assistant.exceptions import AssistantError  # noqa: F401

EXIT_COMMANDS = {"exit", "close", "quit"}


def parse_input(line: str) -> tuple[str, list[str]]:
    """Розбиває рядок на (команда, аргументи). Підтримує лапки (shlex)."""
    raise NotImplementedError


def main() -> None:
    """Запускає цикл помічника."""
    print("Skeleton: цикл CLI ще не реалізовано (див. TODO у main.py).")


if __name__ == "__main__":
    main()
