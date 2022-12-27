#!/usr/bin/python3
"""Set up the application.

Involves establishing the configuration settings for the
application and ensuring the instance folder exists.
"""

import os
from flask import Flask
from main import db
from main.views import auth


def create_app(test_config=None):
    """Create and configure the application.

    Args:
        test_config (str): path to configuration file.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Create the instance folder if it doesn't already exist
    print(f'Database: {app.config["DATABASE"]}')
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        print(f'Directory {app.instance_path} could not be created')

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)
    app.register_blueprint(auth.auth_views)

    return app
