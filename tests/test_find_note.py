from types import SimpleNamespace
from unittest.mock import patch

import pytest
from assistant.notes.models import Note

from assistant.exceptions import ValidationError
from assistant.notes.book import NoteBook
from assistant.notes.commands import find_note


def _make_note(note_id: int, text: str, tags: list[str] | None = None) -> Note:
    note = Note.__new__(Note)
    note.id = note_id
    note.text = text
    note.tags = tags or []
    note.created_at = "2026-11-28T01:51:00"
    return note


def _make_ctx() -> SimpleNamespace:
    return SimpleNamespace(notes=NoteBook())


def test_find_note_casefold_after_trim_and_keeps_order():
    ctx = _make_ctx()
    n1 = _make_note(1, "Daily standup", ["work"])
    n2 = _make_note(2, "Team Meeting notes", ["sync"])
    n3 = _make_note(3, "Another MEETING recap", ["archive"])
    ctx.notes.data = {1: n1, 2: n2, 3: n3}

    result = find_note(["  mEeTiNg  "], ctx)
    lines = result.splitlines()

    assert len(lines) == 2
    assert "ID: 2" in lines[0]
    assert "Team Meeting notes" in lines[0]
    assert "sync" in lines[0]
    assert "ID: 3" in lines[1]
    assert "Another MEETING recap" in lines[1]
    assert "archive" in lines[1]


def test_find_note_searches_only_text_not_tags():
    ctx = _make_ctx()
    ctx.notes.data = {1: _make_note(1, "Buy groceries", ["meeting"])}

    with patch("assistant.notes.commands.print_message") as mock_print:
        find_note(["meeting"], ctx)
        mock_print.assert_called_once()


def test_find_note_no_matches_calls_print_message_and_keeps_data():
    ctx = _make_ctx()
    original = _make_note(1, "Buy coffee", ["food"])
    ctx.notes.data = {1: original}

    with patch("assistant.notes.commands.print_message") as mock_print:
        msg = find_note(["absent"], ctx)
        mock_print.assert_called_once_with(msg)

    assert list(ctx.notes.data.keys()) == [1]
    assert ctx.notes.data[1].text == "Buy coffee"


def test_find_note_empty_query_raises_validation_error():
    ctx = _make_ctx()
    with (
        patch("assistant.notes.commands.ask", return_value="   "),
        pytest.raises(ValidationError),
    ):
        find_note([], ctx)
