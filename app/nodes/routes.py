from flask import render_template, jsonify
from app.nodes import bp
from app.db import get_db


@bp.get("/nodes")
def index():
    db = get_db()
    nodes = []

    try:
        rows = db.execute("SELECT id, username, password FROM user").fetchall()
    except db.IntegrityError:
        pass
    except db.OperationalError:
        pass

    for row in rows:
        node = {}
        node["id"] = row["id"]
        node["username"] = row["username"]
        node["password"] = row["password"]
        nodes.append(node)

    return jsonify(nodes)


@bp.post("/nodes")
def post():
    db = get_db()

    try:
        db.execute("INSERT INTO user (username, password) VALUES ('ab', 453)")
    except db.IntegrityError:
        print("error")
    except db.OperationalError:
        print("errror")
    return render_template("/base.html", page="node")
