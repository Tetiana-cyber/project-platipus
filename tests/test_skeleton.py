"""Check the public skeleton contracts and a safe startup."""

import runpy
import subprocess
import sys
from importlib import import_module
from inspect import signature
from pathlib import Path
from unittest.mock import Mock

import pytest

from assistant import (
    cli,
    contact_commands,
    note_commands,
    storage,
    suggestions,
    ui,
)
from assistant.contacts import (
    Address,
    AddressBook,
    Birthday,
    Contact,
    Email,
    Field,
    Name,
    Phone,
)
from assistant.notes import Note, NoteBook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SIGNATURE = signature(cli.run)


@pytest.mark.parametrize(
    "module_name",
    [
        "main",
        "assistant",
        "assistant.cli",
        "assistant.contact_commands",
        "assistant.contacts",
        "assistant.note_commands",
        "assistant.notes",
        "assistant.storage",
        "assistant.suggestions",
        "assistant.ui",
    ],
)
def test_module_imports(module_name):
    assert import_module(module_name).__name__ == module_name


def test_field_and_error_inheritance():
    for field_type in (Name, Address, Phone, Email, Birthday):
        assert issubclass(field_type, Field)
    assert issubclass(storage.SaveError, OSError)


@pytest.mark.parametrize(
    ("public_callable", "parameters"),
    [
        (Field, "(value)"),
        (Contact.to_dict, "(self)"),
        (Contact.from_dict, "(data)"),
        (
            AddressBook.add_contact,
            "(self, name, *, address=None, phone=None, email=None, "
            "birthday=None)",
        ),
        (AddressBook.get_contact, "(self, name)"),
        (AddressBook.list_contacts, "(self)"),
        (AddressBook.update_contact, "(self, name, /, **changes)"),
        (AddressBook.delete_contact, "(self, name)"),
        (AddressBook.search_contacts, "(self, query, *, field='name')"),
        (
            AddressBook.upcoming_birthdays,
            "(self, days, *, today=None, exact=False)",
        ),
        (AddressBook.to_dict, "(self)"),
        (AddressBook.from_dict, "(data)"),
        (Note.to_dict, "(self)"),
        (Note.from_dict, "(data)"),
        (NoteBook.add_note, "(self, text)"),
        (NoteBook.get_note, "(self, note_id)"),
        (NoteBook.list_notes, "(self)"),
        (NoteBook.update_note, "(self, note_id, text)"),
        (NoteBook.delete_note, "(self, note_id)"),
        (NoteBook.search_notes, "(self, query)"),
        (NoteBook.add_tags, "(self, note_id, tags)"),
        (NoteBook.find_by_tag, "(self, tag)"),
        (NoteBook.sort_by_tags, "(self, tags)"),
        (NoteBook.to_dict, "(self)"),
        (NoteBook.from_dict, "(data)"),
        (storage.load_data, "(path)"),
        (storage.save_data, "(data, path)"),
        (contact_commands.get_handlers, "(book, on_change)"),
        (note_commands.get_handlers, "(notes, on_change)"),
        (cli.run, "(book, notes, on_change, *, has_unsaved_changes)"),
        (ui.prompt, "(label)"),
        (ui.success, "(message)"),
        (ui.error, "(message)"),
        (ui.info, "(message)"),
        (ui.show_contacts, "(contacts)"),
        (ui.show_notes, "(notes)"),
        (ui.show_birthdays, "(items, *, today=None)"),
        (suggestions.suggest_command, "(text, commands)"),
    ],
)
def test_public_signatures(public_callable, parameters):
    contract = signature(public_callable)
    public_parameters = [
        parameter.replace(annotation=parameter.empty)
        for parameter in contract.parameters.values()
    ]
    # The receiver name is an internal choice for instance methods.
    if parameters.startswith("(self"):
        public_parameters[0] = public_parameters[0].replace(name="self")
    without_types = contract.replace(
        parameters=public_parameters, return_annotation=contract.empty
    )
    assert str(without_types) == parameters


@pytest.fixture
def isolated_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    return tmp_path


@pytest.fixture
def startup_arguments(isolated_home, monkeypatch):
    run = Mock()
    monkeypatch.setattr(cli, "run", run)
    runpy.run_path(str(PROJECT_ROOT / "main.py"), run_name="__main__")

    run.assert_called_once()
    # Use the CLI contract to accept positional and keyword calls alike.
    return CLI_SIGNATURE.bind(
        *run.call_args.args, **run.call_args.kwargs
    ).arguments


def test_startup_passes_books_and_callbacks_to_cli(startup_arguments):
    assert isinstance(startup_arguments["book"], AddressBook)
    assert isinstance(startup_arguments["notes"], NoteBook)
    on_change = startup_arguments["on_change"]
    assert callable(on_change)
    signature(on_change).bind()
    has_unsaved_changes = startup_arguments["has_unsaved_changes"]
    assert callable(has_unsaved_changes)
    assert has_unsaved_changes() is False


def test_registries_expose_required_commands(startup_arguments):
    contacts = contact_commands.get_handlers(
        startup_arguments["book"], startup_arguments["on_change"]
    )
    notes = note_commands.get_handlers(
        startup_arguments["notes"], startup_arguments["on_change"]
    )
    required_contacts = {
        "add-contact",
        "list-contacts",
        "edit-contact",
        "delete-contact",
        "find-contact",
        "birthdays",
    }
    required_notes = {
        "add-note",
        "list-notes",
        "edit-note",
        "delete-note",
        "find-note",
        "add-tag",
        "find-tag",
        "sort-notes",
    }

    for registry, required in (
        (contacts, required_contacts),
        (notes, required_notes),
    ):
        assert isinstance(registry, dict)
        assert required <= registry.keys()
        for handler in registry.values():
            assert callable(handler)
            signature(handler).bind()


@pytest.mark.parametrize("exit_command", ["exit", "close", ""])
def test_cli_session(exit_command, isolated_home):
    session = subprocess.run(
        [sys.executable, "-B", "main.py"],
        cwd=PROJECT_ROOT,
        input=f"  \nunknown\nhelp\n{exit_command}\n",
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert session.returncode == 0, session.stderr
    assert "Traceback" not in session.stderr
    for command in ("help", "exit"):
        assert command in session.stdout.casefold()


def test_read_only_session_preserves_saved_data(isolated_home):
    data_directory = isolated_home / ".personal_assistant"
    data_directory.mkdir()
    data_file = data_directory / "data.json"
    before = b'{"schema_version": 1, "contacts": [], "notes": []}\n'
    data_file.write_bytes(before)

    session = subprocess.run(
        [sys.executable, "-B", "main.py"],
        cwd=PROJECT_ROOT,
        input="help\nexit\n",
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert session.returncode == 0, session.stderr
    assert data_file.read_bytes() == before
