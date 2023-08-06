from flask import Flask

import routes


def create_app():
    app = Flask(__name__)
    _apply_public_blueprints(app)
    return app


def _apply_public_blueprints(app: Flask):
    for bp in routes.enabled_blueprints:
        app.register_blueprint(bp)
