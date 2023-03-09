from flask import jsonify
from app.nodes import bp
from app.db import get_db


@bp.get("/nodes")
def index():
    db = get_db()
    nodes = []

    try:
        rows = db.execute("SELECT id, created, type, active FROM node").fetchall()
    except db.Error as e:
        print(e)

    for row in rows:
        node = {}
        node["id"] = row["id"]
        node["created"] = row["created"]
        node["type"] = row["type"]
        node["active"] = row["active"]
        nodes.append(node)

    return jsonify(nodes)


@bp.post("/nodes")
def post():
    db = get_db()

    try:
        db.execute("INSERT INTO node (type) VALUES (?)", ("Test",))
        db.commit()
    except db.Error as e:
        print(e)

    return jsonify([])
