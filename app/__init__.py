from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS
from google.cloud import firestore
from firebase_admin import credentials, firestore, initialize_app

# db = SQLAlchemy()
# migrate = Migrate()
load_dotenv()
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)  
db = firestore.client()


def create_app():
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    
    

    # db = firestore.client()
    # collection = db.collection('users')
    # # Register Blueprints here
    # from .routes.board_routes import board_bp
    # app.register_blueprint(board_bp)
    from .routes.calendar import calendar_bp
    app.register_blueprint(calendar_bp)

    from .routes.firestore_routes import firestore_bp
    app.register_blueprint(firestore_bp)

    # from .routes.card_routes import card_bp
    # app.register_blueprint(card_bp)
    # # from .routes import example_bp
    # # app.register_blueprint(example_bp)

    CORS(app)
    return app
