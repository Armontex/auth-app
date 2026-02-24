# Приложение для авторизации на модели RBAC

## Содержание

- [Приложение для авторизации на модели RBAC](#приложение-для-авторизации-на-модели-rbac)
  - [Содержание](#содержание)
  - [Запуск через Docker](#запуск-через-docker)
  - [Сущности и связи в БД](#сущности-и-связи-в-бд)
  - [RBAC](#rbac)
    - [Тестовые пользователи](#тестовые-пользователи)
  - [Endpoints](#endpoints)

---

## Запуск через Docker

Требования: установлен Docker и Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

После этого API будет доступен по адресу [http://localhost:8000](http://localhost:8000), документация - /docs и /redoc.

Данные в контейнерах Postgres/Redis не сохраняются(volumes не используются, так как это тестовый проект).

## Сущности и связи в БД

![Диаграмма БД](/docs/images/db_diagram.svg)

---

## RBAC

| Permission         | limited_user | user | admin |
| ------------------ | ------------ | ---- | ----- |
| profile:me:read    | +            | +    | +     |
| profile:me:update  | -            | +    | +     |
| profile:read       | -            | -    | +     |
| role:me:read       | -            | -    | +     |
| role:read          | -            | -    | +     |
| role:set           | -            | -    | +     |
| permission:me:read | -            | -    | +     |
| permission:read    | -            | -    | +     |

Формат права: `<resource>:<scope>:<action>`, где:
​
`resource` - тип ресурса (profile, role, permission).

`scope` - область действия (me или пусто / глобально).

`action` - операция (read, update, set и т.п.)

### Тестовые пользователи

Для демонстрации RBAC при инициализации создаются три пользователя:

- `limited@example.com` — роль `limited_user`
- `user@example.com` — роль `user`
- `admin@example.com` — роль `admin`

---

## Endpoints

| Method | Path                         | Access    | Description                                  | Required permission | Success codes | Error codes        |
| ------ | ---------------------------- | --------- | -------------------------------------------- | ------------------- | ------------- | ------------------ |
| POST   | /api/v1/auth/login           | Public    | Логин, выдача access token                   | -                   | 200           | 400, 401, 422      |
| POST   | /api/v1/auth/logout          | Protected | Logout, отзыв токена                         | -                   | 204           | 401, 422           |
| DELETE | /api/v1/auth                 | Protected | Удаление текущего пользователя               | -                   | 204           | 401, 404, 422      |
| POST   | /api/v1/auth/change-email    | Protected | Смена email                                  | -                   | 204           | 400, 401, 409, 422 |
| POST   | /api/v1/auth/change-password | Protected | Смена пароля                                 | -                   | 204           | 400, 401, 422      |
| POST   | /api/v1/register             | Public    | Регистрация пользователя                     | -                   | 201           | 400, 409, 422      |
| PUT    | /api/v1/profile/me           | Protected | Обновить свой профиль                        | profile:me:update   | 200           | 400, 401, 403, 422 |
| GET    | /api/v1/profile/me           | Protected | Получить свой профиль                        | profile:me:read     | 200           | 401, 403           |
| GET    | /api/v1/profile              | Protected | Получить профиль по user_id                  | profile:read        | 200           | 400, 401, 403, 422 |
| GET    | /api/v1/rbac/role/me         | Protected | Получить свои роли                           | role:me:read        | 200           | 401, 403           |
| GET    | /api/v1/rbac/role            | Protected | Получить роли пользователя по user_id        | role:read           | 200           | 400, 401, 403, 422 |
| POST   | /api/v1/rbac/role            | Protected | Назначить роль пользователю                  | role:set            | 204           | 400, 401, 403, 422 |
| GET    | /api/v1/rbac/permission/me   | Protected | Получить свои permissions                    | permission:me:read  | 200           | 401, 403           |
| GET    | /api/v1/rbac/permission      | Protected | Получить permissions пользователя по user_id | permission:read     | 200           | 400, 401, 403, 422 |
