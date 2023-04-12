from flask import render_template
from app.db import get_db
from app.routes.led import bp
from app.utils.db import select
import board
import neopixel

@bp.get("/led")
def index():
    pixels = neopixel.NeoPixel(board.D12, 24, brightness=0.1, auto_write=False)
    pixels.fill((255,0,0))
    pixels.show()
