from flask import render_template
from app.main import bp

from app.db import get_db


@bp.route("/")
def index():
    db = get_db()
    devices = []

    try:
        devices_rows = db.execute("SELECT node_id, created, type FROM node").fetchall()
    except db.Error as e:
        print(e)

    for row in devices_rows:
        device = {}
        device["node_id"] = row["node_id"]
        device["created"] = row["created"]
        device["type"] = row["type"]
        device["link"] = f"/devices/{device['node_id']}"
        devices.append(device)

    return render_template("/pages/main.html", page="dashboard", devices=devices)
