### Описание проекта.
Сайт Foodgram, «Продуктовый помощник». Это онлайн-сервис и API для него.

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

[![Foodgram workflow](https://github.com/RederickMind/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/RederickMind/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

## Проект доступен по ссылке:

```
- http://158.160.19.189
```

Foodgram - проект позволяет:

- Просматривать рецепты
- Добавлять рецепты в избранное
- Добавлять рецепты в список покупок
- Создавать, удалять и редактировать собственные рецепты
- Скачивать список покупок

### Технологи проекта:
```
Django 3.2
Django REST framework
Python 3.9.10
Docker
DockerHub
Nginx
GitHub Actions
Postgres SQL
```

## Инструкции по установке
***- Клонируйте репозиторий:***
```
git clone git@github.com:Rederickmind/foodgram-project-react.git
```

## Для работы с удаленным сервером (на ubuntu):
* Выполните вход на свой удаленный сервер

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
* Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

* Cоздайте .env файл и впишите:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса контейнера БД
DB_PORT=5432 # порт для подключения к БД

DEBUG= Значение дебага
SECRET_KEY= Ваш секретный ключ Django проекта
ALLOWED_HOSTS = Разрешенные хосты
```
* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
    
DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>
    
SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>

DEBUG= Значение дебага
SECRET_KEY= Ваш секретный ключ Django проекта
ALLOWED_HOSTS = Разрешенные хосты
```
Workflow состоит из трёх шагов:
- Проверка кода на соответствие PEP8
- Сборка и публикация образа бекенда на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.  
  
* На сервере соберите docker-compose:
```
sudo docker-compose up -d --build
```
* После успешной сборки на сервере выполните команды (только после первого деплоя):
- Соберите статические файлы:
```
sudo docker-compose exec web python manage.py collectstatic --noinput
```
- Примените миграции:
```
sudo docker-compose exec web python manage.py migrate --noinput
```
- Загрузите ингридиенты  в базу данных:
```
sudo docker-compose exec web python manage.py import_ingredients
```
- Создать суперпользователя Django:
```
sudo docker-compose exec web python manage.py createsuperuser
```
- Проект будет доступен по вашему IP

```

### Ссылки для проверки сайта:

[Admin](http://158.160.19.189/admin/login/?next=/admin/)

[Api](http://158.160.19.189/api/)

[Foodgram] (http://158.160.19.189/recipes)

### Автор проекта:
Nikita Levushkin, Yandex Practikum 19+
