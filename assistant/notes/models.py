"""Модель нотатки. Owner: Dev 2.

Правила (контракт):
- id: ціле число, унікальне, призначається NoteBook.
- text: непорожній рядок.
- tags: список рядків у нижньому регістрі, без дублікатів, без пробілів.
- created_at: ISO datetime (YYYY-MM-DDTHH:MM:SS).
"""

from __future__ import annotations

from datetime import datetime

from assistant.exceptions import ValidationError


def _validate_note_id(note_id: int) -> int:
    if not isinstance(note_id, int) or isinstance(note_id, bool) or note_id < 1:
        raise ValidationError("ID нотатки має бути додатним цілим числом.")
    return note_id


def _validate_text(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValidationError("Текст нотатки не може бути порожнім.")
    return text


def _normalize_tag(tag: str) -> str:
    if not isinstance(tag, str):
        raise ValidationError("Тег має бути рядком.")
    cleaned = tag.strip().lower()
    if not cleaned or any(ch.isspace() for ch in cleaned):
        raise ValidationError("Тег не може бути порожнім або містити пробіли.")
    return cleaned


def _normalize_tags(tags: list[str] | None) -> list[str]:
    if tags is None:
        return []
    if not isinstance(tags, list):
        raise ValidationError("Теги мають бути списком рядків.")
    result: list[str] = []
    for tag in tags:
        normalized = _normalize_tag(tag)
        if normalized not in result:
            result.append(normalized)
    return result


class Note:
    """Атрибути: id, text, tags, created_at."""

    def __init__(
        self,
        note_id: int,
        text: str,
        tags: list[str] | None = None,
        created_at: str | None = None,
    ) -> None:
        self.id: int = _validate_note_id(note_id)
        self.text: str = _validate_text(text)
        self.tags: list[str] = _normalize_tags(tags)
        if created_at is None:
            self.created_at: str = datetime.now().replace(microsecond=0).isoformat()
        else:
            if not isinstance(created_at, str) or not created_at.strip():
                raise ValidationError("Некоректна дата створення нотатки.")
            try:
                datetime.fromisoformat(created_at)
            except ValueError as exc:
                raise ValidationError("Дата створення має бути в ISO-форматі.") from exc
            self.created_at = created_at

    def edit(self, text: str) -> None:
        self.text = _validate_text(text)

    def add_tag(self, tag: str) -> None:
        normalized = _normalize_tag(tag)
        if normalized not in self.tags:
            self.tags.append(normalized)

    def remove_tag(self, tag: str) -> None:
        normalized = _normalize_tag(tag)
        if normalized in self.tags:
            self.tags.remove(normalized)

    def to_dict(self) -> dict:
        """Формат — див. schemas/note.schema.json."""
        return {
            "id": self.id,
            "text": self.text,
            "tags": list(self.tags),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Note:
        if not isinstance(data, dict):
            raise ValidationError("Дані нотатки мають бути словником.")
        expected_keys = {"id", "text", "tags", "created_at"}
        if set(data.keys()) != expected_keys:
            raise ValidationError("Некоректний набір полів у даних нотатки.")
        return cls(
            note_id=data["id"],
            text=data["text"],
            tags=data["tags"],
            created_at=data["created_at"],
        )

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "-"
        return f"[{self.id}] ({self.created_at}) {self.text} [tags: {tags_str}]"
