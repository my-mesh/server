import time
from flask import Response, stream_with_context
from app.routes.listen import bp

from app.db import get_db

def get_nodes_inactive(db):
    devices = []
    devices_rows = []

    try:
        devices_rows = db.execute(
            "SELECT node_id, created, type, active FROM node WHERE active = 0 "
        ).fetchall()
    except db.Error as e:
        print(e)

    for row in devices_rows:
        device = {}
        device["node_id"] = row["node_id"]
        device["created"] = row["created"]
        device["type"] = row["type"]
        devices.append(device)

    return devices


@bp.get("/listen")
def index():
    db = get_db()

    @stream_with_context
    def event_stream():
        while True:
            stream = "data: {}\n\n".format(get_nodes_inactive(db))
            time.sleep(10)
            print(stream)
            yield stream

    return Response(event_stream(), mimetype="text/event-stream")
