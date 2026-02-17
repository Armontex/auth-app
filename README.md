# Приложение для авторизации на модели RBAC

## Содержание

- [Приложение для авторизации на модели RBAC](#приложение-для-авторизации-на-модели-rbac)
  - [Содержание](#содержание)
  - [Сущности и связи в БД](#сущности-и-связи-в-бд)
    - [Сущности](#сущности)
      - [users](#users)
      - [roles](#roles)
      - [permissions](#permissions)
      - [user\_roles](#user_roles)
      - [role\_permissions](#role_permissions)
    - [Связи](#связи)
  - [Endpoints](#endpoints)
    - [`auth/register`](#authregister)
    - [`auth/login`](#authlogin)
    - [`auth/logout`](#authlogout)

---

## Сущности и связи в БД

### Сущности

#### users

- id
- first_name
- middle_name (отчество)
- last_name
- email
- password_hash
- is_active
- created_at

#### roles

- id
- code
- name

#### permissions

- id
- resource
- action
- description

#### user_roles

- user_id
- role_id

#### role_permissions

- role_id
- permission_id

### Связи

- users <-> roles через user_roles
- roles <-> permissions через role_permissions

---

## Endpoints

### `auth/register`

**Доступность**: Public

**Метод**: `POST`

**Заголовки**:

- Content-Type: application/json

**Request**:

```json
{
  "first_name": "some-first-name",
  "middle_name": "some-middle-name",
  "last_name": "some-last-name",
  "email": "admin@example.com",
  "password": "some-password",
  "confirm_password": "some-password"
}
```

**Response**:

1. `201 Created` - успешная регистрация

```json
{ "id": 1, "email": "ivan@example.com" }
```

2. `400 Bad Request` - ошибки валидации

```json
{
  "email": ["Enter a valid email address."],
  "password": ["Passwords do not match."]
}
```

3. `409 Conflict` - пользователь с таким `email` уже существует

```json
{
  "detail": "User with this email already exists."
}
```

### `auth/login`

**Доступность**: Public

**Метод**: `POST`

**Заголовки**:

- Content-Type: application/json

**Request**:

```json
{
  "email": "your@example.com",
  "password": "your-password"
}
```

**Response**:

1. `2O0 OK` - успешная авторизация

```json
{ "access_token": "<token>" }
```

После успешного login, клиент получает `access_token` и передаёт его в `Authorization: Bearer <token>`

2. `400 Bad Request` - запрос неправильной формы

```json
{ "email": ["This field is required."] }
```

3. `401 Unauthorized` - неверные учётные данные.

```json
{
  "detail": "Invalid credentials."
}
```

### `auth/logout`

**Доступность**: Protected

**Метод**: `POST`

**Заголовки**:

- Authorization: Bearer `<token>`

**Response**:

1. `204 No Content` - успешный logout

2. `401 Unauthorized` - токен отсутствует / невалиден / истёк

```json
{
  "detail": "Invalid or expired token."
}
```

или

```json
{
  "detail": "Authentication credentials were not provided."
}
```

