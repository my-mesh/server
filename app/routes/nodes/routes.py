import json
from flask import jsonify, redirect, request, stream_with_context, Response
import gevent
from app.routes.nodes import bp
from app.db import get_db
from app.utils.db import select, insert, update, delete
import datetime


@bp.get("/nodes/")
def index():
    db = get_db()

    data = select(db, "node", ["node_id", "created", "type", "active"])

    return jsonify(data)


@bp.get("/nodes/sse")
def get_see():
    db = get_db()

    @stream_with_context
    def event_stream():
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        while True:
            nodes = select(
                db,
                "node",
                ["node_id", "created", "type"],
                where="created > ? AND active = 0",
                args=(now,),
            )

            if len(nodes) != 0:
                now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

            stream = "data: {}\n\n".format(json.dumps(nodes, default=str))

            print("data")
            gevent.sleep(10)
            yield stream

    return Response(event_stream(), mimetype="text/event-stream")


@bp.post("/nodes/")
def post():
    db = get_db()
    form = request.form

    id = insert(db, "node", ["type"], [form.get("type")])

    if form.get("redirect") == "True":
        return redirect(request.referrer)

    return jsonify({"status": "ok", "id": id})


@bp.post("/nodes/<id>")
def post_id(id):
    db = get_db()
    form = request.form

    columns = []
    values = []

    for key, value in form.items():
        if key != "method" and key != "redirect":
            columns.append(key)
            values.append(value)

    print(columns)
    print(values)

    if form.get("method") == "patch":
        update(db, "node", columns, values, "node_id = ?", (id,))
    elif form.get("method") == "delete":
        delete(db, "node", "node_id = ?", (id,))

    if form.get("redirect") == "True":
        return redirect(request.referrer)

    return jsonify({"status": "ok"})
