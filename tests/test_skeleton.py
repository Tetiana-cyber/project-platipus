"""Smoke-тести каркаса: усе імпортується, команди зареєстровані."""

from __future__ import annotations

import main  # noqa: F401
from assistant import registry

EXPECTED = {
    "add-contact", "edit-contact", "delete-contact", "find-contact",
    "show-contacts", "birthdays", "add-note", "edit-note", "delete-note",
    "find-note", "show-notes", "add-tag", "find-by-tag", "sort-notes",
}  # fmt: skip


def test_commands_registered():
    assert EXPECTED <= set(registry.all_commands())
