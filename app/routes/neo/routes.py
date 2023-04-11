from flask import jsonify, request
import gevent
from app.routes.neo import bp

import board
import neopixel

pixels = neopixel.NeoPixel(board.D12, 1)

@bp.post("/neo/")
def index():
    form = request.form

    color = form.get("color")
    length = form.get("length")

    pixels.fill((int(color), 0, 0))
    pixels.show()

    gevent.sleep(int(length))
    pixels.deinit()

    return jsonify({"status": "ok"})
