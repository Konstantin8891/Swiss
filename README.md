# Клиника

## Клонирование

https://github.com/Konstantin8891/Swiss.git

## Активация виртуального окружения и установка зависимостей

Используется python3.13

python3 -m venv venv

. venv/bin/activate

## Запуск тестов

pytest -x

## Запуск проекта

docker compose up --build

## Миграции

docker compose exec backend python manage.py migrate

## Создание суперпользователя

docker compose exec backend python manage.py createsuperuser

## Прекоммит хуки

pre-commit install
pre-commit install --hook-type commit-msg --hook-type pre-push

коммит

cz commit

## Экспорт зависимостей

uv pip compile pyproject.toml --quiet --output-file backend/requirements.txt

## Группы пользователей

Зашиты в миграциях

1 - Доктор
2 - Администратор
3 - Пациент
