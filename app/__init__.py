from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.board import Board
    # from app.models.card import Card
    

    # db.init_app(app)
    # migrate.init_app(app, db)

    # # Register Blueprints here
    # from .routes.board_routes import board_bp
    # app.register_blueprint(board_bp)

    # from .routes.card_routes import card_bp
    # app.register_blueprint(card_bp)
    # # from .routes import example_bp
    # # app.register_blueprint(example_bp)

    CORS(app)
    return app