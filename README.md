# project-platipus — Персональний помічник

Консольний застосунок для зберігання **контактів** і **нотаток** (Neoversity, командний проєкт з Python).

> Статус: skeleton (SET-02). Функціонал реалізується командою за CONTRIBUTING.md.

## Можливості (за ТЗ)
- Контакти: ім'я, адреса, телефон, email, день народження; пошук, редагування, видалення; іменинники через N днів; валідація.
- Нотатки: додавання, пошук, редагування, видалення; (додатково) теги, пошук і сортування за тегами.
- Дані зберігаються у `~/.personal_assistant/data.json`.

## Встановлення
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Запуск
```bash
python main.py
```

## Тести та якість коду
```bash
pytest
ruff check .
ruff format .
```

## Команди
| Команда | Опис |
|---|---|
| `add-contact`, `edit-contact`, `delete-contact`, `find-contact`, `show-contacts`, `birthdays` | Контакти |
| `add-note`, `edit-note`, `delete-note`, `find-note`, `show-notes`, `add-tag`, `find-by-tag`, `sort-notes` | Нотатки |
| `exit`, `close`, `quit` | Вихід |

## Команда
TL, Scrum Master, Dev 1, Dev 2 — див. CONTRIBUTING.md.
