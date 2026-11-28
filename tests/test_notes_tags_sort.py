from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from assistant.exceptions import ValidationError
from assistant.notes.book import NoteBook
from assistant.notes.commands import add_tag, find_by_tag, sort_notes
from assistant.notes.models import Note


class SaveError(RuntimeError):
    """Тестова помилка збереження."""


def _make_note(note_id: int, text: str, tags: list[str] | None = None) -> Note:
    note = Note.__new__(Note)
    note.id = note_id
    note.text = text
    note.tags = [t.strip().casefold() for t in (tags or [])]
    note.created_at = "2026-11-28T02:04:00"
    return note


def _make_ctx(notes: dict[int, Note] | None = None) -> SimpleNamespace:
    book = NoteBook()
    if notes:
        book.data = notes
    return SimpleNamespace(
        notes=book,
        on_change=MagicMock(),
        save=MagicMock(),
    )


def test_add_tag_multiple_comma_separated_casefold_and_unicode():
    ctx = _make_ctx({1: _make_note(1, "Task", ["Existing"])})

    res = add_tag(["1", "  Терміново , WORK , existing  "], ctx)

    assert "1" in res
    assert ctx.notes.data[1].tags == ["existing", "терміново", "work"]
    ctx.on_change.assert_called_once()
    ctx.save.assert_called_once()


def test_add_tag_duplicate_no_change_calls_info_not_on_change():
    ctx = _make_ctx({1: _make_note(1, "Task", ["work"])})

    with patch("assistant.notes.commands.print_message") as mock_print:
        add_tag(["1", "  WORK  "], ctx)
        mock_print.assert_called_once()

    assert ctx.notes.data[1].tags == ["work"]
    ctx.on_change.assert_not_called()
    ctx.save.assert_not_called()


def test_add_tag_empty_element_raises_validation_error():
    ctx = _make_ctx({1: _make_note(1, "Task", ["work"])})

    with pytest.raises(ValidationError):
        add_tag(["1", "work, "], ctx)

    assert ctx.notes.data[1].tags == ["work"]
    ctx.on_change.assert_not_called()


def test_add_tag_propagates_save_error():
    ctx = _make_ctx({1: _make_note(1, "Task", [])})
    ctx.save.side_effect = SaveError("disk full")

    with pytest.raises(SaveError):
        add_tag(["1", "urgent"], ctx)

    ctx.on_change.assert_called_once()


def test_find_by_tag_exact_normalized_and_no_results():
    ctx = _make_ctx(
        {
            1: _make_note(1, "N1", ["work"]),
            2: _make_note(2, "N2", ["workshop"]),
            3: _make_note(3, "N3", ["WORK"]),
        }
    )

    out = find_by_tag(["  Work "], ctx)
    lines = out.splitlines()
    assert len(lines) == 2
    assert "ID: 1" in lines[0]
    assert "ID: 3" in lines[1]

    with patch("assistant.notes.commands.print_message") as mock_print:
        find_by_tag(["missing"], ctx)
        mock_print.assert_called_once()

    ctx.on_change.assert_not_called()


def test_sort_notes_ranking_ties_untagged_and_no_mutation():
    ctx = _make_ctx(
        {
            1: _make_note(1, "Only work", ["work"]),
            2: _make_note(2, "Both tags", ["work", "urgent"]),
            3: _make_note(3, "Home note", ["home"]),
            4: _make_note(4, "No tags note", []),
            5: _make_note(5, "Only urgent", ["urgent"]),
            6: _make_note(6, "Second work", ["work"]),
        }
    )

    out = sort_notes(["work, urgent"], ctx)
    ids_in_order = [
        int(line.split("|")[0].replace("ID:", "").strip()) for line in out.splitlines()
    ]

    assert ids_in_order == [2, 1, 5, 6, 3, 4]
    assert list(ctx.notes.data.keys()) == [1, 2, 3, 4, 5, 6]
    ctx.on_change.assert_not_called()
    ctx.save.assert_not_called()


def test_sort_notes_empty_tags_raises_validation_error():
    ctx = _make_ctx({1: _make_note(1, "N1", ["work"])})

    with (
        patch("assistant.notes.commands.ask", return_value="  ,  "),
        pytest.raises(ValidationError),
    ):
        sort_notes([], ctx)
