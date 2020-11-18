![yatube](https://github.com/frolkit/yatube/workflows/yatube/badge.svg)

# [yatube](https://yatube.frolkit.gq/)
Первый проект на Django. Простой сайт-блог для публикации постов. Можно оставлять комментарии, подписываться на авторов. Реализовано полное дублирование функционала с помощью API.

Стек: Django, DRF, Python, Docker, PostgreSQL, Nginx, GitHub Actions.

Сайт доступен: https://yatube.frolkit.gq/

## Инструкция по развёртыванию.
1. Создайте отдельную папку для проекта. Все дальнейшие действия выполняйте из неё.

2. Скопируйте себе файл docker-compose.yaml

3. Создайте и заполните файл .env
```
DEBUG=False
SECRET_KEY=Сгенерируйте ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgresql
POSTGRES_USER=postgresql
POSTGRES_PASSWORD=postgresql
DB_HOST=db
DB_PORT=5432
```

4. Запустите контейнеры
```
docker-compose up -d
```

5. Сделайте миграции.
```
docker-compose exec web python manage.py migrate
```

6. Сервер доступен по 127.0.0.1:80

## Настройка приложения.

1. Создание суперпользователя
```
docker-compose exec web python manage.py createsuperuser
```
