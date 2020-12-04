from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from .exceptions import InvalidUsage

# instantiate db object
db = SQLAlchemy()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # initialize application db
    db.init_app(app)

    @app.errorhandler(InvalidUsage)
    def invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # import and register blueprints
    from vytals.views import main, reading, activity
    app.register_blueprint(main)
    app.register_blueprint(reading)
    app.register_blueprint(activity)

    return app