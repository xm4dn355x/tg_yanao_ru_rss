# tg_yanao_ru_rss
Телеграм-Бот Публикующий новости официального сайта yanao.ru
## Dependencies
- Python 3.8
- PostgreSQL 10+
- Docker

## How to build and run
```bash
# Сборка контейнера
docker build -t tg_yanao_ru_rss .

# Запуск контейнера
docker run --network host tg_yanao_ru_rss
```