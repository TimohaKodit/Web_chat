# Правила работы над проектом

## Что это за проект

Учебный веб-мессенджер на FastAPI + WebSocket. Цель — научиться, а не быстро
получить работающий репозиторий. Проект идёт в портфолио на GitHub, в планах —
деплой на реальный сервер.

## Роль Claude в этом проекте — наставник, а не исполнитель

1. **Не писать готовый код проекта и не править файлы за автора.** Направлять:
   объяснять механику, задавать наводящие вопросы, показывать, где ошибка, — но
   решение пишет автор.
2. **Исключение — базовый синтаксис языка.** Автор подзабыл Python и FastAPI,
   поэтому напоминать синтаксис (try/except, списки, словари, классы, async)
   можно и нужно — но **на нейтральных примерах**, не на его задаче.
3. **Исключение — фронтенд.** Автор им не занимается и не изучает его. HTML/JS
   в `app/static/` пишет Claude, когда бэкенд-часть этапа закрыта.
4. **Одна задача за раз.** Не выдавать списками по 3-5 задач — автор просил
   давать ровно одну и писать короче.
5. **Всегда давать ссылки на источники** — официальная документация, MDN, RFC.
6. **Ревью кода — через вопросы.** Не «вот исправленный код», а «посмотри на эту
   строку: что она возвращает?».
7. Если код всё же приводится — только короткий фрагмент, с разбором, что там
   происходит и почему.

## Как ведётся работа

Цикл одной задачи:

```
git switch main && git pull
git switch -c <тип>/<описание>
   ... код, git add, git commit ...
git push -u origin <ветка>
   ... PR на GitHub, читаем диф, мержим, удаляем ветку ...
git switch main && git pull && git branch -d <ветка>
```

Типы веток: `feature/`, `fix/`, `refactor/`, `chore/`, `docs/`.
Сообщения коммитов — в стиле Conventional Commits (`feat:`, `fix:`, `refactor:`).

Правило: **сначала заставь работать, потом сделай красиво** — фича и рефакторинг
идут разными коммитами.

## Стек

- Python + FastAPI, uvicorn
- WebSocket для реального времени
- PostgreSQL (впереди)
- Docker + nginx для деплоя (впереди)

## Запуск

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

## Дорожная карта

Правила движения: один этап — одна или несколько веток, этап закрыт, когда
выполнены **все** критерии готовности. Отметку `[x]` ставит автор. Фронт
(`app/static/`) пишет Claude только после закрытия бэкенд-части этапа.

### Часть 1. Ядро чата (без БД)

- [x] **1. Скелет** — venv, git, `requirements.txt`, `.gitignore`, FastAPI-приложение с `GET /`.
- [x] **2. Эхо-сокет** — `/ws` принимает соединение, возвращает сообщение, ловит `WebSocketDisconnect`.
- [x] **3. Broadcast** — сообщение уходит всем подключённым.
- [x] **4. `ConnectionManager`** — список подключений и рассылка вынесены в класс.
- [x] **5. Статика** — HTML в `app/static/index.html`, отдаётся через `FileResponse`.

- [ ] **6. JSON-протокол**
  - Изучить: `receive_json` / `send_json`, поле `type` как способ различать сообщения.
  - Готово, когда: клиент шлёт `{"text": ...}`, сервер отвечает `{"type": "message", "text": ...}`;
    при мусоре вместо JSON сервер **не падает** и соединение не рвётся у остальных.
  - Проверка: две вкладки, сообщение видно в обеих; отправить невалидный JSON через devtools — сервер жив.
  - Доки: https://fastapi.tiangolo.com/advanced/websockets/ , https://www.starlette.io/websockets/

- [] **7. Имена и системные сообщения**
  - Изучить: как передать имя при подключении (query-параметр `?name=` или первое сообщение), как хранить связку `websocket → name`.
  - Готово, когда: сервер сам проставляет `user` в исходящем сообщении (клиент не может подделать);
    при входе/выходе всем уходит `{"type": "system", "text": "Вася вошёл"}`; имя валидируется (не пустое, ограничена длина).
  - Доки: https://fastapi.tiangolo.com/tutorial/query-params/ , https://docs.python.org/3/tutorial/datastructures.html#dictionaries

- [ ] **8. Валидация через Pydantic**
  - Изучить: `BaseModel`, `ValidationError`, `Field(max_length=...)`, `Literal` для поля `type`.
  - Готово, когда: входящие и исходящие сообщения описаны моделями в `app/schemas.py`;
    невалидное сообщение вызывает ответ `{"type": "error", "text": ...}` только отправителю.
  - Доки: https://docs.pydantic.dev/latest/concepts/models/

- [ ] **9. Структура проекта**
  - Изучить: `APIRouter`, разбиение на модули.
  - Готово, когда: `main.py` только собирает приложение; отдельно `routers/ws.py`, `services/connection_manager.py`, `schemas.py`; ничего не сломалось.
  - Доки: https://fastapi.tiangolo.com/tutorial/bigger-applications/

### Часть 2. Хранение

- [ ] **10. Конфигурация**
  - Изучить: переменные окружения, `.env`, `pydantic-settings`.
  - Готово, когда: `DATABASE_URL`, `SECRET_KEY` читаются из окружения через `Settings`; `.env.example` в репозитории, `.env` — в `.gitignore`.
  - Доки: https://docs.pydantic.dev/latest/concepts/pydantic_settings/ , https://12factor.net/ru/config

- [ ] **11. PostgreSQL в Docker (только БД)**
  - Изучить: `docker compose`, образ `postgres`, тома, `psql`.
  - Готово, когда: `docker compose up -d db` поднимает Postgres; данные переживают перезапуск контейнера; можно зайти через `psql` и выполнить `SELECT 1`.
  - Доки: https://hub.docker.com/_/postgres , https://docs.docker.com/compose/

- [ ] **12. SQLAlchemy async + Alembic**
  - Изучить: `AsyncSession`, `async_sessionmaker`, декларативные модели, миграции, `asyncpg`.
  - Готово, когда: модели `User` и `Message` (`id`, `user_id`, `text`, `created_at`); первая миграция создаёт таблицы;
    `alembic upgrade head` / `downgrade base` проходят чисто; сессия выдаётся через `Depends`.
  - Доки: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html , https://alembic.sqlalchemy.org/en/latest/tutorial.html

- [ ] **13. История сообщений**
  - Изучить: сохранение при broadcast, `GET /messages?limit=&before=` (пагинация), индекс по `created_at`.
  - Готово, когда: каждое сообщение пишется в БД; при подключении клиент получает последние N сообщений; эндпоинт истории отдаёт страницу.
  - Доки: https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html

### Часть 3. Пользователи

- [ ] **14. Регистрация и пароли**
  - Изучить: хеширование (`bcrypt`/`argon2`), почему нельзя хранить пароль, уникальность логина, статус-коды 201/409.
  - Готово, когда: `POST /auth/register` создаёт пользователя с хешем; повторный логин → 409; пароль нигде не логируется и не возвращается.
  - Доки: https://fastapi.tiangolo.com/tutorial/security/ , https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

- [ ] **15. JWT-авторизация**
  - Изучить: структура JWT, `exp`, `HS256`, `OAuth2PasswordBearer`, зависимость `get_current_user`.
  - Готово, когда: `POST /auth/login` выдаёт access-токен; защищённый `GET /me` отвечает 401 без токена и 200 с ним; истёкший токен → 401.
  - Доки: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ , https://datatracker.ietf.org/doc/html/rfc7519

- [ ] **16. Авторизация в WebSocket**
  - Изучить: как передать токен в WS (query-параметр или первое сообщение), коды закрытия (`1008`).
  - Готово, когда: `/ws` без валидного токена закрывается с `1008`; имя в сообщениях берётся из `User` в БД, а не от клиента; этап 7 переписан под это.
  - Доки: https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code

- [ ] **17. Комнаты**
  - Изучить: модель `Room`, связь many-to-many, рассылка только внутри комнаты.
  - Готово, когда: `POST /rooms`, `GET /rooms`, `/ws/{room_id}`; сообщение видно только участникам комнаты; история — по комнате.
  - Доки: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

### Часть 4. Качество

- [ ] **18. Тесты**
  - Изучить: `pytest`, `TestClient` и его `websocket_connect`, фикстуры, тестовая БД, `pytest-asyncio`.
  - Готово, когда: тесты на регистрацию/логин/401, на broadcast между двумя WS-клиентами, на историю; `pytest` зелёный.
  - Доки: https://fastapi.tiangolo.com/advanced/testing-websockets/ , https://docs.pytest.org/en/stable/how-to/fixtures.html

- [ ] **19. Логирование и обработка ошибок**
  - Изучить: модуль `logging`, уровни, обработчики исключений FastAPI, почему `print` — не логирование.
  - Готово, когда: `print` заменён на `logging`; подключения/отключения/ошибки логируются с именем пользователя; необработанное исключение в WS не роняет сервер.
  - Доки: https://docs.python.org/3/howto/logging.html , https://fastapi.tiangolo.com/tutorial/handling-errors/

- [ ] **20. Линтер и pre-commit**
  - Изучить: `ruff` (lint + format), `pre-commit`.
  - Готово, когда: `ruff check .` и `ruff format --check .` чистые; хук запускает их перед коммитом.
  - Доки: https://docs.astral.sh/ruff/ , https://pre-commit.com/

- [ ] **21. CI на GitHub Actions**
  - Готово, когда: на каждый PR запускаются ruff и pytest (Postgres как service); мерж в `main` запрещён при красном CI.
  - Доки: https://docs.github.com/en/actions/quickstart , https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers

### Часть 5. Деплой

- [ ] **22. Dockerfile приложения**
  - Изучить: слои, `.dockerignore`, multi-stage, непривилегированный пользователь, `uvicorn` без `--reload`.
  - Готово, когда: `docker build` собирается; `docker compose up` поднимает `app` + `db`; миграции применяются при старте; образ < 300 MB.
  - Доки: https://docs.docker.com/get-started/ , https://fastapi.tiangolo.com/deployment/docker/

- [ ] **23. nginx + HTTPS**
  - Изучить: reverse proxy, заголовки `Upgrade`/`Connection` для WebSocket, Let's Encrypt.
  - Готово, когда: nginx в compose проксирует HTTP и WS на `app`; сертификат выдан; `http://` редиректит на `https://`; чат работает через `wss://`.
  - Доки: https://nginx.org/en/docs/http/websocket.html , https://certbot.eff.org/

- [ ] **24. VPS**
  - Изучить: SSH-ключи, `ufw`, отдельный пользователь без root, `docker compose` на сервере, `.env` на сервере.
  - Готово, когда: чат доступен по домену; вход по паролю на SSH отключён; открыты только 22/80/443; контейнеры поднимаются после ребута (`restart: unless-stopped`).
  - Доки: https://docs.docker.com/engine/install/ubuntu/ , https://ubuntu.com/server/docs/firewalls

- [ ] **25. Автодеплой**
  - Готово, когда: пуш в `main` → CI → сборка образа → доставка на сервер (SSH-action или `watchtower`) → сервис обновлён без ручных действий.
  - Доки: https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions

### Часть 6. Опционально, для роста

- [ ] **26. Масштабирование broadcast** — Redis Pub/Sub, чтобы два экземпляра `app` видели сообщения друг друга.
- [ ] **27. Статус «онлайн» и «печатает»** — эфемерные события без записи в БД.
- [ ] **28. Rate limiting** — защита от флуда по WS и по `/auth/login`.
- [ ] **29. Refresh-токены** — короткий access + долгий refresh, выход со всех устройств.
- [ ] **30. Наблюдаемость** — `/health`, метрики Prometheus, структурные логи в JSON.

## Текущий этап

**6. JSON-протокол.** После него обновить README: раздел «Протокол» и чекбоксы «Возможности».
