from flask import jsonify, redirect, request
from app.routes.nodes import bp
from app.db import get_db


@bp.get("/nodes/")
def index():
    db = get_db()
    nodes = []

    try:
        rows = db.execute("SELECT node_id, created, type, active FROM node").fetchall()
    except db.Error as e:
        print(e)

    for row in rows:
        node = {}
        node["node_id"] = row["node_id"]
        node["created"] = row["created"]
        node["type"] = row["type"]
        node["active"] = row["active"]
        nodes.append(node)

    return jsonify(nodes)


@bp.post("/nodes/")
def post():
    data = request.json
    db = get_db()

    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO node (type, mesh_id) VALUES (?, ?)",
            ("Test", data["mesh_id"]),
        )
        db.commit()
    except db.Error as e:
        print(e)

    return redirect(request.referrer)
