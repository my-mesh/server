from flask import render_template
from app.routes.screens import bp


@bp.get("/screens/")
def index():
    return render_template("/pages/screens.html", page="info")
