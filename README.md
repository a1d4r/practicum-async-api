# Проектное задание четвёртого спринта

- [Асинхронный API для кинотеатра](./async_api)
- [ETL сервис](./etl)
- [Доска с задачами](https://github.com/users/a1d4r/projects/2)
- [Список issues](https://github.com/a1d4r/practicum-async-api/issues)

## Запуск всех сервисов

```bash
COMPOSE_PROFILES=infra,etl,api docker compose up -d
```

Остановить:
```bash
COMPOSE_PROFILES=infra,etl,api docker compose down
```
