from flask import Flask
import os 
from app.db import db

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI='sqlite:///flaskr.sqlite',
    )

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .routes import bp as routes
    app.register_blueprint(routes)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app
