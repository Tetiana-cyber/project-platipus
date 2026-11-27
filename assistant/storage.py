"""Збереження даних у JSON. Owner: Tech Lead.

Файл: ~/.personal_assistant/data.json
(можна змінити змінною оточення PA_DATA_FILE — зручно для тестів).
"""

from __future__ import annotations

import json
import os
from pathlib import Path


def data_path() -> Path:
    custom = os.environ.get("PA_DATA_FILE")
    if custom:
        return Path(custom)
    return Path.home() / ".personal_assistant" / "data.json"


def load_data() -> dict:
    """Читає дані. Якщо файлу немає або він пошкоджений — порожній словник."""
    path = data_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_data(data: dict) -> None:
    """Записує дані (спочатку у тимчасовий файл, щоб не втратити старі)."""
    path = data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)
