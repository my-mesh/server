from flask import render_template
from app.main import bp

from app.db import get_db


@bp.route("/")
def index():
    db = get_db()

    try:
        db.execute(
            "INSERT INTO user (username, password) VALUES ('Test', 123)",
        )
        db.commit()
    except db.IntegrityError:
        error = f"User is already registered."

    print(db)
    return render_template("/pages/main.html", page="dashboard")
