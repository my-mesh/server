from flask import render_template, redirect, request
from app.devices import bp
from app.db import get_db


@bp.get("/devices/")
def get_devices():
    db = get_db()
    nodes = []

    try:
        rows = db.execute("SELECT node_id, created, type FROM node").fetchall()
    except db.Error as e:
        print(e)
    
    for row in rows:
        node = {}
        node["node_id"] = row["node_id"]
        node["created"] = row["created"]
        node["type"] = row["type"]
        node["link"] = f"/devices/{node['node_id']}"
        nodes.append(node)

    print(nodes)
    return render_template("/pages/devices.html", page="devices", devices=nodes)


@bp.get("/devices/<node_id>")
def index(node_id):
    db = get_db()

    try:
        device = db.execute(
            "SELECT node_id, created, type FROM node WHERE node_id=?", (node_id,)
        ).fetchall()
    except db.Error as e:
        print(e)

    if len(device) == 0:
        return redirect("/devices")

    try:
        data = db.execute(
            "SELECT node_id, created FROM data WHERE node_id=?", (node_id,)
        ).fetchall()
    except db.Error as e:
        print(e)

    return render_template("/pages/device.html", page="devices", device=device)
