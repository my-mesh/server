from flask import Blueprint

bp = Blueprint("screens", __name__)

from app.routes.screens import routes
