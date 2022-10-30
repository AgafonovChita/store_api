

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
<p>
<img src="https://github.com/AgafonovSiberia/Store_API_SanicFramework/blob/master/api_1.jpg" width="410" height="390">
<img src="https://github.com/AgafonovSiberia/Store_API_SanicFramework/blob/master/api_2.jpg" width="410" height="390">
</p>

**Полная документация API доступна на** <a href="http://0.0.0.0:8080/docs">0.0.0.0:8080/docs</a>
___________________________________________________________________
## Example
#### Request
` curl -X POST --location "http://0.0.0.0:8080/admin/users_and_wallets" `
<br>
`-H "Content-Type: application/json"`
<br>
`-H "Authorization: eyJhbGciOiJIUzI1XNzIn0.eyJ1c2VzcsImV4cCI6MTY2NzE0ODgxMn0.djuDOcgZYipQruZwWKVt3T7jNPmngFc" `

#### Response

`HTTP/1.1 200 OK`
<br>
`content-length: 296`
<br>
`connection: keep-alive`
<br>
`content-type: application/json`
br

`[
  {
    "user_id": 777,
    "login": "admin",
    "wallets": [
      {
        "wallet_id": 7779,
        "wallet_balance": 1000
      },
      {
        "wallet_id": 7770,
        "wallet_balance": 20
      }
    ]
  },
  {
    "user_id": 555,
    "login": "agafonov",
    "wallets": [
      {
        "wallet_id": 5559,
        "wallet_balance": 100
      },
      {
        "wallet_id": 5551,
        "wallet_balance": 999
      },
      {
        "wallet_id": 5552,
        "wallet_balance": 1000000
      }
    ]
  }
] `

