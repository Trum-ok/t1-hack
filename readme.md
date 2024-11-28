# T1-Hack

![img](t1.jpg)

<hr>

- [T1-Hack](#t1-hack)
  - [Локальный запуск](#локальный-запуск)
  - [Как это работает?](#как-это-работает)
  - [Модели, используемые в проекте](#модели-используемые-в-проекте)
  - [Файловая структура проекта](#файловая-структура-проекта)
  - [Лицензия](#лицензия)
  - [Авторы](#авторы)

[Документация](https://t1-hack.com) \
[Репозиторий с документацией](https://github.com/Trum-ok/t1-hack-documentation)

<hr>

## Локальный запуск
in dev
```bash
docker-compose -f s3/docker-compose-minio.yaml up -d
docker-compose -f docker-compose-app.yaml up -d
```
1. Запуск локального S3-хранилища
2. пупупу

    > [!WARNING]  
    > Локальный запуск требует серьезных вычислительных ресурсов (**GPU**)

## Как это работает?
После загрузки базы знаний на сайте, происходит ее индексация - преобразование в вектора. Благодаря этому становится возможным семантический поиск между запросом пользователя и информацией в загруженной базе знаний. Основная идея этого проекта - использование RAG (Retrieval Augmented Generation) для LLM. Добавление/обновление баз знаний не требует много ресурсов и времени, а результат остается на высоте!

> [!TIP]
> Чтобы ускорить поиск в базе знаний, **стоит использовать GPU**

## Модели, используемые в проекте
- [DeepPavlov/rubert-base-cased-sentence](https://huggingface.co/DeepPavlov/rubert-base-cased-sentence) - токенизация для семантического поиска
- [Anthropic Claude 3.5 Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet) - для использование по API на сайте
- []() - для локальных запусков / запусков в контуре
  

## Файловая структура проекта
```bash
 ├── app    - 
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
 ├── db      - вспомогательные файлы для работы с БД
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
 │   └── main.py
 ├── models         - надстройки для удобной работы с API
 │   ├── __init__.py
 │   ├── dev.py
 │   ├── anthropi.py
 │   ├── google.py
 │   ├── llama.py
 │   └── openai.py
 ├── s3             - локальное S3 хранилище
 │   ├── main.py
 │   └── docker-compose-minio.yaml - настройки запуска локального S3
 ├── utils
 │   ├── __init__.py
 │   ├── log.py
 │   └── nodes.py
 ├── .dockerignore
 ├── .gitignore
 ├── Dockerfile
 ├── LICENSE.txt
 ├── config.py
 ├── docker-compose.yaml - главный docker-compose файл
 ├── nodes.md
 ├── readme.md
 └── requirements.txt
 ```

 ## Лицензия

This project is licensed under the MIT License.

## Авторы

Создано командой Invalid Syntax с большой любовью и огромными усилиями.