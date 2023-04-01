from flask import jsonify, redirect, request
from app.routes.nodes import bp
from app.db import get_db

from .utils import handle_form, handle_json

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
    content_type = request.headers.get('Content-Type')

    print(request.form)

    return redirect(request.referrer)

@bp.patch("/nodes/")
def patch():
    db = get_db()
    content_type = request.headers.get('Content-Type')
    
    print(request.form)
    
    return redirect(request.referrer)