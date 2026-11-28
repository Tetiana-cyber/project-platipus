class ValidationError(Exception):
    """Помилка валідації вхідних даних."""


class SaveError(OSError):
    """Помилка збереження даних на диск."""


class StorageLoadError(Exception):
    """Помилка читання або парсингу файлу сховища."""


class StorageSchemaError(Exception):
    """Помилка схеми або версії даних сховища."""


class StorageRecordError(Exception):
    """Помилка структури або валідації окремого запису."""
