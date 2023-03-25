from flask import render_template
from app.routes.info import bp

@bp.get("/info")
def index():
    return render_template("/pages/info.html", page="info")