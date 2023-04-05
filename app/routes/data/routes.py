from flask import jsonify, redirect, request, stream_with_context, Response, json
from app.routes.data import bp
from app.db import get_db
import datetime
import gevent
from app.utils.db import select

@bp.get("/data")
def index():
    db = get_db()
    nodes = []

    try:
        rows = db.execute(
            "SELECT data_id, created, payload, node_id FROM data"
        ).fetchall()
    except db.Error as e:
        print(e)

    for row in rows:
        node = {}
        node["data_id"] = row["data_id"]
        node["created"] = row["created"]
        node["payload"] = row["payload"]
        node["node_id"] = row["node_id"]
        nodes.append(node)

    return jsonify(nodes)

@bp.get("/data/sse")
def get_sse():
    db = get_db()

    @stream_with_context
    def event_stream():
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            nodes = select(db, "data", ["payload"], where="created > ? AND node_id = 0",args=(now,))
            
            if len(nodes) != 0:
                now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            stream = "data: {}\n\n".format(json.dumps(nodes, default=str))

            print("data")
            gevent.sleep(2)
            yield stream

    return Response(event_stream(), mimetype="text/event-stream")


@bp.post("/data")
def post():
    db = get_db()
    form = request.form

    print(form)

    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO data (payload, node_id) VALUES (?, ?)",
            (form.get("payload"), form.get("node_id")),
        )
        db.commit()
    except db.Error as e:
        print(e)

    if form.get("redirect") == "True":
        return redirect(request.referrer)

    return jsonify({"status": "ok"})
