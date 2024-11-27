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


class FaissIndex:
    def __init__(self, dimension, index_path="knowledge_base.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(dimension)  # L2 метрика

    def add_vectors(self, vectors):
        """Добавляет векторы в индекс"""
        self.index.add(vectors)

    def save(self):
        """Сохраняет индекс на диск"""
        faiss.write_index(self.index, self.index_path)

    def load(self):
        """Загружает индекс с диска"""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)


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
        # bucket, key = self._parse_s3_url(s3_url)
        # file_object = s3_client.get_object(Bucket=bucket, Key=key)
        file_object = json.loads('test.json')
        file_stream = file_object['Body']

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

    def process_and_index(self, url):
        """Обрабатывает текстовые данные из ссылки и добавляет их в индекс"""
        for chunk in self.extractor.extract_text(url):
            vector = self.embedder.encode(chunk)
            self.index.add_vectors(np.array([vector], dtype="float32"))

    def save_index(self):
        """Сохраняет индекс на диск"""
        self.index.save()


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
