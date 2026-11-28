import json
from pathlib import Path
from unittest.mock import patch

import pytest

from assistant.context import Context
from assistant.exceptions import (
    SaveError,
    StorageLoadError,
    StorageRecordError,
    StorageSchemaError,
)
from assistant.notes.models import Note
from assistant.storage import StorageManager


def _seed_context() -> Context:
    ctx = Context()
    ctx.notes.data[1] = Note(note_id=1, text="First note", tags=["work"])
    return ctx


def test_load_invalid_json_preserves_file_and_does_not_reset_dirty(tmp_path: Path):
    target = tmp_path / "storage.json"
    corrupted = "{not valid json"
    target.write_text(corrupted, encoding="utf-8")
    mgr = StorageManager(target, context=_seed_context())
    mgr.on_change()
    with pytest.raises(StorageLoadError):
        mgr.load()
    assert target.read_text(encoding="utf-8") == corrupted
    assert mgr.context.notes.data[1].text == "First note"
    assert mgr.has_unsaved_changes() is True


def test_load_invalid_schema_version_raises_schema_error(tmp_path: Path):
    target = tmp_path / "storage.json"
    target.write_text(
        json.dumps({"version": 999, "contacts": [], "notes": []}), encoding="utf-8"
    )
    with pytest.raises(StorageSchemaError):
        StorageManager(target).load()


def test_load_invalid_record_raises_record_error(tmp_path: Path):
    target = tmp_path / "storage.json"
    target.write_text(
        json.dumps({"version": 1, "contacts": [], "notes": [{"id": 1, "text": "   "}]}),
        encoding="utf-8",
    )
    with pytest.raises(StorageRecordError):
        StorageManager(target).load()


def test_failed_save_keeps_previous_file_no_success_and_keeps_dirty(tmp_path: Path):
    target = tmp_path / "storage.json"
    original_content = json.dumps(
        {"version": 1, "contacts": [], "notes": [{"id": 1, "text": "Old"}]}
    )
    target.write_text(original_content, encoding="utf-8")
    mgr = StorageManager(target, context=_seed_context())
    mgr.on_change()
    with (
        patch("assistant.storage.os.replace", side_effect=OSError("permission denied")),
        pytest.raises(SaveError),
    ):
        mgr.save()
    assert target.read_text(encoding="utf-8") == original_content
    assert mgr.has_unsaved_changes() is True


def test_retry_save_writes_both_books_without_remutation_and_clears_dirty(
    tmp_path: Path,
):
    target = tmp_path / "storage.json"
    mgr = StorageManager(target, context=_seed_context())
    mgr.on_change()
    with (
        patch("assistant.storage.os.replace", side_effect=OSError("disk full")),
        pytest.raises(SaveError),
    ):
        mgr.save()
    assert mgr.has_unsaved_changes() is True
    mgr.retry_save()
    assert mgr.has_unsaved_changes() is False
    reloaded = StorageManager(target).load()
    assert reloaded.notes.data[1].text == "First note"
    assert reloaded.notes.data[1].tags == ["work"]
    assert isinstance(reloaded.to_dict()["contacts"], list)
