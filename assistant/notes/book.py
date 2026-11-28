"""Книга нотаток. Owner: Dev 2."""

from __future__ import annotations

from assistant.exceptions import ValidationError
from assistant.notes.models import Note


class NoteBook:
    def __init__(self) -> None:
        self.data: dict[int, Note] = {}

    def get(self, note_id: int) -> Note:
        """Повертає нотатку за id або кидає ValidationError, якщо немає."""
        if note_id not in self.data:
            raise ValidationError(f"Нотатку з ID {note_id} не знайдено.")
        return self.data[note_id]

    def search(self, query: str) -> list[Note]:
        """Пошук за текстом (підрядок, без регістру)."""
        normalized = query.strip().casefold()
        if not normalized:
            raise ValidationError("Пошуковий запит не може бути порожнім.")

        return [
            note for note in self.data.values() if normalized in note.text.casefold()
        ]

    @staticmethod
    def _normalize_tag(tag: str) -> str:
        return tag.strip().casefold()

    @classmethod
    def _parse_tags_input(cls, raw_tags: str | list[str]) -> list[str]:
        parts = raw_tags.split(",") if isinstance(raw_tags, str) else list(raw_tags)
        if not parts:
            raise ValidationError("Список тегів не може бути порожнім.")

        normalized: list[str] = []
        for part in parts:
            trimmed = part.strip()
            if not trimmed:
                raise ValidationError("Тег не може бути порожнім.")
            tag = trimmed.casefold()
            if tag not in normalized:
                normalized.append(tag)
        return normalized

    def add_tags(self, note_id: int, raw_tags: str | list[str]) -> bool:
        """Додає теги до нотатки. Повертає True, якщо нотатка змінилась."""
        tags_to_add = self._parse_tags_input(raw_tags)
        note = self.get(note_id)

        note.tags = [self._normalize_tag(t) for t in note.tags]
        changed = False
        for tag in tags_to_add:
            if tag not in note.tags:
                note.tags.append(tag)
                changed = True
        return changed

    def search_by_tag(self, tag: str) -> list[Note]:
        """Пошук нотаток за точним нормалізованим тегом (read-only)."""
        normalized = self._normalize_tag(tag)
        if not normalized:
            raise ValidationError("Тег для пошуку не може бути порожнім.")

        return [
            note
            for note in self.data.values()
            if any(self._normalize_tag(t) == normalized for t in note.tags)
        ]

    def sorted_by_tags(self, selected_tags: list[str] | str) -> list[Note]:
        """Повертає нотатки за релевантністю вибраним тегам без мутації."""
        parsed = self._parse_tags_input(selected_tags)
        selected_set = set(parsed)

        notes_with_index = list(enumerate(self.data.values()))

        def _sort_key(item: tuple[int, Note]) -> tuple[int, int, int]:
            idx, note = item
            note_tags = {self._normalize_tag(t) for t in note.tags}
            match_count = len(note_tags & selected_set)
            has_match = 1 if match_count > 0 else 0
            return (-has_match, -match_count, idx)

        ordered = sorted(notes_with_index, key=_sort_key)
        return [note for _, note in ordered]

    def to_list(self) -> list[dict]:
        return [note.to_dict() for note in self.data.values()]

    @classmethod
    def from_list(cls, items: list[dict]) -> NoteBook:
        book = cls()
        for item in items:
            note = Note.from_dict(item)
            book.data[note.id] = note
        return book
