from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

# Настройки подключения к базе данных
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
APP_VERSION = os.getenv('APP_VERSION', 'Unknown version')

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return jsonify({"status": "Connected to the database!", "version": APP_VERSION})
    except Exception as e:
        return jsonify({"error": str(e), "version": APP_VERSION}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
