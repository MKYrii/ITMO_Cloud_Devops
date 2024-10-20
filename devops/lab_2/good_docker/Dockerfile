# "Хороший" Dockerfile

# Легковесный и актуальный образ Python
FROM python:3.9-slim

# Объединяем команды RUN
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /good_docker

# Сначала копируем только файл зависимостей, чтобы сохранить кэш слоёв
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы после установки зависимостей (чтобы изменения кода не пересобирали зависимости)
COPY . .

# Не сохраняем секреты в образе — они будут передаваться через переменные окружения

# Запуск от обычного пользователя для повышения безопасности
USER nobody

CMD ["python", "app/app.py"]
