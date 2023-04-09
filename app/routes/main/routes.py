from flask import render_template
from app.routes.main import bp

from app.db import get_db
from app.utils.db import select


@bp.route("/")
def index():
    db = get_db()

    devices_active = select(
        db, "node", ["node_id", "created", "type", "state"], where="active = 1"
    )

    devices_inactive = select(
        db, "node", ["node_id", "created", "type", "active"], where="active = 0"
    )

    for element in devices_active:
        element["link"] = f"/devices/{element['node_id']}"

    return render_template(
        "/pages/main.html",
        page="dashboard",
        title="Dashboard",
        devices=devices_active,
        devices_inactive=devices_inactive,
    )
