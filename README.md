

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
<img src="https://raw.githubusercontent.com/sanic-org/sanic-assets/master/png/sanic-framework-logo-400x97.png" width="120" height="30">

## API для онлайн-магазина на <a href="https://sanic.dev/en/">Sanic Framework</a>
**1. Сервис авторизации**
* Регистрация (логин / пароль)
* Активация аккаунта по ссылке, отправленной в ответе
* Авторизация через JWT (access_token + refresh_token)

**2. Магазин**
* Просмотреть список всех товаров
* Купить товар
* Просмотреть свои счета и текущий баланс на них
* Просмотреть транзакции
* Зачисление средств на счёт

**3. Администратор**
* Просмотреть все товары (добавить/редактировать/удалить товар)
* Просмотреть всех пользователей и их счета
* Изменить статус пользователя (заблокировать/разблокировать, назначить администратором)
________________________________________________________________
## УСТАНОВКА
<ol>
    <li>Установить <a href="https://docs.docker.com/">Docker</a> и <a href="https://docs.docker.com/compose/">Docker-compose</a>
    <li>Клонировать репозиторий <code>https://github.com/AgafonovSiberia/Store_API_SanicFramework.git</code>
    <li>Перейти в рабочую директорию <code>cd Store_API_SanicFramework</code>
    <li>Заменить <code>.env-example</code> на <code>.env_prod</code> и заполнить его
    <li>Запустить приложение командой <code>make run</code>
  </ol>
Чтобы остановить приложение <code>make stop</code>

________________________________________________________________

## ДОКУМЕНТАЦИЯ API
Документация <b>Swagger</b> доступна по <a href="http://0.0.0.0:8080/docs">0.0.0.0:8080/docs</a>


