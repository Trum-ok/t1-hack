from urllib.parse import urlparse
import validators
import numpy as np
import requests
import torch
import os
import json
import faiss
import pdfplumber
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import BertModel, BertTokenizer
from config import backet
from s3.main import minio_client


class FaissIndex:
    def __init__(self, dimension, index_path="knowledge_base.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(dimension)  # L2 метрика
        self.metadata = []

    def add_vectors(self, vectors, texts):
        """Добавляет векторы в индекс"""
        self.index.add(vectors)
        self.metadata.extend(texts)

    def save(self):
        """Сохраняет индекс на диск"""
        faiss.write_index(self.index, self.index_path)

    def load(self):
        """Загружает индекс с диска"""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

    def get_metadata(self, indices):
        """Получает метаданные (тексты) по индексам"""
        return [self.metadata[i] for i in indices]


class TextEmbedder:
    def __init__(self, model_name="DeepPavlov/rubert-base-cased-sentence"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)

    def encode(self, text):
        """Генерирует векторное представление текста"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


class DataExtractor:
    def __init__(self, embedder):
        self.embedder = embedder

    def extract_pdf(self, url):
        """Потоковая обработка PDF файла"""
        response = requests.get(url, stream=True)
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    yield text

    def extract_html(self, url):
        """Извлечение текста из HTML страницы"""
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()

    def extract_text(self, url):
        """Определяет тип источника и извлекает текст"""
        parsed = urlparse(url)
        if parsed.path.endswith(".pdf"):
            for text in self.extract_pdf(url):
                yield text
        else:
            yield self.extract_html(url)

    def extract_pdf_chunk(self, s3_url):
        """Загрузка PDF по чанкам с S3"""
        objects = minio_client.list_objects(backet)
        if s3_url not in objects:
            raise ValueError("Not found")

        file_object = minio_client.download_file(backet, s3_url, s3_url.split("/")[-1])
        # file_object = json.loads('test.json')
        file_stream = file_object['Body']
        print(file_object, file_stream)

        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    yield text


class KnowledgeBaseBuilder:
    def __init__(self, dimension=768, index_path="knowledge_base.index"):
        self.embedder = TextEmbedder()
        self.index = FaissIndex(dimension, index_path)
        self.index.load()
        self.extractor = DataExtractor(self.embedder)

    def _extract_text_from_json(self, data):
        """
        Рекурсивно извлекает текстовые данные из словаря JSON.

        :param data: Словарь JSON.
        :return: Список текстовых фрагментов.
        """
        text_chunks = []
        for key, value in data.items():
            if isinstance(value, str):
                text_chunks.append(value)
            elif isinstance(value, dict):
                text_chunks.extend(self._extract_text_from_json(value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        text_chunks.append(item)
                    elif isinstance(item, dict):
                        text_chunks.extend(self._extract_text_from_json(item))
        return text_chunks

    def process_and_index(self, source, source_type="url"):
        """
        Обрабатывает текстовые данные из источника (ссылка или файл) и добавляет их в индекс.

        :param source: Источник данных (ссылка или путь к файлу).
        :param source_type: Тип источника: "url" или "file".
        """
        texts = []
        vectors = []

        if source_type == "url":
            text_chunks = self.extractor.extract_text(source)
        elif source_type == "file":
            file_extension = os.path.splitext(source)[-1].lower()
            if file_extension == ".pdf":
                with open(source, "rb") as f:
                    text_chunks = self.extractor.extract_pdf(BytesIO(f.read()))
            elif file_extension == ".json":
                with open(source, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Предполагаем, что JSON содержит текстовые данные в ключах
                    # Если структура другая, нужно настроить извлечение данных
                    text_chunks = []
                    if isinstance(data, dict):
                        text_chunks = self._extract_text_from_json(data)
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                text_chunks.extend(self._extract_text_from_json(item))
                            elif isinstance(item, str):
                                text_chunks.append(item)

            else:
                raise ValueError(f"Формат файла {file_extension} не поддерживается.")
        else:
            raise ValueError(f"Тип источника {source_type} не поддерживается.")

        for chunk in text_chunks:
            vector = self.embedder.encode(chunk)
            texts.append(chunk)  # Сохраняем текст
            vectors.append(vector)

        # Добавляем векторы и текстовые данные в индекс
        self.index.add_vectors(np.array(vectors, dtype="float32"), texts)


    def search(self, query, top_k=3):
        """Выполняет поиск по базе знаний с использованием FAISS"""
        print(self.index.index.ntotal)  # Число векторов в индексе
        query_vector = self.embedder.encode(query)
        query_vector = np.expand_dims(query_vector, axis=0).astype("float32")

        distances, indices = self.index.index.search(query_vector, top_k)
        print(indices[0])
        print(type(indices[0]))
        print(self.index.metadata)
        results = self.index.get_metadata(indices[0])
        return results, distances[0]

    def save_index(self):
        """Сохраняет индекс на диск"""
        self.index.save()
        return(self.index.index.ntotal)


def get_link_type(url: str) -> str:
    if not validators.url(url):
        raise ValueError("Некорректная ссылка")

    parsed = urlparse(url)
    if "notion" in parsed.netloc:
        return "notion"
    elif "confluence" in parsed.netloc:
        return "confluence"
    elif "drive.google.com" in parsed.netloc:
        return "google_drive"
    elif parsed.path.endswith(".pdf"):
        return "pdf"
    else:
        return "unknown"
