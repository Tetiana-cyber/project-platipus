"""Книга нотаток. Owner: Dev 2."""

from __future__ import annotations

from assistant.notes.models import Note


class NoteBook:
    def __init__(self) -> None:
        self.data: dict[int, Note] = {}

    def to_list(self) -> list[dict]:
        return [note.to_dict() for note in self.data.values()]

    @classmethod
    def from_list(cls, items: list[dict]) -> NoteBook:
        book = cls()
        for item in items:
            note = Note.from_dict(item)
            book.data[note.id] = note
        return book
