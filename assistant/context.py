"""Спільний контекст, який main.py передає в кожну команду. Owner: Tech Lead."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from assistant.notes.book import NoteBook

try:
    from assistant.contacts.book import AddressBook
except ModuleNotFoundError:

    class AddressBook:  # type: ignore[no-redef]
        """Тимчасова заглушка, доки модуль контактів не додано."""

        def to_list(self) -> list[dict[str, Any]]:
            return []

        @classmethod
        def from_list(cls, items: list[dict[str, Any]]) -> AddressBook:
            return cls()


@dataclass
class Context:
    """Контейнер даних застосунку."""

    contacts: AddressBook = field(default_factory=AddressBook)
    notes: NoteBook = field(default_factory=NoteBook)

    def to_dict(self) -> dict:
        to_list = getattr(self.contacts, "to_list", None)
        contacts_data = to_list() if callable(to_list) else []
        return {"version": 1, "contacts": contacts_data, "notes": self.notes.to_list()}

    @classmethod
    def from_dict(cls, data: dict) -> Context:
        ctx = cls()
        from_list = getattr(AddressBook, "from_list", None)
        if data.get("contacts") and callable(from_list):
            ctx.contacts = from_list(data["contacts"])
        if data.get("notes"):
            ctx.notes = NoteBook.from_list(data["notes"])
        return ctx
