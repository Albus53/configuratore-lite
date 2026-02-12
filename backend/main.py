import os
import warnings

# === WARNINGS CONFIGURATION ===
warnings.simplefilter(action='ignore', category=FutureWarning)

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import firebase_admin
from firebase_admin import credentials
from kafka_consumer import run_consumer_thread

from models import db
from api_routes import api
from web_routes import web

# --- App Configuration ---
app = Flask(__name__)
CORS(app)

# Database Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT Config (For Web)
app.config["JWT_SECRET_KEY"] = "supersecret-key"

# --- Services Initialization ---
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

jwt = JWTManager(app)

db.init_app(app)

# --- Register Blueprints ---
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(web)

# --- Startup Logic ---
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Prevents the Kafka thread from starting twice
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("Launching Kafka Consumer thread...")
        run_consumer_thread(app)
    else:
        print("Initializing application context...")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)