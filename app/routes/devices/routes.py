from flask import render_template, redirect
from app.routes.devices import bp
from app.db import get_db
from app.utils.db import select


@bp.get("/devices/")
def get_devices():
    db = get_db()

    devices = select(db, "node", ["node_id", "created", "type"])

    for element in devices:
        element["link"] = f"/devices/{element['node_id']}"

    return render_template(
        "/pages/devices.html", page="devices", title="Geräteliste", devices=devices
    )


@bp.get("/devices/<node_id>")
def index(node_id):
    db = get_db()

    device = select(
        db, "node", ["node_id", "created", "type"], where="node_id = ?", args=(node_id,)
    )

    if len(device) == 0:
        return redirect("/devices")

    nodes = select(
        db,
        "data",
        ["data_id", "created", "payload"],
        where="node_id = ?",
        args=(node_id,),
    )

    return render_template(
        "/pages/device.html",
        page="devices",
        title="Geräte Daten",
        device=device,
        nodes=nodes,
    )
