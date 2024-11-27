# T1-Hack
## 

## Локальный запуск
```bash
docker-compose -f s3/docker-compose-minio.yaml up -d
docker-compose -f docker-compose-app.yaml up -d
```

## Модели, используемые в проекте
- [DeepPavlov/rubert-base-cased-sentence](DeepPavlov/rubert-base-cased-sentence) - преобразования для семантического поиска
- []

## что здесь должно быть?
я хочу использовать RAG для какой-нибудь API модели. 

Для RAG использовать FAISS. Моя задача написать это все здесь, собрать в докере и дописать ко всему этому инструкцию по запуску.


## Файловая структура проекта
```bash
 ├── app
 │   ├── api
 │   │   ├── __init__.py
 │   │   └── routes.py
 │   ├── errors
 │   │   ├── __init__.py
 │   │   └── handlers.py
 │   ├── knowlege_base
 │   │   ├── __init__.py
 │   │   └── routes.py
 │   ├── main
 │   │   ├── __init__.py
 │   │   └── routes.py
 │   └── __init__.py
 ├── db
 │   ├── app_db
 │   │   ├── tables
 │   │   │   ├── __init__.py
 │   │   │   ├── databases.py
 │   │   │   ├── files.py
 │   │   │   └── websites.py
 │   │   ├── base.py
 │   │   └── main.py
 │   ├── nosql
 │   ├── sql
 │   ├── vector
 │   └── __init__.py
 ├── faiss          - файлы для работы с FAISS
 │   ├── __init__.py
 │   ├── extractors.py
 │   ├── main.py
 │   └── test.json
 ├── models         - обертки для удобной работы с API
 │   ├── __init__.py
 │   ├── anthropi.py
 │   ├── dev.py
 │   ├── google.py
 │   ├── llama.py
 │   └── openai.py
 ├── s3             - локальное S3 хранилище
 │   ├── config
 │   │   └── certs
 │   │       └── CAs
 │   ├── data
 │   │   └── mybucket
 │   └── docker-compose-minio.yaml
 ├── utils
 │   ├── __init__.py
 │   ├── log.py
 │   └── nodes.py
 ├── .dockerignore
 ├── .gitignore
 ├── Dockerfile
 ├── LICENSE.txt
 ├── config.py
 ├── docker-compose.yaml
 ├── nodes.md
 ├── readme.md
 └── requirements.txt
 ```