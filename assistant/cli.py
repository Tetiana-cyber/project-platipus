"""Minimal command loop for the Personal Assistant skeleton."""

from collections.abc import Callable

from assistant import contact_commands, note_commands, ui
from assistant.contacts import AddressBook
from assistant.notes import NoteBook


def run(
    book: AddressBook,
    notes: NoteBook,
    on_change: Callable[[], None],
    *,
    has_unsaved_changes: Callable[[], bool],
) -> None:
    """Run the command loop with the agreed persistence callbacks."""

    def show_help() -> None:
        ui.info("Available commands:")
        for command in handlers:
            ui.info(f"  {command}")

    handlers: dict[str, Callable[[], None] | None] = {
        **contact_commands.get_handlers(book, on_change),
        **note_commands.get_handlers(notes, on_change),
        "help": show_help,
        "exit": None,
        "close": None,
    }

    try:
        ui.info("Personal Assistant")
        show_help()
        while True:
            command = ui.prompt("Command").strip().casefold()
            if not command:
                ui.error("Enter a command. Type 'help' for options.")
                continue
            if command not in handlers:
                ui.error("Unknown command. Type 'help' for options.")
                continue

            handler = handlers[command]
            if handler is None:
                return
            handler()
    except (EOFError, KeyboardInterrupt):
        ui.info("\nGoodbye.")
