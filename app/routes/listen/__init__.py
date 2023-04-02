from flask import Blueprint

bp = Blueprint("listen", __name__)

from app.routes.listen import routes
