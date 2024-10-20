# Отчет по лабораторной работе №2 со звёздочкой

## Задание

> Написать простое python-приложение, для которого будут писаться докерфайлы и собираться образы.
> 1. Написать “плохой” Docker compose файл, в котором есть не менее трех “bad practices” по их написанию
> 2. Написать “хороший” Docker compose файл, в котором эти плохие практики исправлены
> 3. В Readme описать каждую из плохих практик в плохом файле, почему она плохая и как в хорошем она была исправлена, как исправление повлияло на результат
> 4. После предыдущих пунктов в хорошем файле настроить сервисы так, чтобы контейнеры в рамках этого compose-проекта так же поднимались вместе, но не "видели"
> друг друга по сети.


## Выполнили:
- Михайлов Юрий
- Христофоров Владислав
- Норкина Ярослава


Напишем python-приложение:
``` python
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
```

А также создадим образ на основе докерфайла:
```
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y iputils-ping

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

### "Плохой" Docker Compose file

> Написать “плохой” Docker compose файл, в котором есть не менее трех “bad practices” по их написанию

Напишем Docker Compose файл с плохими практиками:

```
  version: "3"

  services:
      app:
          build: ./app
          ports:
              - "5000:5000"
          environment:
              - DB_HOST=db
              - DB_NAME=mydb
              - DB_USER=user
              - DB_PASSWORD=password
              - APP_VERSION="Bad Compose Version"
          networks:
              - default

      db:
          image: postgres
          environment:
              POSTGRES_DB: mydb
              POSTGRES_USER: user
              POSTGRES_PASSWORD: password
          ports:
              - "5432:5432"
          volumes:
              - db_data_bad:/var/lib/postgresql/data
          networks:
              - default

  volumes:
      db_data_bad:

  networks:
      default:
          driver: bridge
```

Опишем подробно плохие практики, которые были реализованы:

-   Неявное использование версии образа для базы данных:
  `db:
          image: postgres`

    -   Используется образ без указания версии, что может привести к проблемам с совместимостью.


-  Отсутствие зависимости между сервисами:

    -   Нет параметра **_depends_on_**
    -   Отсутствие зависимостей между последовательностью загрузки приложения и базы данных
    -   Приложение может обращаться к базе данных, что вызовет ошибку

-  Отсутствие ограничений ресурсов:

    -   Нет параметра **_resources: limits:_**
    -   Необходимо ограничить работу процессора и выделяемую память для контейнера
    -   Без ограничений контейнеры могут использовать слишком много ресурсов хоста, что может привести к деградации производительности других процессов и сервисов.

---

### "Хороший" Docker Compose file

> Написать “хороший” Docker compose файл, в котором эти плохие практики исправлены

Теперь исправим все ошибки и добавим недостающие параметры:

```
  version: "3.8"

  services:
      app:
          build: ./app
          ports:
              - "5000:5000"
          environment:
              - DB_HOST=db
              - DB_NAME=mydb
              - DB_USER=user
              - DB_PASSWORD=password
              - APP_VERSION="Good Compose Version"
          depends_on:
              - db
          deploy:
              resources:
                  limits:
                      cpus: "0.5"
                      memory: 512M
          networks:
              - default

      db:
          image: postgres:13.4
          environment:
              POSTGRES_DB: mydb
              POSTGRES_USER: user
              POSTGRES_PASSWORD: password
          ports:
              - "5432:5432"
          volumes:
              - db_data_good:/var/lib/postgresql/data
          deploy:
              resources:
                  limits:
                      cpus: "0.5"
                      memory: 512M
          networks:
              - default

  volumes:
      db_data_good:

  networks:
      default:
          driver: bridge
```

Исправления в "хорошем" файле:

-   Добавлена явная версия образа `postgres:13.4`.
-   Добавлен параметр depends_on, гарантирующий запуск базы данных перед приложением.
-   Ограничено использование процессора до 0.5 и памяти до 512M.

---

### Вывод

> Описать, как исправление повлияло на результат

Соберем образы на основе написанных докерфайлов:

`docker build -t bad_image ./devops/lab_2/bad_docker`

`docker build -t good_image ./devops/lab_2/good_docker`

Что же мы можем заметить в результате наших исправлений:

-   **_Размер образа_**: за счет выбора легковесного образа размер собранного docker-образа уменьшился в несколько раз:

    ![размеры образов](screenshots/image_size.png)

-   **_Скорость сборки_**: уменьшение размера образа, отсутствие установки ненужных пакетов повлияли на скорость сборки, он теперь собирается намного быстрее:

    ![время сборки образов](screenshots/build_time.png)

-   **_Безопасность_**: в хорошем образе теперь уделено больше внимания безопасности, т.к. теперь используется актуальный образ, добавлен пользователь без прав root, отсутствуют конфиденциальные данные в слоях образа. Снизу вы можете увидеть, что выводится при запуске контейнеров плохого и хорошего образов без указания параметров (кроме порта):

    `docker run -p 5000:5000 bad_image`

    ![токен в плохом образе](screenshots/bad_secret.png)

    `docker run -p 5000:5001 good_image`

    ![нет токена в хорошем образе](screenshots/good_secret_1.png)

    Как мы видим, в плохом примере мы можем получить токен без каких-либо особых сложностей, потому что он был добавлен прямо в образ. А в хорошем - токена нет, т.к. мы его не передавали. Так, давайте передадим токен во время запуска контейнера через переменные окружения.

    `docker run -p 5002:5000 -e SECRET_TOKEN=my_secret_token good_image`

    ![токен в хорошем образе](screenshots/good_secret_2.png)

    Таким образом, токен мы можем получить только, если сами его передадим при запуске контейнера.

-   **_Скорость пересборки_**: изменим код приложения, пусть в 16 строке теперь будет выводиться другое сообщение:

    ![измененное сообщение](screenshots/app_some_change.png)

    Теперь нужно пересобрать образ, сделаем это и сравним время сборки:

    ![время пересборки образов](screenshots/rebuild_time.png)

    Пересборка хорошего образа осуществилась намного быстрее, чем плохого, благодаря оптимальной установке зависимостей в нем.

---
### Сложности при выполнении 1-3 пунктов



---
### Настройка compose-проекта

> Настроить сервисы так, чтобы контейнеры в рамках этого compose-проекта так же поднимались вместе, но не "видели"
> друг друга по сети.

