from flask import Blueprint, request, jsonify
from firebase_admin import auth
from sqlalchemy import desc
from models import db, User, Build

api = Blueprint('api', __name__)

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