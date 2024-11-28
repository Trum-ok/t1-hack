import json
from flask import jsonify, request

from app.api import bp
from models.dev import Models
from models.anthropi import anthropic_route


@bp.route("/llm/<source>/<model>", methods=['POST'])
def get_answer_from_llm(source: str, model: str):
    """
    Обрабатывает запрос к LLM для заданного источника и модели.

    :param source: Источник модели (например, "anthropic").
    :param model: Модель в рамках источника (например, "SONNET3_5").
    """
    if source.upper() not in Models.__members__:
        return jsonify({"error": f"Model '{source}' does`t support."}), 400

    if source.lower() == "anthropic":
        return anthropic_route(model)

    return jsonify({"error": f"Source '{source}' not implemented yet."}), 501


# @bp.route('/pipe', methods=['POST'])
# def get_pipeline():
#     data = request.get_json()

#     if not data:
#         return jsonify({"error": "No data provided."}), 400
#     try:
#         file = json.loads(data)
