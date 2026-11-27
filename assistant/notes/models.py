"""Модель нотатки. Owner: Dev 2.

Правила (контракт):
- id: ціле число, унікальне, призначається NoteBook.
- text: непорожній рядок.
- tags: список рядків у нижньому регістрі, без дублікатів, без пробілів.
- created_at: ISO datetime (YYYY-MM-DDTHH:MM:SS).
"""

from __future__ import annotations

from assistant.exceptions import ValidationError  # noqa: F401


class Note:
    """Атрибути: id, text, tags, created_at."""

    def __init__(self, note_id: int, text: str, tags: list[str] | None = None):
        raise NotImplementedError

    def edit(self, text: str) -> None:
        raise NotImplementedError

    def add_tag(self, tag: str) -> None:
        raise NotImplementedError

    def remove_tag(self, tag: str) -> None:
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Формат — див. schemas/note.schema.json."""
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict) -> Note:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
