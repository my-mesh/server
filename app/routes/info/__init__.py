from flask import Blueprint

bp = Blueprint('info', __name__)

from app.routes.info import routes