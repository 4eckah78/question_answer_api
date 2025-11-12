# API для вопросов и ответов

REST API для управления вопросами и ответами. Реализовано на Django.

## 🛠 Технологии
- Python 3.11
- Django
- PostgreSQL
- Docker
- pytest

## 🚀 Запуск

1. Убедитесь, что установлены Docker и docker-compose
2. Запустите:

```bash
docker-compose up --build
```

Сервис будет доступен на http://localhost:8000/api/

## 📡 Эндпоинты
- GET /api/questions/ — список вопросов

- POST /api/questions/ — создать вопрос

- GET /api/questions/{id}/ — вопрос + ответы

- DELETE /api/questions/{id}/ — удалить вопрос

- POST /api/questions/{id}/answers/ — добавить ответ

- GET /api/answers/{id}/ — получить ответ

- DELETE /api/answers/{id}/ — удалить ответ

## 🧪 Тесты
```bash
docker-compose exec web pytest
```
## 📝 Логи
Логи пишутся в qa_api.log.

## ✅ Проверка

1. Запусти: `docker-compose up --build`
2. Открой: `http://localhost:8000/api/questions/`
3. Попробуй создать вопрос через `curl`:

```bash
curl -X POST http://localhost:8000/api/questions/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Как пройти в библиотеку?"}'