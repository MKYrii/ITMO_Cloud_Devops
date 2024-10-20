from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv(dotenv_path="/bad_docker/app/.env")

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Получаем токен из переменной окружения
    secret_token = os.getenv("SECRET_TOKEN", "Токен не найден")
    
    # Возвращаем токен в ответе (для демонстрации)
    return jsonify({"message": "Hello, DevOps World!", "token": secret_token})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
