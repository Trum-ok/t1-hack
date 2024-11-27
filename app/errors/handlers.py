import logging
from flask import jsonify
from app.errors import bp

logger = logging.getLogger("WEB")


@bp.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Error occurred: {str(e)}", exc_info=True)
    response = {
        "error": str(e),
        "type": type(e).__name__
    }
    return jsonify(response), 500
