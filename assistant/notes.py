"""Note and notebook contracts for the skeleton."""

from __future__ import annotations


class Note:
    """Public note fields and serialization contract."""

    id: str
    text: str
    tags: list[str]

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict) -> Note:
        raise NotImplementedError


class NoteBook:
    """Note collection contract."""

    def add_note(self, text: str) -> Note:
        raise NotImplementedError

    def get_note(self, note_id: str) -> Note:
        raise NotImplementedError

    def list_notes(self) -> list[Note]:
        raise NotImplementedError

    def update_note(self, note_id: str, text: str) -> Note:
        raise NotImplementedError

    def delete_note(self, note_id: str) -> None:
        raise NotImplementedError

    def search_notes(self, query: str) -> list[Note]:
        raise NotImplementedError

    def add_tags(self, note_id: str, tags: list[str]) -> Note:
        raise NotImplementedError

    def find_by_tag(self, tag: str) -> list[Note]:
        raise NotImplementedError

    def sort_by_tags(self, tags: list[str]) -> list[Note]:
        raise NotImplementedError

    def to_dict(self) -> list[dict]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: list[dict]) -> NoteBook:
        raise NotImplementedError
