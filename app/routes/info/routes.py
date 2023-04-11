from flask import render_template
from app.db import get_db
from app.routes.info import bp
from app.utils.db import select


@bp.get("/info")
def index():
    db = get_db()

    screen = select(db, "screens", ["screens_id"], where="active = ?", args=(1,))[0]

    print(screen["screens_id"])

    if (screen["screens_id"] == 1):
        return render_template("/pages/info/time.html", page="info")
    
    if (screen["screens_id"] == 2):
        return render_template("/pages/info/date.html", page="info")
    
    if (screen["screens_id"] == 3):
        return render_template("/pages/info/blank.html", page="info")
