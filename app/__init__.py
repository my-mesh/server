import logging
import os
import signal

from flask import Flask
from app.routes.main import bp as main_bp
from app.routes.nodes import bp as node_bp
from app.routes.devices import bp as devices_bp
from app.routes.data import bp as data_bp
from app.routes.info import bp as info_bp

from app.threads.factory import BackgroundThreadFactory

from app import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(node_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(info_bp)

    notification_thread = BackgroundThreadFactory.create("notification")

    if (
        not (app.debug or os.environ.get("FLASK_ENV") == "development")
        or os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    ):
        notification_thread.start()

        original_handler = signal.getsignal(signal.SIGINT)

        def sigint_handler(signum, frame):
            notification_thread.stop()

            # wait until thread is finished
            if notification_thread.is_alive():
                notification_thread.join()

            original_handler(signum, frame)

        try:
            signal.signal(signal.SIGINT, sigint_handler)
        except ValueError as e:
            logging.error(f"{e}. Continuing execution...")

    return app
