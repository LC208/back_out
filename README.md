# Инструкция по запуску проекта

## Запуск вручную

1. Скачиваем репозиторий:
   ```bash
   git clone <repo_url>
   cd <repo_folder>
    ```

2. Создаём виртуальное окружение в папке с проектом:

   * **Windows**:

     ```bash
     py -m venv venv
     ```
   * **Linux / MacOS**:

     ```bash
     python3 -m venv venv
     ```
3. Активируем виртуальное окружение:

   * **Windows**:

     ```bash
     venv\Scripts\activate
     ```
   * **Linux / MacOS**:

     ```bash
     source venv/bin/activate
     ```
4. Устанавливаем все зависимости:

   ```bash
   pip install -r req.txt
   ```

---

## Запуск через Docker

1. Создаём файл `.env` в корне проекта и прописываем все параметры, используемые в `docker-compose.yml`.
2. Поднимаем контейнеры:

   ```bash
   docker-compose up
   ```

   или

   ```bash
   docker compose up
   ```

---

## Параметры `.env`

Пример содержимого `.env`:

```env
# Настройки базы данных
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_PORT=5432

# Путь до SQL-дампа (например, дампа с прода)
DUMP_PATH=./dump.sql

# Переменные для Django (если используются)
SECRET_KEY=your_secret_key
DEBUG="" # (Пустой для False и Любое значение для True)
ALLOWED_HOSTS=*
```

### Важно

* Если вы разворачиваете базу **из дампа (например, с продакшена)**, то в `.env` **обязательно указывайте реальные параметры подключения** (DB\_NAME, DB\_USER, DB\_PASSWORD), соответствующие боевой базе.
* Параметр `DUMP_PATH` должен указывать на путь к вашему дампу, чтобы при старте контейнера Postgres автоматически восстановил данные.
* Если дамп не используется, можно убрать строку с `DUMP_PATH` из `.env` и `volumes` в `docker-compose.yml`.

---

## Структура `docker-compose.yml`

Проект запускается с двумя сервисами:

* **db** — база данных (Postgres 15.8)

  * Инициализируется дампом, если указан `DUMP_PATH`.
  * Параметры берутся из `.env`.
* **back** — backend на Django

  * При запуске выполняет `makemigrations`, `migrate` и запускает сервер на `0.0.0.0:8000`.



