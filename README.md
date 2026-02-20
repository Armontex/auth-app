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
    - [POST `/auth/register/`](#post-authregister)
    - [POST `/auth/login/`](#post-authlogin)
    - [POST `/auth/logout/`](#post-authlogout)
    - [DELETE `/auth/`](#delete-auth)

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

### POST `/auth/register/`

**Доступность**: Public

**Метод**: `POST`

**Заголовки**:

- Content-Type: application/json

**Response**:

1. `201 Created` - успешная регистрация

2. `400 Bad Request` - ошибки валидации

3. `409 Conflict` - пользователь с таким `email` уже существует

### POST `/auth/login/`

**Доступность**: Public

**Метод**: `POST`

**Заголовки**:

- Content-Type: application/json

**Response**:

1. `2O0 OK` - успешная авторизация

2. `400 Bad Request` - запрос неправильной формы

3. `401 Unauthorized` - неверные учётные данные.

### POST `/auth/logout/`

**Доступность**: Protected

**Метод**: `POST`

**Заголовки**:

- Authorization: Bearer `<token>`

**Response**:

1. `204 No Content` - успешный logout

2. `401 Unauthorized` - токен отсутствует / невалиден / истёк

### DELETE `/auth/`

**Доступность**: Protected

**Метод**: `DELETE`

**Заголовки**:

- Authorization: Bearer `<token>`

**Response**:

1. `204 No Content` - пользователь успешно удалён, токен отозван

2. `401 Unauthorized` - токен отсутствует / невалиден / истёк

3. `404 Not Found` - пользователь не существует
