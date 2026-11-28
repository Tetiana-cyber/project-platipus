"""Start the Personal Assistant skeleton."""

from assistant import cli
from assistant.contacts import AddressBook
from assistant.notes import NoteBook
from assistant.storage import SaveError


def on_change() -> None:
    """Report that persistence is unavailable in the skeleton."""
    raise SaveError("Saving is not implemented yet.")


def has_unsaved_changes() -> bool:
    """Return False while the skeleton has no commands that change data."""
    return False


def main() -> None:
    """Connect the empty books and the CLI without loading user data."""
    cli.run(
        AddressBook(),
        NoteBook(),
        on_change,
        has_unsaved_changes=has_unsaved_changes,
    )


if __name__ == "__main__":
    main()
