import json
import time
from flask import Response, render_template
from app.routes.listen import bp

from app.db import get_db

def get_message():
    '''this could be any function that blocks until data is ready'''
    time.sleep(1.0)
    message = {"message": "Hello World!"}
    return json.dumps(message)

@bp.route("/listen")
def index():
    def eventStream():
        while True:
            print("yes")
            # wait for source data to be available, then push it
            yield "data: {}\n\n".format(get_message())

    return Response(eventStream(), mimetype="text/event-stream")
