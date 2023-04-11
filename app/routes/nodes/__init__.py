from flask import Blueprint

bp = Blueprint("nodes", __name__)

from app.routes.nodes import routes
