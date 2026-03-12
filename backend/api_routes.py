from flask import Blueprint, request, jsonify
from firebase_admin import auth
from sqlalchemy import desc
from models import db, User, Build, Board

api = Blueprint('api', __name__)


def serialize_feature(feature):
    return {
        "id": feature.id,
        "name": feature.name,
        "description": feature.description,
    }


def serialize_board(board):
    return {
        "id": board.id,
        "name": board.name,
        "description": board.description,
        "toolchain": board.toolchain,
        "cross_compiler": board.cross_compiler,
        "hardware_configuration": board.hardware_configuration,
    }


@api.route("/boards", methods=["GET"])
def get_boards():
    boards = Board.query.order_by(Board.name.asc()).all()
    results = []

    for board in boards:
        results.append(serialize_board(board))

    return jsonify(results)


@api.route("/boards/<board_id>/features", methods=["GET"])
def get_board_features(board_id):
    board = Board.query.filter_by(id=board_id).first()

    if not board:
        return jsonify({"error": "Board not found"}), 404

    results = []
    features = sorted(board.features, key=lambda feature: feature.name.lower())

    for feature in features:
        results.append(serialize_feature(feature))

    return jsonify(results)


@api.route("/profile", methods=["GET"])
def get_profile():
    """
    Fetches the user profile. 
    Implements 'Lazy Sync': if the user exists in Firebase but not in SQL, 
    it creates the record locally on the fly.
    """
    
    # Auth Check
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization Header"}), 401
    
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Database Sync
    user = User.query.filter_by(firebase_uid=uid).first()

    if not user:
        # Create new user if not found
        username = email.split("@")[0] if "@" in email else "user"
        new_user = User(
            firebase_uid=uid,
            email=email,
            username=username,
            role="client"
        )
        db.session.add(new_user)
        db.session.commit()
        user = new_user

    return jsonify({
        "message": "Success",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    })

@api.route("/builds", methods=["GET"])
def get_builds():
    """
    Retrieves the list of builds.
    - Filters by user_id if the requester is a 'client'.
    - Returns all builds if the requester is an 'admin'.
    - Limits results to the last 20 records.
    """

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization Header"}), 401
    
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
    except Exception:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = User.query.filter_by(firebase_uid=uid).first()
    
    if not user:
        return jsonify({"error": "User not found in database. Please login first."}), 404

    # --- Query Logic ---
    query = Build.query

    if user.role != 'admin':
        query = query.filter_by(user_id=user.id)

    builds = query.order_by(desc(Build.started_at)).limit(20).all()

    # --- Serialization ---
    results = []
    for b in builds:
        results.append({
            "id": b.id,
            "user_id": b.user_id,
            "status": b.status,
            "configuration": b.configuration, # Sent as raw JSON string, frontend will parse it
            "started_at": b.started_at.isoformat() if b.started_at else None,
            "finished_at": b.finished_at.isoformat() if b.finished_at else None
        })

    return jsonify(results)
