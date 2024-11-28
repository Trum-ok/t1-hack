from flask import jsonify

# from app import app_
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/ping', methods=['GET', 'POST'])
def index():
    return jsonify({"msg": "pong"}), 200
