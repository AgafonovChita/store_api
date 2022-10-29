
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<img src="https://raw.githubusercontent.com/sanic-org/sanic-assets/master/png/sanic-framework-logo-400x97.png" width="120" height="30">
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## API для онлайн-магазина на <a href="https://sanic.dev/en/">Sanic Framework</a>
1. Сервис авторизации
* Регистрация (логин / пароль)
* Активация аккаунта по ссылке
* Авторизация через JWT (access_token + refresh_token)
2. Магазин
* Получить список товаров
* Купить товар
* Получить свои счета и баланс
* Получить транзакции
* Зачисление средств на счёт
3. Администратор
* Получить все товары (добавить / редактировать / удалить товар)
* Получить всех пользователей и их счета
* Изменить статус пользователя (заблокировать, разблокировать, назначить администратором)
________________________________________________________________
## УСТАНОВКА
<ol>
    <li>Установить Docker и Docker-compose
    <li>Клонировать репозиторий <code>git clone https://github.com/AgafonovChita/store_api.git</code>
    <li>Перейти в рабочую директорию <code>cd store_api</code>
    <li>Запустить контейнер <code>make run</code>
  </ol>
Чтобы остановить приложение <code>make stop</code><p>


