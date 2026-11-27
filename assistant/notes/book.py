"""Книга нотаток. Owner: Dev 2."""

from __future__ import annotations

from assistant.exceptions import NotFoundError, ValidationError
from assistant.notes.models import Note, _normalize_tag, _validate_note_id


class NoteBook:
    def __init__(self) -> None:
        self.data: dict[int, Note] = {}
        self._next_id: int = 1

    def _allocate_id(self) -> int:
        while self._next_id in self.data:
            self._next_id += 1
        note_id = self._next_id
        self._next_id += 1
        return note_id

    def add_note(self, text: str, tags: list[str] | None = None) -> Note:
        """Створює нотатку з новим id."""
        note_id = self._allocate_id()
        note = Note(note_id=note_id, text=text, tags=tags)
        self.data[note.id] = note
        return note

    def get(self, note_id: int) -> Note:
        """NotFoundError, якщо немає."""
        valid_id = _validate_note_id(note_id)
        if valid_id not in self.data:
            raise NotFoundError(f"Нотатку з ID {valid_id} не знайдено.")
        return self.data[valid_id]

    def edit_note(self, note_id: int, text: str) -> Note:
        note = self.get(note_id)
        note.edit(text)
        return note

    def search(self, query: str) -> list[Note]:
        """Пошук за текстом (підрядок, без регістру)."""
        if not isinstance(query, str) or not query.strip():
            raise ValidationError("Пошуковий запит не може бути порожнім.")
        needle = query.casefold()
        return [note for note in self.data.values() if needle in note.text.casefold()]

    def search_by_tag(self, tag: str) -> list[Note]:
        normalized = _normalize_tag(tag)
        return [note for note in self.data.values() if normalized in note.tags]

    def sorted_by_tags(self) -> list[Note]:
        """Нотатки, відсортовані за тегами."""
        return sorted(
            self.data.values(),
            key=lambda note: (
                0 if note.tags else 1,
                ",".join(note.tags),
                note.id,
            ),
        )

    def delete(self, note_id: int) -> None:
        valid_id = _validate_note_id(note_id)
        if valid_id not in self.data:
            raise NotFoundError(f"Нотатку з ID {valid_id} не знайдено.")
        del self.data[valid_id]

    def to_list(self) -> list[dict]:
        return [note.to_dict() for note in self.data.values()]

    @classmethod
    def from_list(cls, items: list[dict]) -> NoteBook:
        if not isinstance(items, list):
            raise ValidationError("Список нотаток має бути масивом.")
        book = cls()
        max_id = 0
        for item in items:
            note = Note.from_dict(item)
            if note.id in book.data:
                raise ValidationError(
                    f"Дублікат ID нотатки при завантаженні: {note.id}."
                )
            book.data[note.id] = note
            if note.id > max_id:
                max_id = note.id
        book._next_id = max_id + 1
        return book
