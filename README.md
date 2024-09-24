# call_registration_system

Это небольшое Django-приложение, состоящее из API для работы с продуктами и фронтенда на Vite.

Функциональность
API:

  Модель продукта с полями: название, описание, цена
Конечные точки:
  POST /api/products/: Создание нового продукта
  GET /api/products/: Получение списка всех продуктов
Валидация при создании продукта (цена должна быть положительным числом, название не должно быть пустым)

Фронтенд:

Простая HTML-страница с формой для добавления нового продукта
JavaScript-логика для отправки данных формы на API и обновления списка продуктов на странице

Как запустить

1. Клонируйте репозиторий:
```
git clone git@github.com:DoraLoginova/product_market.git

```
2. Создайте (в корне проекта) файл .env (пример файла):

```
SECRET_KEY=django-insecure-o78r3to*^z6s74=1&ie^8qu&#43sojs+s43iq*90e=x37&abxt
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost,127.0.0.1:5173

```
3. Для запуска бэкенда перейдите в директорию:
```
 cd backend
```
4. Создайте и активируйте виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate  

```
 
5. Установите зависимости и примените миграции::
 
```
pip install -r requirements.txt
python manage.py migrate

```

5. Запустите сервер Django::

```
python manage.py runserver

```
6. Перейдите в директорию фронтенда и запустите Vite-сервер отдельном терминале:

```
cd front
npm install
npm run dev
```