from flask import Blueprint

bp = Blueprint('know', __name__)

from app.knowlege_base import routes  # noqa: F401
