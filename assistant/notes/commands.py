"""Команди нотаток. Owner: Dev 2.

Підпис кожної команди: (args: list[str], ctx: Context) -> str
"""

from __future__ import annotations

from assistant.context import Context
from assistant.exceptions import CommandArgumentError
from assistant.registry import register


def _parse_id(raw_id: str) -> int:
    try:
        return int(raw_id)
    except ValueError as exc:
        raise CommandArgumentError("ID нотатки має бути цілим числом.") from exc


@register("add-note", "add-note <text> — додати нотатку")
def add_note(args: list[str], ctx: Context) -> str:
    text = " ".join(args)
    note = ctx.notes.add_note(text)
    return f"Note #{note.id} added."


@register("edit-note", "edit-note <id> <text> — змінити нотатку")
def edit_note(args: list[str], ctx: Context) -> str:
    if len(args) < 2:
        raise CommandArgumentError("Використання: edit-note <id> <text>")
    note_id = _parse_id(args[0])
    new_text = " ".join(args[1:])
    note = ctx.notes.edit_note(note_id, new_text)
    return f"Note #{note.id} updated."


@register("delete-note", "delete-note <id> [confirm] — видалити нотатку")
def delete_note(args: list[str], ctx: Context) -> str:
    if not args:
        raise CommandArgumentError("Використання: delete-note <id> [confirm]")
    note_id = _parse_id(args[0])
    ctx.notes.get(note_id)
    if len(args) < 2 or args[1].strip().lower() not in {"confirm", "yes"}:
        return f"Deletion cancelled. Run 'delete-note {note_id} confirm' to confirm."
    ctx.notes.delete(note_id)
    return f"Note #{note_id} deleted."


@register("find-note", "find-note <query> — пошук нотаток")
def find_note(args: list[str], ctx: Context) -> str:
    query = " ".join(args)
    matches = ctx.notes.search(query)
    if not matches:
        return "No matching notes found."
    return "\n".join(str(note) for note in matches)


@register("show-notes", "show-notes — усі нотатки")
def show_notes(args: list[str], ctx: Context) -> str:
    if args:
        raise CommandArgumentError("Команда show-notes не приймає аргументів.")
    if not ctx.notes.data:
        return "Notes book is empty."
    return "\n".join(str(note) for note in ctx.notes.data.values())


@register("add-tag", "add-tag <id> <tag> — додати тег до нотатки")
def add_tag(args: list[str], ctx: Context) -> str:
    if len(args) < 2:
        raise CommandArgumentError("Використання: add-tag <id> <tag>")
    note_id = _parse_id(args[0])
    tag = " ".join(args[1:])
    note = ctx.notes.get(note_id)
    note.add_tag(tag)
    return f"Tag added to note #{note.id}."


@register("find-by-tag", "find-by-tag <tag> — пошук нотаток за тегом")
def find_by_tag(args: list[str], ctx: Context) -> str:
    tag = " ".join(args)
    matches = ctx.notes.search_by_tag(tag)
    if not matches:
        return "No matching notes found."
    return "\n".join(str(note) for note in matches)


@register("sort-notes", "sort-notes — нотатки, відсортовані за тегами")
def sort_notes(args: list[str], ctx: Context) -> str:
    if args:
        raise CommandArgumentError("Команда sort-notes не приймає аргументів.")
    notes = ctx.notes.sorted_by_tags()
    if not notes:
        return "Notes book is empty."
    return "\n".join(str(note) for note in notes)
