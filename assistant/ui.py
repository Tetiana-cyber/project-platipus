"""Shared terminal input and output contracts."""

from datetime import date

from assistant.contacts import Contact
from assistant.notes import Note


def prompt(label: str) -> str:
    return input(f"{label}: ")


def success(message: str) -> None:
    print(message)


def error(message: str) -> None:
    print(f"Error: {message}")


def info(message: str) -> None:
    print(message)


def show_contacts(contacts: list[Contact]) -> None:
    raise NotImplementedError


def show_notes(notes: list[Note]) -> None:
    raise NotImplementedError


def show_birthdays(
    items: list[tuple[Contact, date]], *, today: date | None = None
) -> None:
    raise NotImplementedError
