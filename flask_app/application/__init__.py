from flask import Flask
from flask import current_app
from .blueprints.auth import auth_bp

def create_cam_app(config_file = None):
    
    app = Flask(__name__)
    if config_file:
        app.config.from_object(config_file)
    print(app.config['DB_HOST'])
    app.register_blueprint(auth_bp)

    return app