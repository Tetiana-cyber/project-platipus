"""Адресна книга. Owner: Dev 1."""

from __future__ import annotations

from assistant.contacts.models import Record


class AddressBook:
    """Колекція контактів. Ключ — ім'я контакту (унікальне)."""

    def __init__(self) -> None:
        self.data: dict[str, Record] = {}

    def add_record(self, record: Record) -> None:
        """DuplicateError, якщо контакт уже є."""
        raise NotImplementedError

    def find(self, name: str) -> Record:
        """NotFoundError, якщо контакту немає."""
        raise NotImplementedError

    def search(self, query: str) -> list[Record]:
        """Пошук за іменем, телефоном, email, адресою (підрядок, без регістру)."""
        raise NotImplementedError

    def delete(self, name: str) -> None:
        """NotFoundError, якщо контакту немає."""
        raise NotImplementedError

    def upcoming_birthdays(self, days: int) -> list[Record]:
        """Контакти, у яких день народження через `days` днів від сьогодні."""
        raise NotImplementedError

    def to_list(self) -> list[dict]:
        return [record.to_dict() for record in self.data.values()]

    @classmethod
    def from_list(cls, items: list[dict]) -> AddressBook:
        book = cls()
        for item in items:
            book.add_record(Record.from_dict(item))
        return book
