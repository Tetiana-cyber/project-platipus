"""Безпечне сховище даних та керування станом збереження (ST-02)."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from assistant.context import Context
from assistant.exceptions import (
    SaveError,
    StorageLoadError,
    StorageRecordError,
    StorageSchemaError,
)


class StorageManager:
    """Керує завантаженням, збереженням, dirty-станом і повтором запису."""

    EXPECTED_VERSION = 1

    def __init__(self, path: str | Path, context: Context | None = None) -> None:
        self.path = Path(path)
        self.context = context if context is not None else Context()
        self._dirty = False

    def has_unsaved_changes(self) -> bool:
        return self._dirty

    def on_change(self) -> None:
        self._dirty = True

    def load(self) -> Context:
        if not self.path.exists():
            self.context = Context()
            self._dirty = False
            return self.context
        try:
            raw_text = self.path.read_text(encoding="utf-8")
            data = json.loads(raw_text)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise StorageLoadError(
                f"Не вдалося прочитати або розпарсити файл '{self.path}': {exc}"
            ) from exc
        if not isinstance(data, dict):
            raise StorageSchemaError("Кореневий об'єкт сховища має бути словником.")
        version = data.get("version")
        if version != self.EXPECTED_VERSION:
            raise StorageSchemaError(
                f"Непідтримувана версія схеми сховища: {version!r}."
            )
        contacts_raw = data.get("contacts", [])
        notes_raw = data.get("notes", [])
        if not isinstance(contacts_raw, list):
            raise StorageSchemaError("Поле 'contacts' має бути списком.")
        if not isinstance(notes_raw, list):
            raise StorageSchemaError("Поле 'notes' має бути списком.")
        for idx, item in enumerate(contacts_raw):
            if not isinstance(item, dict):
                raise StorageRecordError(
                    f"Некоректний запис контакту на позиції {idx}."
                )
        for idx, item in enumerate(notes_raw):
            if not isinstance(item, dict) or "id" not in item or "text" not in item:
                raise StorageRecordError(f"Некоректний запис нотатки на позиції {idx}.")
        try:
            ctx = Context.from_dict(
                {"version": version, "contacts": contacts_raw, "notes": notes_raw}
            )
        except Exception as exc:
            raise StorageRecordError(
                f"Помилка відновлення записів зі сховища: {exc}"
            ) from exc
        self.context = ctx
        self._dirty = False
        return self.context

    def _build_payload(self) -> dict[str, Any]:
        payload = self.context.to_dict()
        payload["version"] = self.EXPECTED_VERSION
        if not isinstance(payload.get("contacts"), list):
            payload["contacts"] = []
        if not isinstance(payload.get("notes"), list):
            payload["notes"] = []
        return payload

    def save(self) -> None:
        payload = self._build_payload()
        serialized = json.dumps(payload, ensure_ascii=False, indent=2)
        parent = self.path.parent
        tmp_path: Path | None = None
        try:
            parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(
                prefix=f".{self.path.name}.", suffix=".tmp", dir=str(parent)
            )
            tmp_path = Path(tmp_name)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(serialized)
                    handle.flush()
                    os.fsync(handle.fileno())
            except Exception:
                tmp_path.unlink(missing_ok=True)
                raise
            os.replace(tmp_path, self.path)
        except OSError as exc:
            if tmp_path is not None:
                tmp_path.unlink(missing_ok=True)
            self._dirty = True
            raise SaveError(f"Не вдалося зберегти дані у '{self.path}': {exc}") from exc
        self._dirty = False

    def retry_save(self) -> None:
        self.save()
