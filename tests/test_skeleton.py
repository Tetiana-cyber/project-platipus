"""Smoke-тести каркаса: усе імпортується, команди зареєстровані, storage працює."""

from __future__ import annotations

import main
from assistant import registry, storage

EXPECTED = {
    "add-contact", "edit-contact", "delete-contact", "find-contact",
    "show-contacts", "birthdays", "add-note", "edit-note", "delete-note",
    "find-note", "show-notes", "add-tag", "find-by-tag", "sort-notes",
}  # fmt: skip


def test_commands_registered():
    assert EXPECTED <= set(registry.all_commands())


def test_parse_input():
    assert main.parse_input('add-note "hello world"') == ("add-note", ["hello world"])
    assert main.parse_input("") == ("", [])


def test_storage_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("PA_DATA_FILE", str(tmp_path / "data.json"))
    assert storage.load_data() == {}
    storage.save_data({"version": 1, "contacts": [], "notes": []})
    assert storage.load_data()["version"] == 1
