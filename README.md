Бэкенд-часть выпускной квалификационной работы "Платформа для обучения с системой оценки и обратной связи"

Используется язык Python и СУБД PostgreSQL и Redis

Запуск:

1. docker compose up - для запуска docker-контейнера с БД
2. pip install -r requirements.txt - установка python библиотек
3. uvicorn app:app --host <ip> - запуск сервера