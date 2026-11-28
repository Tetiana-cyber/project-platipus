"""Note command registry for the skeleton."""

from collections.abc import Callable

from assistant import ui
from assistant.notes import NoteBook


def _unavailable() -> None:
    ui.info("This command is not available yet.")


def get_handlers(
    notes: NoteBook, on_change: Callable[[], None]
) -> dict[str, Callable[[], None]]:
    """Expose the agreed note and tag command names."""
    return {
        "add-note": _unavailable,
        "list-notes": _unavailable,
        "edit-note": _unavailable,
        "delete-note": _unavailable,
        "find-note": _unavailable,
        "add-tag": _unavailable,
        "find-tag": _unavailable,
        "sort-notes": _unavailable,
    }
