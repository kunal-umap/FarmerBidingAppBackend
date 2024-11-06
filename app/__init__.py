from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes import auth, farmer, businessman
    app.register_blueprint(auth.bp)
    app.register_blueprint(farmer.bp)
    app.register_blueprint(businessman.bp)

    return app