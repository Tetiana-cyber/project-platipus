"""Модель нотатки. Owner: Dev 2."""

from __future__ import annotations

from datetime import datetime

from assistant.exceptions import ValidationError


class Note:
    """Атрибути: id, text, tags, created_at."""

    def __init__(self, note_id: int, text: str, tags: list[str] | None = None) -> None:
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValidationError("Текст нотатки не може бути порожнім.")

        normalized_tags: list[str] = []
        for tag in tags or []:
            cleaned_tag = tag.strip().lower()
            if cleaned_tag and cleaned_tag not in normalized_tags:
                normalized_tags.append(cleaned_tag)

        self.id = note_id
        self.text = cleaned_text
        self.tags = normalized_tags
        self.created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def edit(self, text: str) -> None:
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValidationError("Текст нотатки не може бути порожнім.")
        self.text = cleaned_text

    def add_tag(self, tag: str) -> None:
        cleaned_tag = tag.strip().lower()
        if cleaned_tag and cleaned_tag not in self.tags:
            self.tags.append(cleaned_tag)

    def remove_tag(self, tag: str) -> None:
        cleaned_tag = tag.strip().lower()
        if cleaned_tag in self.tags:
            self.tags.remove(cleaned_tag)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "tags": list(self.tags),
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Note:
        note = cls(
            note_id=data["id"],
            text=data["text"],
            tags=data.get("tags", []),
        )
        if "created_at" in data:
            note.created_at = data["created_at"]
        return note

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "-"
        return f"#{self.id}: {self.text} [{tags_str}]"
