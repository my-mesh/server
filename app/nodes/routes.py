from flask import render_template
from app.main import bp

@bp.route('/nodes')
def index():
    return render_template('/pages/main.html', page="node")