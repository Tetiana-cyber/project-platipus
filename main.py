"""Точка входу Персонального помічника. Owner: Tech Lead."""

from __future__ import annotations

import shlex

import assistant.contacts.commands  # noqa: F401  (реєструє команди)
import assistant.notes.commands  # noqa: F401  (реєструє команди)
from assistant import registry, ui
from assistant.context import Context
from assistant.exceptions import AssistantError
from assistant.storage import load_data, save_data
from assistant.suggest import suggest_command

EXIT_COMMANDS = {"exit", "close", "quit"}


def parse_input(line: str) -> tuple[str, list[str]]:
    """Розбиває рядок на (команда, аргументи). Підтримує лапки."""
    parts = shlex.split(line)
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def main() -> None:
    ctx = Context.from_dict(load_data())
    ui.print_menu(registry.all_commands())
    while True:
        try:
            line = ui.ask("Введіть команду: ")
            command, args = parse_input(line)
        except (KeyboardInterrupt, EOFError):
            command, args = "exit", []
        except ValueError:
            ui.print_error("Некоректні лапки у вводі.")
            continue

        if not command:
            continue
        if command in EXIT_COMMANDS:
            save_data(ctx.to_dict())
            ui.print_message("До побачення!")
            break

        handler = registry.get(command)
        if handler is None:
            hint = suggest_command(command, list(registry.all_commands()))
            ui.print_error(
                f"Невідома команда: {command}."
                + (f" Можливо, ви мали на увазі: {hint}?" if hint else "")
            )
            continue
        try:
            ui.print_message(handler(args, ctx))
            save_data(ctx.to_dict())
        except NotImplementedError:
            ui.print_error("Ця команда ще не реалізована.")
        except AssistantError as err:
            ui.print_error(str(err))


if __name__ == "__main__":
    main()
