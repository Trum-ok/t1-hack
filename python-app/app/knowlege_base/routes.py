import os
import sys
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import jsonify, request
from typing import Optional
from vectors.extractors import FaissIndex, TextEmbedder, DataExtractor

from app.knowlege_base import bp


def index_file_by_chunks(s3_url, index: FaissIndex, embedder: TextEmbedder):
    """
    Индексирует файл, загруженный с S3, по чанкам (например, из PDF).
    Для каждого чанка текста генерируется вектор и добавляется в FAISS.
    """
    extractor = DataExtractor(embedder)
    chunk_size = 512  # максимальный размер чанка для обработки

    try:
        print("тут")
        for chunk in extractor.extract_pdf_chunk(s3_url):
            print('chunk:', chunk)
            chunks = [chunk[i:i+chunk_size] for i in range(0, len(chunk), chunk_size)]

            for ch in chunks:
                vector = embedder.encode(ch)
                index.add_vectors(np.array([vector], dtype="float32"))
            print("тут")
    except ValueError as e:
        return jsonify({"error": "Такого файла нет на S3: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/api/upload/<source_type>/', methods=['POST'])
@bp.route('/api/upload/<source_type>/<source_detail>', methods=['POST'])
def upload(source_type: str, source_detail: Optional[str] = None):
    try:
        if source_type == 'db':
            supported_db = ['postgres', 'mysql', 'sqlite', 'mongodb', 'elastic']
            if not source_detail or source_detail not in supported_db:
                return jsonify({"error": f"Database type '{source_detail}' isn`t supported."}), 400

            pass

        elif source_type == 'file':
            data_str = request.get_data().decode('utf-8')

            try:
                data = json.loads(data_str)
                s3_url = data.get('s3_url', '')

                if not s3_url:
                    return jsonify({"error": "s3_url not found"}), 400
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid JSON"}), 400

            if not s3_url:
                return jsonify({"error": "Не указан s3_url."}), 400

            index_file_by_chunks(s3_url, FaissIndex(768), TextEmbedder())
            return jsonify({"success": "Файл проиндексирован"}), 200
        elif source_type == 'url':
            pass
        return jsonify({"error": f"Тип файла '{source_type}' не поддерживается."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
