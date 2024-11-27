import numpy as np

from flask import jsonify, request
from faiss.extractors import FaissIndex, TextEmbedder, DataExtractor

from app.main import bp


def index_file_by_chunks(s3_url, index: FaissIndex, embedder: TextEmbedder):
    """
    Индексирует файл, загруженный с S3, по чанкам (например, из PDF).
    Для каждого чанка текста генерируется вектор и добавляется в FAISS.
    """
    extractor = DataExtractor(embedder)
    chunk_size = 512  # максимальный размер чанка для обработки

    for chunk in extractor.extract_pdf_chunk(s3_url):
        chunks = [chunk[i:i+chunk_size] for i in range(0, len(chunk), chunk_size)]

        for ch in chunks:
            vector = embedder.encode(ch)
            index.add_vectors(np.array([vector], dtype="float32"))


@bp.route('/api/upload/<source_type>/<source_detail>', methods=['POST'])
def upload(source_type, source_detail):
    try:
        if source_type == 'db':
            if source_detail == 'faiss':
                return jsonify({"message": "FAISS database updated successfully."})
            return jsonify({"error": f"Database type '{source_detail}' not supported."}), 400

        elif source_type == 'file':
            data = request.get_data()
            s3_url = data.get('s3_url', '')

            index_file_by_chunks(s3_url, FaissIndex(768), TextEmbedder())
        elif source_type == 'url':
            pass
        return jsonify({"error": f"Тип файла '{source_type}' не поддерживается."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
