import os
import warnings

# === WARNINGS CONFIGURATION ===
warnings.simplefilter(action='ignore', category=FutureWarning)

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import firebase_admin
from firebase_admin import credentials
from sqlalchemy import inspect, text
from kafka_consumer import run_consumer_thread

from models import db
from seeds import seed_reference_data
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
def ensure_feature_schema_alignment():
    inspector = inspect(db.engine)

    if "features" not in inspector.get_table_names():
        return

    feature_columns = {column["name"] for column in inspector.get_columns("features")}

    if "category" in feature_columns:
        return

    with db.engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE features "
                "ADD COLUMN category VARCHAR(80) NOT NULL DEFAULT 'uncategorized'"
            )
        )


with app.app_context():
    db.create_all()
    ensure_feature_schema_alignment()
    seed_reference_data()

if __name__ == "__main__":
    # Prevents the Kafka thread from starting twice
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("Launching Kafka Consumer thread...")
        run_consumer_thread(app)
    else:
        print("Initializing application context...")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
