from flask import render_template
from app.main import bp

from app.db import get_db


@bp.route("/")
def index():
    db = get_db()

    try:
        rows = db.execute(
            "SELECT node_id, created, type FROM node"
        ).fetchall()
    except db.Error as e:
        print(e)

    return render_template("/pages/main.html", page="dashboard", devices=rows)
