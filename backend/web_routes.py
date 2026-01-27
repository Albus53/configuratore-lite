from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import create_access_token, jwt_required
from jsonschema import validate, ValidationError
from jinja2 import Environment, FileSystemLoader
import json
import io
import zipfile

# Create a Blueprint for Web routes
web = Blueprint('web', __name__)

# --- Setup for Yocto Generator ---
# Load schema and templates only for web routes
try:
    with open("schema.json") as schema_file:
        schema = json.load(schema_file)
    env = Environment(loader=FileSystemLoader("template"))
except Exception as e:
    print(f"[WARNING] Template/Schema missing: {e}")

@web.route("/login", methods=["POST"])
def login():
    """Legacy Web Login (Username/Password)."""
    creds = request.get_json()
    username = creds.get("username")
    password = creds.get("password")

    # Hardcoded check (To be replaced with DB check later)
    if username == "admin" and password == "admin123":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid credentials"}), 401

@web.route("/interpret", methods=["POST"])
@jwt_required()
def interpret():
    """Generates the Yocto configuration ZIP file."""
    try:
        config = request.get_json()
        validate(instance=config, schema=schema)
    except ValidationError as exc:
        return jsonify({"errors": [{"message": exc.message}]}), 400
    except Exception as exc:
        return jsonify({"errors": [{"message": str(exc)}]}), 400

    # Render Templates
    config_bbappend = env.get_template("config.bbappend.j2").render(config=config)
    local_conf = env.get_template("local.conf.j2").render(config=config)
    fragment_conf = env.get_template("fragment.conf.j2").render(config=config)

    # Create In-Memory ZIP
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w") as archive:
        archive.writestr("config.bbappend", config_bbappend)
        archive.writestr("local.conf", local_conf)
        archive.writestr("fragment.conf", fragment_conf)

    memory_file.seek(0)

    return send_file(
        memory_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name="yocto-config.zip",
    )