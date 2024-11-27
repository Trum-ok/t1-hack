from flask import jsonify
from app.main import bp


@bp.route('/upload/<source_type>/<source_detail>', methods=['POST'])
def upload(source_type, source_detail):
    try:
        if source_type == 'db':
            if source_detail == 'faiss':
                return jsonify({"message": "FAISS database updated successfully."})
            return jsonify({"error": f"Database type '{source_detail}' not supported."}), 400

        elif source_type == 'file':
            uploaded_file = None
            # uploaded_file = request.files.get('file')
            # if not uploaded_file:
            #     return jsonify({"error": "No file uploaded."}), 400

            file_type = source_detail  # Тип файла (например, 'json', 'csv', и т.д.)
            if file_type == 'json':
                # Логика обработки JSON
                data = uploaded_file.read()
                # Загрузить данные в память, векторизовать или сохранить
                return jsonify({"message": "JSON file processed successfully."})
            elif file_type == 'csv':
                # Логика обработки CSV
                data = uploaded_file.read()
                # Обработка данных
                return jsonify({"message": "CSV file processed successfully."})
        elif source_type == 'url':
            pass
        return jsonify({"error": f"Тип файла '{source_type}' не поддерживается."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
