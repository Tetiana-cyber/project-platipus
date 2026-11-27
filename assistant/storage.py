"""Збереження даних у JSON. Owner: TL.

Файл: ~/.personal_assistant/data.json
(можна змінити змінною оточення PA_DATA_FILE — зручно для тестів).
Формат: див. schemas/data.schema.json.
"""

from __future__ import annotations

from pathlib import Path


def data_path() -> Path:
    """Шлях до файлу даних (враховує PA_DATA_FILE)."""
    raise NotImplementedError


def load_data() -> dict:
    """Читає дані. Якщо файлу немає або він пошкоджений — порожній словник."""
    raise NotImplementedError


def save_data(data: dict) -> None:
    """Записує дані так, щоб не втратити старі при помилці."""
    raise NotImplementedError
