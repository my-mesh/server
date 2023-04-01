from flask import jsonify, redirect, request
from app.routes.nodes import bp
from app.db import get_db

from .utils import handle_delete, handle_patch, handle_post


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
    db = get_db()
    form = request.form

    id = handle_post(db, form)

    if form.get("redirect") == "True":
        return redirect(request.referrer)

    return jsonify({"status": "ok", "id": id})


@bp.post("/nodes/<id>")
def post_id(id):
    db = get_db()
    form = request.form

    if form.get("method") == "patch":
        handle_patch(db, form, id)
    elif form.get("method") == "delete":
        handle_delete(db, form, id)

    if form.get("redirect") == "True":
        return redirect(request.referrer)

    return jsonify({"status": "ok"})
