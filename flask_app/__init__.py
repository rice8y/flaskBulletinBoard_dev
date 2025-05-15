from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from .controllers import index
    app.register_blueprint(index.bp)

    @app.before_request
    def before_request():
        try:
            with app.app_context():
                db.create_all()
        except Exception as e:
            print(f"Table creation error: {e}")
    
    return app
