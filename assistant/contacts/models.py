"""Моделі контактів. Owner: Dev 1.

Правила валідації (контракт):
- Name: непорожній, до 50 символів.
- Phone: рівно 10 цифр.
- Email: формат user@domain.tld.
- Birthday: вводиться DD.MM.YYYY, зберігається як ISO YYYY-MM-DD.
- Address: довільний непорожній рядок.
Некоректне значення -> ValidationError з зрозумілим текстом.
"""

from __future__ import annotations

from datetime import date

from assistant.exceptions import ValidationError  # noqa: F401


class Field:
    """Базовий клас поля. Зберігає значення у `value`."""

    def __init__(self, value: str) -> None:
        raise NotImplementedError


class Name(Field):
    pass


class Phone(Field):
    pass


class Email(Field):
    pass


class Address(Field):
    pass


class Birthday(Field):
    pass


class Record:
    """Один контакт."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError

    def add_phone(self, phone: str) -> None:
        raise NotImplementedError

    def edit_phone(self, old: str, new: str) -> None:
        raise NotImplementedError

    def remove_phone(self, phone: str) -> None:
        raise NotImplementedError

    def set_email(self, email: str) -> None:
        raise NotImplementedError

    def set_address(self, address: str) -> None:
        raise NotImplementedError

    def set_birthday(self, birthday: str) -> None:
        raise NotImplementedError

    def days_to_birthday(self, today: date | None = None) -> int | None:
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Формат — див. schemas/contact.schema.json."""
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict) -> Record:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
