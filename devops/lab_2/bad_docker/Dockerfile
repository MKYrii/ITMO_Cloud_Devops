# "Плохой" Dockerfile

# Использование устаревшего и неподдерживаемого базового образа
FROM python:3.7

# Выполнение множества команд RUN без объединения (создаёт лишние слои)
# Установка ненужных и неиспользуемых пакетов
# Использование одного только apt-get update в RUN приводит к проблемам с кэшированием и сбою последующих инструкций  apt-get install. 
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y curl

WORKDIR /bad_docker

# Использование ADD вместо COPY для простого копирования файлов (лишние возможности, которые могут привести к ошибкам)
ADD . .

# Установка зависимостей после копирования всех файлов приложения 
RUN pip install --no-cache-dir -r requirements.txt

# Хранение конфиденциальной информации в слоях
RUN echo "SECRET_TOKEN=12345" >> /bad_docker/app/.env

# Запуск от root пользователя (небезопасно)
CMD ["python", "app/app.py"]
