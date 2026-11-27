"""Команди нотаток. Owner: Dev 2.

Підпис кожної команди: (args: list[str], ctx: Context) -> str
"""

from __future__ import annotations

from assistant.context import Context
from assistant.exceptions import ValidationError
from assistant.notes.models import Note
from assistant.registry import register
from assistant.ui import ask, print_message


def _format_note(note: Note) -> str:
    tags = ", ".join(note.tags) if note.tags else "-"
    return f"ID: {note.id} | {note.text} | tags: {tags}"


@register("add-note", "add-note <text> — додати нотатку")
def add_note(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("edit-note", "edit-note <id> <text> — змінити нотатку")
def edit_note(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("delete-note", "delete-note <id> — видалити нотатку")
def delete_note(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("find-note", "find-note <query> — пошук нотаток")
def find_note(args: list[str], ctx: Context) -> str:
    raw_query = " ".join(args).strip()
    if not raw_query:
        raw_query = ask("Введіть текст для пошуку: ").strip()

    if not raw_query:
        raise ValidationError("Пошуковий запит не може бути порожнім.")

    matches = ctx.notes.search(raw_query)

    if not matches:
        message = f"Нотаток за запитом '{raw_query}' не знайдено."
        print_message(message)
        return message

    return "\n".join(_format_note(note) for note in matches)


@register("show-notes", "show-notes — усі нотатки")
def show_notes(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("add-tag", "add-tag <id> <tag> — додати тег")
def add_tag(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("find-by-tag", "find-by-tag <tag> — пошук за тегом")
def find_by_tag(args: list[str], ctx: Context) -> str:
    raise NotImplementedError


@register("sort-notes", "sort-notes — сортування нотаток за тегами")
def sort_notes(args: list[str], ctx: Context) -> str:
    raise NotImplementedError
