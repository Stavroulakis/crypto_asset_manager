from flask import Flask
from flask import current_app
from .blueprints.auth import auth_bp
from .blueprints.dashboard import dash_bp
from .blueprints.actions import action_bp
def create_cam_app(config_file = None):
    
    app = Flask(__name__)
    if config_file:
        app.config.from_object(config_file)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(action_bp)

    return app