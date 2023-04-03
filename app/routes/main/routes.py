from flask import render_template
from app.routes.main import bp

from app.db import get_db
from app.utils.db import select

@bp.route("/")
def index():
    db = get_db()

    devices = select(db, "node", ["node_id", "created", "type"])

    devices_inactive = select(
        db, "node", ["node_id", "created", "type", "active"], where="active = 0"
    )

    for element in devices:
        element["link"] = f"/devices/{element['node_id']}"

    return render_template(
        "/pages/main.html",
        page="dashboard",
        title="Dashboard",
        devices=devices,
        devices_inactive=devices_inactive,
    )
