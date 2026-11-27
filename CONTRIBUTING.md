# CONTRIBUTING v1.0 — Персональний помічник (project-platipus)

Єдині правила для команди й для **усіх AI-інструментів**, які пишуть код у цьому репозиторії.
Якщо правило не описане тут — спитайте Tech Lead (TL), а не вигадуйте.

## 1. Швидкий старт

```bash
git clone https://github.com/Tetiana-cyber/project-platipus.git
cd project-platipus
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python main.py                     # запуск
pytest                             # тести
ruff check . && ruff format --check .   # лінтер і формат
```

- Python: **3.10+** (рекомендовано 3.13, див. `.python-version`).
- Залежності фіксуємо у `requirements*.txt` з точною версією. Нову залежність додає лише TL.

## 2. Модулі та власники

| Файли | Owner | Що робить |
|---|---|---|
| `main.py`, `assistant/{registry,ui,storage,context,suggest,exceptions}.py`, `schemas/`, CONTRIBUTING | **TL — Тетяна У.** | Цикл CLI, реєстр команд, спільний UI, збереження, контракти |
| `assistant/contacts/*` | **Dev 1 — Тетяна** | Контакти: поля, валідація, книга, команди, іменинники |
| `assistant/notes/*` | **Dev 2 — Нік** | Нотатки: теги, пошук, сортування, команди |
| `tests/`, `README.md`, Ruff/CI, Trello | **Scrum Master — Олена** | Тести, документація, якість процесу |

**Правило:** редагуєте лише файли свого модуля. Потрібна зміна в чужому файлі — створіть issue або напишіть власнику.
Змінювати сигнатури зі розділу 4 можна лише через PR, який схвалив TL.

## 3. Git-процес

- `main` захищена: прямі push заборонені, merge лише через PR.
- Гілки: `feature/<task>-<короткий-опис>`, наприклад `feature/SET-03-contacts-models`.
- Коміти: короткі, зрозумілі, у наказовому способі (`Add phone validation`).
- PR: опис «що зроблено / як перевірити»; **мінімум 1 review від іншого учасника**; автор свій PR не мержить.
- Перед PR: `ruff check .`, `ruff format .`, `pytest` — без помилок.
- Конфлікти вирішує автор PR, підтягнувши свіжий `main` (`git pull origin main`).

## 4. Контракти (обов'язкові)

### 4.1 Команда (handler)
```python
def handler(args: list[str], ctx: Context) -> str
```
- Повертає текст для користувача (не `print` усередині).
- Помилки — лише винятками з `assistant/exceptions.py`.
- Реєстрація: `@register("name", "name <arg> — опис")` у `commands.py` свого модуля.

### 4.2 Правила команд
- Імена: нижній регістр, слова через дефіс: `add-contact`, `find-by-tag`.
- Формат: `<дієслово>-<сутність>`: `add-`, `edit-`, `delete-`, `find-`, `show-`.
- Аргументи розділені пробілом; значення з пробілами — в лапках: `add-note "купити хліб"`.
- Некоректний ввід не закриває програму: повідомлення з порадою, що ввести.

### 4.3 Спільні UI-функції (`assistant/ui.py`)
`ask(prompt) -> str`, `print_message(text)`, `print_error(text)`,
`print_table(headers, rows) -> str`, `print_menu(commands)`.
Меню показуємо **лише на старті**.

### 4.4 Винятки
`AssistantError` ← `ValidationError`, `NotFoundError`, `DuplicateError`, `CommandArgumentError`.
Текст винятку = повідомлення користувачу (українською, зрозуміле).

### 4.5 Поля й валідація
| Поле | Правило |
|---|---|
| name | непорожнє, ≤ 50 символів, унікальне серед контактів |
| phone | рівно 10 цифр |
| email | формат `user@domain.tld` |
| birthday | вводиться `DD.MM.YYYY`, зберігається ISO `YYYY-MM-DD` |
| note.text | непорожній |
| tag | нижній регістр, без пробілів, без дублікатів |

### 4.6 Дані (JSON)
- Файл: `~/.personal_assistant/data.json` (змінна `PA_DATA_FILE` для тестів).
- Структура: `{"version": 1, "contacts": [...], "notes": [...]}`.
- Схеми: `schemas/contact.schema.json`, `schemas/note.schema.json`, `schemas/data.schema.json`.
- Моделі мають `to_dict()` / `from_dict()`; книги — `to_list()` / `from_list()`.
- Файли даних у git не комітимо.

### 4.7 Перелік команд (v1.0)
Контакти: `add-contact`, `edit-contact`, `delete-contact`, `find-contact`, `show-contacts`, `birthdays`.
Нотатки: `add-note`, `edit-note`, `delete-note`, `find-note`, `show-notes`, `add-tag`, `find-by-tag`, `sort-notes`.
Загальні: `exit` / `close` / `quit`.

## 5. Стиль коду
- PEP 8, перевіряє Ruff (`pyproject.toml`). Довжина рядка ≤ 88.
- Типи (type hints) і короткий docstring українською чи англійською — послідовно в межах файлу.
- ООП: успадкування для полів (`Field` → `Phone`), композиція для `Record` / `AddressBook`.
- Жодних «магічних» глобальних змінних; стан — у `Context`.

## 6. Інструкція для AI-інструментів
1. Прочитай цей файл повністю перед роботою.
2. Працюй лише у файлах свого модуля (розділ 2).
3. Не змінюй сигнатури, імена команд, схеми й винятки без дозволу TL.
4. Заміни `raise NotImplementedError` реальним кодом; не створюй нових stubs.
5. Не додавай залежностей. Лише стандартна бібліотека.
6. Після змін запусти: `ruff check . && ruff format . && pytest && python main.py`.
7. Не придумуй вимог: джерело правди — цей файл, `schemas/` і ТЗ.

## 7. Definition of Done
- [ ] Працює `python main.py` без помилок імпорту.
- [ ] Валідація полів, коректна обробка помилок ввода.
- [ ] Дані зберігаються й читаються після перезапуску.
- [ ] Тести й Ruff проходять.
- [ ] PR переглянув інший учасник.
- [ ] У фінальній версії **немає stubs** (`raise NotImplementedError`): `grep -rn NotImplementedError assistant/` порожній.
