from flask import jsonify
from app.nodes import bp
from app.db import get_db


@bp.get("/nodes")
def index():
    db = get_db()
    nodes = []

    try:
        rows = db.execute("SELECT id, created, type, active FROM node").fetchall()
    except db.IntegrityError:
        pass
    except db.OperationalError:
        pass

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
    except db.IntegrityError as e:
        print(e)
    except db.OperationalError as e:
        print(e)

    return jsonify([])
