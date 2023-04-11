from flask import Blueprint

bp = Blueprint("neo", __name__)

from app.routes.neo import neo
