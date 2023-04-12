from flask import render_template
from app.routes.screens import bp
import json
from flask import jsonify, redirect, request, stream_with_context, Response
from app.db import get_db
from app.utils.db import select, insert, update, delete


@bp.get("/screens/")
def index():
    db = get_db()

    screens = select(db, "screens", ["screens_id", "name", "active"])

    return render_template("/pages/screens.html", page="info", screens=screens)


@bp.post("/screens/")
def post():
    db = get_db()
    form = request.form

    print("yes")

    update(db, "screens", ["active"], ["0"])

    update(
        db,
        "screens",
        ["active"],
        ["1"],
        where="screens_id = ?",
        args=(form.get("screens_id"),),
    )

    if form.get("redirect") == "True":
        return redirect(request.referrer)

    return jsonify({"status": "ok"})
