"""Contact and address book contracts for the skeleton."""

from __future__ import annotations

from datetime import date


class Field:
    """Base class for contact fields."""

    def __init__(self, value: str | date | None) -> None:
        self.value = value


class Name(Field):
    """Contact name field."""


class Address(Field):
    """Contact address field."""


class Phone(Field):
    """Contact phone field."""


class Email(Field):
    """Contact email field."""


class Birthday(Field):
    """Contact birthday field."""


class Contact:
    """Public contact fields and serialization contract."""

    name: str
    address: str | None
    phone: str | None
    email: str | None
    birthday: date | None

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict) -> Contact:
        raise NotImplementedError


class AddressBook:
    """Contact collection contract."""

    def add_contact(
        self,
        name: str,
        *,
        address: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        birthday: str | date | None = None,
    ) -> Contact:
        raise NotImplementedError

    def get_contact(self, name: str) -> Contact:
        raise NotImplementedError

    def list_contacts(self) -> list[Contact]:
        raise NotImplementedError

    def update_contact(
        self, name: str, /, **changes: str | date | None
    ) -> Contact:
        raise NotImplementedError

    def delete_contact(self, name: str) -> None:
        raise NotImplementedError

    def search_contacts(
        self, query: str, *, field: str = "name"
    ) -> list[Contact]:
        raise NotImplementedError

    def upcoming_birthdays(
        self, days: int, *, today: date | None = None, exact: bool = False
    ) -> list[tuple[Contact, date]]:
        raise NotImplementedError

    def to_dict(self) -> list[dict]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: list[dict]) -> AddressBook:
        raise NotImplementedError
