import logging
import os
import signal
import threading
import atexit
import time

from flask import Flask
from app.main import bp as main_bp
from app.nodes import bp as node_bp
from app.devices import bp as devices_bp
from app.data import bp as data_bp

from .mesh import BackgroundThreadFactory
from . import db


def stop_background():
    print("stop event")


def task(test):
    while not test.is_set():
        time.sleep(1)
        print("yes")
    print("end")


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

    notification_thread = BackgroundThreadFactory.create("notification")
    notification_thread.start()

    original_handler = signal.getsignal(signal.SIGINT)

    def sigint_handler(signum, frame):
        notification_thread.stop()

        if notification_thread.is_alive():
            notification_thread.join()

        original_handler(signum, frame)

    try:
        signal.signal(signal.SIGINT, sigint_handler)
    except ValueError as e:
        logging.error(f"{e}. Continuing execution...")

    return app
