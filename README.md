# Проектное задание четвёртого спринта

- [Асинхронный API для кинотеатра](./async_api)
- [ETL сервис](./etl)
- [Доска с задачами](https://github.com/users/a1d4r/projects/2)
- [Список issues](https://github.com/a1d4r/practicum-async-api/issues)

## Установка

```bash
cp infra/postgres/.env.example infra/postgres/.env
```

## Запуск

### Для разработки

Запустить все сервисы разом можно следующей командой:

```bash
COMPOSE_PROFILES=infra,etl,api docker compose up -d
```

Для остановки выполнить:

```bash
COMPOSE_PROFILES=infra,etl,api docker compose down
```

### Для
