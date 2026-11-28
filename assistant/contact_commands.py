"""Contact command registry for the skeleton."""

from collections.abc import Callable

from assistant import ui
from assistant.contacts import AddressBook


def _unavailable() -> None:
    ui.info("This command is not available yet.")


def get_handlers(
    book: AddressBook, on_change: Callable[[], None]
) -> dict[str, Callable[[], None]]:
    """Expose the agreed contact command names."""
    return {
        "add-contact": _unavailable,
        "list-contacts": _unavailable,
        "edit-contact": _unavailable,
        "delete-contact": _unavailable,
        "find-contact": _unavailable,
        "birthdays": _unavailable,
    }
