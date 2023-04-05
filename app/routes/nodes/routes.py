import json
from flask import jsonify, redirect, request, stream_with_context, Response
import gevent
from app.routes.nodes import bp
from app.db import get_db
from app.utils.db import select
import datetime
from .utils import handle_delete, handle_patch, handle_post


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
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            nodes = select(db, "node", ["node_id", "created", "type"], where="created > ? AND active = 0",args=(now,))
            
            if len(nodes) != 0:
                now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            stream = "data: {}\n\n".format(json.dumps(nodes, default=str))

            print("data")
            gevent.sleep(10)
            yield stream

    return Response(event_stream(), mimetype="text/event-stream")


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
