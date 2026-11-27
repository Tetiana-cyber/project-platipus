"""Спільний контекст, який main.py передає в кожну команду. Owner: Tech Lead."""

from __future__ import annotations

from dataclasses import dataclass, field

from assistant.contacts.book import AddressBook
from assistant.notes.book import NoteBook


@dataclass
class Context:
    """Контейнер даних застосунку."""

    contacts: AddressBook = field(default_factory=AddressBook)
    notes: NoteBook = field(default_factory=NoteBook)

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "contacts": self.contacts.to_list(),
            "notes": self.notes.to_list(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Context:
        ctx = cls()
        if data.get("contacts"):
            ctx.contacts = AddressBook.from_list(data["contacts"])
        if data.get("notes"):
            ctx.notes = NoteBook.from_list(data["notes"])
        return ctx
