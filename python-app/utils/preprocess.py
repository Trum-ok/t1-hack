import json
import requests
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from abc import ABC
from pymongo import MongoClient
import mysql.connector
import psycopg2


class Loader(ABC):
    def __init__(self) -> None:
        super().__init__()


class FileLoader(Loader):
    def __init__(self, file_path) -> None:
        super().__init__()
        self.file_path = file_path

    def load_pdf(file_path):
        text = ""
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def load_xlsx(file_path):
        return pd.read_excel(file_path).to_dict(orient='records')

    def load_txt(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def load_docx(file_path):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])


class DBLoader(Loader):
    def __init__(self) -> None:
        super().__init__()

    def load_mysql(db_config, query):
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def load_postgresql(db_config, query):
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def load_mongodb(db_config, collection_name):
        client = MongoClient(db_config['uri'])
        db = client[db_config['db_name']]
        collection = db[collection_name]
        return list(collection.find({}))


class URLLoader(Loader):
    def __init__(self) -> None:
        super().__init__()

    def load_from_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to load URL: {url} with status code {response.status_code}")

