"""Книга нотаток. Owner: Dev 2."""

from __future__ import annotations

from assistant.notes.models import Note


class NoteBook:
    def __init__(self) -> None:
        self.data: dict[int, Note] = {}

    def add_note(self, text: str, tags: list[str] | None = None) -> Note:
        """Створює нотатку з новим id."""
        raise NotImplementedError

    def get(self, note_id: int) -> Note:
        """NotFoundError, якщо немає."""
        raise NotImplementedError

    def search(self, query: str) -> list[Note]:
        """Пошук за текстом (підрядок, без регістру)."""
        raise NotImplementedError

    def search_by_tag(self, tag: str) -> list[Note]:
        raise NotImplementedError

    def sorted_by_tags(self) -> list[Note]:
        """Нотатки, відсортовані за тегами."""
        raise NotImplementedError

    def delete(self, note_id: int) -> None:
        raise NotImplementedError

    def to_list(self) -> list[dict]:
        return [note.to_dict() for note in self.data.values()]

    @classmethod
    def from_list(cls, items: list[dict]) -> NoteBook:
        book = cls()
        for item in items:
            note = Note.from_dict(item)
            book.data[note.id] = note
        return book
