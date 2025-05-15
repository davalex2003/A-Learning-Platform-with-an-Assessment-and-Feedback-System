Бэкенд-часть выпускной квалификационной работы "Платформа для обучения с системой оценки и обратной связи"

Используется язык Python и СУБД PostgreSQL и Redis
Для запуска приложения необходимо наличие установленного python

Запуск:

1. git clone https://github.com/davalex2003/A-Learning-Platform-with-an-Assessment-and-Feedback-System.git - клонируем репозиторий с приложением
2. python (или python3) -m venv venv - создаём локальное окружение для запуска приложения
3. docker compose up - для запуска docker-контейнера с базой данных
4. python (или python3) -m pip install -r requirements.txt - установка python библиотек
5. cd src - переходим в директорию с исходным кодом
6. uvicorn app:app --host <ip> - запуск сервера