

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
<img src="https://raw.githubusercontent.com/sanic-org/sanic-assets/master/png/sanic-framework-logo-400x97.png" width="120" height="30">

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
    <li>Клонировать репозиторий <code>https://github.com/AgafonovSiberia/store_api_SanicFramework.git</code>
    <li>Перейти в рабочую директорию <code>cd store_api</code>
    <li>Заменить <code>.env-example</code> на <code>.env_prod</code> и заполнить его
    <li>Запустить контейнер <code>make run</code>
  </ol>
Чтобы остановить приложение <code>make stop</code>

________________________________________________________________

## ДОКУМЕНТАЦИЯ API
Документация <b>Swagger</b> доступна по <a href="http://0.0.0.0:8080/docs">0.0.0.0:8080/docs</a>


