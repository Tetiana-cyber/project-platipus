"""Спільні винятки. Owner: Tech Lead. Нові — лише через PR до TL.

Усі винятки успадковують AssistantError: main.py ловить його,
показує повідомлення користувачу й НЕ закриває програму.
"""


class AssistantError(Exception):
    """Базовий виняток застосунку. Текст = повідомлення для користувача."""


class ValidationError(AssistantError):
    """Некоректне значення поля (телефон, email, дата тощо)."""


class NotFoundError(AssistantError):
    """Контакт або нотатку не знайдено."""


class DuplicateError(AssistantError):
    """Запис уже існує."""


class CommandArgumentError(AssistantError):
    """Неправильна кількість або формат аргументів команди."""
