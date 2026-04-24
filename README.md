# Widespread Backend

REST API для онлайн магазина одежды.

## Tech Stack

- FastAPI
- PostgreSQL
- JWT Auth

## Запуск

- Установка зависимостей

```sh
  uv sync
```

- Запуск локально

```sh
  uv run uvicorn app.main:app --reload
```

## Линтинг

- Проверить код

```sh
  uv run ruff check .
```

- Исправить ошибки автоматически

```sh
  uv run ruff check . --fix
```

- Форматирование кода

```sh
  uv run ruff format .
```
