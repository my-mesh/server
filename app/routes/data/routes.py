from flask import jsonify, request, redirect
from app.routes.data import bp
from app.db import get_db


@bp.get("/data")
def index():
    db = get_db()
    nodes = []

    try:
        rows = db.execute(
            "SELECT data_id, created, payload, node_id FROM data"
        ).fetchall()
    except db.Error as e:
        print(e)

    for row in rows:
        node = {}
        node["data_id"] = row["data_id"]
        node["created"] = row["created"]
        node["payload"] = row["payload"]
        node["node_id"] = row["node_id"]
        nodes.append(node)

    return jsonify(nodes)


@bp.post("/data")
def post():
    db = get_db()
    form = request.form

    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO data (payload, node_id) VALUES (?, ?)",
            (form.get("payload"), form.get("node_id")),
        )
        db.commit()
    except db.Error as e:
        print(e)

    if form.get("redirect") == "True":
        return redirect(request.referrer)

    return jsonify({"status": "ok"})
