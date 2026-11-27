"""Команди контактів. Owner: Dev 1.

Підпис кожної команди: (args: list[str], ctx: Context) -> str
Повертає текст для користувача. Помилки — через винятки з exceptions.py.
"""

from __future__ import annotations

from assistant.context import Context
from assistant.registry import register


@register("add-contact", "add-contact <name> <phone> — додати контакт")
def add_contact(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("edit-contact", "edit-contact <name> <field> <value> — змінити поле")
def edit_contact(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("delete-contact", "delete-contact <name> — видалити контакт")
def delete_contact(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("find-contact", "find-contact <query> — пошук контактів")
def find_contact(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("show-contacts", "show-contacts — усі контакти")
def show_contacts(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("birthdays", "birthdays <days> — іменинники через N днів")
def birthdays(args: list[str], ctx: Context) -> str:
    raise NotImplementedError
