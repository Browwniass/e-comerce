# Demo E-comerce API
API e-comerce, созданный с Django и DRF
### Что может делать
- Регистрация и аутентификация пользователей как с использованием JWT-токенов, так и через гугл сервисы (OAuth2)
- Отправка и подтверждение регистрации по email
- Просмотр товаров для всех зарегистрированных пользователей и Создание, Удаление и Редактирование уже для админов
- Фильтрация, сортировка и отображение продуктов по slug-названию в пути ресурса
- Создание, Удаление категорий для товаров
- Корзина, в которую товары можно добавлять, удалять и изменять желаемое количество
- Оформление заказов и формирование (атомарной операцией) "снимка заказа" для сохранения информации в изначальном виде
- Оплата заказа с интеграцией стороннего платежного провайдера (юкасса; пока подключенная заглушка)
### Использование
- Регистрация, Аутентификация через с сайт ```POST ``` ```/api/auth/jwt/create/``` ```/api/auth/login/``` ```/api/auth/logout/```
- Регистрация и аутентификация через Google ```POST ``` ```/api/oauth/```
- CRUD продуктов ```/api/products/id/slug/```
- Для фильтрации, сортировки продуктов ```/api/products/id/slug?category=2``` и ```/api/products/id/slug?ordering=price```
- CRUD категорий  ```/api/category/slug/```
- Создание, фильтрация продуктов через nested отношения с категориями ```/api/category/slug/products```
- Формирование заказа /api/orders/
- Оплата и получение данных с стороннего провайдера об оплате ```POST``` ```api/payments/``` ```api/payments/webhook/```
### Стек
- Python 3.14
- Django
- Django REST Framework
- PostgreSQL
### Схема
<img width="852" height="642" alt="image" src="https://github.com/user-attachments/assets/cf8d5bb4-08f7-42c0-8a0d-fab1a1c40934" />

### Установка
```
git clone https://github.com/your-username/ecommerce-api.git
```
Установка виртуального окружения и зависимостей
```
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv/Scripts/activate.ps1     # Windows

pip install -r requirements.txt
```
Настройка почты отправки, OAuth, подлкючение к БД через файл .env. В нем заменить на свои данные:
```
...
EMAIL_HOST_USER=corporate_email
EMAIL_HOST_PASSWORD=email_passord

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=social_auth_google_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET="social_auth_google_secret"
```
### Что будет делать
- Пагинация
- Возвращение денег
- Автодокументация swagger
- Картинки у продуктов
- Тесты
- Докеризация
- кешировать с Redis
