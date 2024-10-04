# call_registration_system

Описание
Это приложение реализует систему регистрации обращений через веб-интерфейс. Пользователи могут отправлять свои обращения, которые сохраняются в базе данных PostgreSQL. Реализованы следующие компоненты:

Frontend: Веб-интерфейс, который позволяет пользователям отправлять обращения.
Backend: REST API на Tornado, который обрабатывает запросы от фронтенда и взаимодействует с RabbitMQ и PostgreSQL.
База данных: PostgreSQL для хранения обращений.
RabbitMQ: Очередь сообщений для обработки событий.
Установка

Требования
Docker
Docker Compose

Запуск приложения
Клонируйте репозиторий:
```
git clone git@github.com:DoraLoginova/call_registration_system.git

```
Убедитесь, что docker-compose.yml находится в корневой папке проекта.

Запустите команды:

```
docker-compose up --build

```
Это создаст и запустит все сервисы. Frontend будет доступен на http://localhost:3000, а Backend на http://localhost:8000/api/appeal

Структура проекта:
  frontend/ — папка с фронтендом.
  backend/ — папка с бэкендом.
  db/ — папка с настройками для PostgreSQL.
  rabbitmq/ — папка с конфигурациями для RabbitMQ.
  servicedb/ - папка для записи в базу данных

Настройка:

PostgreSQL
В файле docker-compose.yml указаны учетные данные доступа к базе данных:
DB NAME: mydb
USER: user
PASSWORD: password

RabbitMQ
Учетные данные доступны в docker-compose.yml:
USER: guest
PASSWORD: guest

Использование:


Отправка обращения:

Откройте браузер и перейдите по адресу http://localhost:3000.
Заполните форму и нажмите "Отправить".
Обращение будет отправлено на сервер и сохранено в базе данных.

Просмотр обращений:

Данные обращения могут быть получены через GET-запрос по адресу http://localhost:8000/api/appeal.

###PgAdmin (опционально)

Для управления базой данных можно использовать PgAdmin. Для этого раскомментируйте секцию pgadmin в docker-compose.yml и перезапустите контейнеры.

Тестирование:

Вы можете тестировать API с помощью Postman или curl.

Пример запроса для получения всех обращений:

```
curl -X GET http://localhost:8000/api/appeal

```

```
curl -X POST http://localhost:8000/api/appeal \
-H "Content-Type: application/json" \
-d '{
  "last_name": "Иванов",
  "first_name": "Иван",
  "patronymic": "Иванович",
  "phone": "+79161234567",
  "message": "Тестовый текст."
}'

```