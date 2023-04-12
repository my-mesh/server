from flask import Blueprint

bp = Blueprint("led", __name__)

from app.routes.led import routes
