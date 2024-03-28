# Функциональные тесты

## Запуск

### Подготовка API и окружения

Поднимите API сервис с сопутствующей инфраструктурой:

```
docker compose up -d
```

Команда запустит:
- API-сервис по адресу http://localhost:8001 (в сети докера http://api:8000)
- Elasticsearch по адресу http://localhost:9201 (в сети докера http://test-elasticsearch:9200)
- Redis по адресу `redis://localhost:6380` (в сети докера `redis://test-redis:6379`)

Для завершения работы API выполните:

```
docker compose down
```

### Запуск тестов

```
pytest -k functional
```
