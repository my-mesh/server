from flask import Blueprint

bp = Blueprint('nodes', __name__)

from app.nodes import routes