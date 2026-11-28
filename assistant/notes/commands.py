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


def _notify_and_save(ctx: Context) -> None:
    on_change = getattr(ctx, "on_change", None)
    if callable(on_change):
        on_change()
    save = getattr(ctx, "save", None)
    if callable(save):
        save()


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


@register("add-tag", "add-tag <id> <tags> — додати один або кілька тегів")
def add_tag(args: list[str], ctx: Context) -> str:
    raw_id = ask("Введіть ID нотатки: ").strip() if not args else args[0].strip()

    try:
        note_id = int(raw_id)
    except ValueError as exc:
        raise ValidationError("ID нотатки має бути цілим числом.") from exc

    if len(args) > 1:
        raw_tags = " ".join(args[1:]).strip()
    else:
        raw_tags = ask("Введіть теги через кому: ").strip()

    if not raw_tags:
        raise ValidationError("Потрібно вказати хоча б один тег.")

    changed = ctx.notes.add_tags(note_id, raw_tags)
    if not changed:
        msg = f"Нотатка #{note_id} вже містить вказані теги. Стан не змінено."
        print_message(msg)
        return msg

    _notify_and_save(ctx)
    note = ctx.notes.data[note_id]
    return f"Теги оновлено для нотатки #{note_id}: {_format_note(note)}"


@register("find-by-tag", "find-by-tag <tag> — пошук за тегом")
def find_by_tag(args: list[str], ctx: Context) -> str:
    raw_tag = " ".join(args).strip()
    if not raw_tag:
        raw_tag = ask("Введіть тег для пошуку: ").strip()

    if not raw_tag:
        raise ValidationError("Тег для пошуку не може бути порожнім.")

    matches = ctx.notes.search_by_tag(raw_tag)
    if not matches:
        msg = f"Нотаток з тегом '{raw_tag.strip().casefold()}' не знайдено."
        print_message(msg)
        return msg

    return "\n".join(_format_note(note) for note in matches)


@register("sort-notes", "sort-notes <tags> — сортування нотаток за тегами")
def sort_notes(args: list[str], ctx: Context) -> str:
    raw_tags = " ".join(args).strip()
    if not raw_tags:
        raw_tags = ask("Введіть теги через кому для сортування: ").strip()

    if not raw_tags:
        raise ValidationError("Список тегів не може бути порожнім.")

    ordered = ctx.notes.sorted_by_tags(raw_tags)
    if not ordered:
        msg = "Нотаток немає."
        print_message(msg)
        return msg

    return "\n".join(_format_note(note) for note in ordered)
